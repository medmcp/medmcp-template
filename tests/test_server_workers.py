"""Worker processes start under the stdio transport, and nothing but JSON-RPC reaches stdout."""

import os
import signal
import subprocess
import sys
import threading

# The server's main() with the MCP session replaced by what went wrong in the
# rehearsal: a thread blocked reading stdin (as the stdio transport has) while a
# multiprocessing Manager starts (as nnU-Net and PyTorch DataLoaders do), and
# prints from the server, a C library and a worker process.
_CHILD = """
import multiprocessing, os, sys, threading, time
from medmcp_template import server

async def fake_serve(protocol):
    threading.Thread(target=sys.stdin.readline, daemon=True).start()
    time.sleep(0.3)
    print("stray line from the server", flush=True)
    os.write(1, b"stray bytes from a C library\\n")
    worker = multiprocessing.Process(target=print, args=("stray line from a worker",))
    worker.start()
    worker.join()
    manager = multiprocessing.Manager()
    manager.shutdown()
    protocol.write("ok\\n")
    protocol.flush()

server._serve = fake_serve
server.main()
"""


def test_workers_start_while_stdin_is_being_read() -> None:
    """A Manager starts while another thread reads stdin, as under the agent.

    stdin stays open for the whole run, as the agent's pipe does; closing it
    would let the reader thread return and hide the hang.
    """
    proc = subprocess.Popen(
        [sys.executable, "-c", _CHILD],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        start_new_session=True,
    )
    # A hung worker keeps stdout open, so the whole process group goes.
    timer = threading.Timer(60, os.killpg, (proc.pid, signal.SIGKILL))
    timer.start()
    try:
        assert proc.stdout is not None
        out = proc.stdout.read()
        proc.wait()
    finally:
        timer.cancel()
        if proc.stdin:
            proc.stdin.close()
    assert "ok" in out, "a worker process hung at start (forked under the stdin reader)"
    assert out == "ok\n", f"something besides the protocol reached stdout: {out!r}"
    assert proc.returncode == 0
