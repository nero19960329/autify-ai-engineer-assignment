import os
import resource
import subprocess
import tempfile
import threading


def run_python_code(
    code: str,
    test_code: str,
    timeout_ms=5000,
    memory_limit_mb=256,
) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save code and test files
        with open(os.path.join(tmpdir, "test.py"), "w", encoding="utf-8") as f:
            f.write(code)
            f.write("\n")
            f.write("def test_code():\n")
            for line in test_code.split("\n"):
                f.write(f"    {line}\n")
            f.write("\n")
            f.write("test_code()")

        # Set resource limits
        def set_resource_limits() -> None:
            resource.setrlimit(resource.RLIMIT_CPU, (timeout_ms, timeout_ms))
            resource.setrlimit(
                resource.RLIMIT_AS,
                (memory_limit_mb * 1024 * 1024, memory_limit_mb * 1024 * 1024),
            )

        def kill_process(proc: subprocess.Popen):
            try:
                proc.kill()
            except OSError:
                pass

        # Run tests in a subprocess
        try:
            proc = subprocess.Popen(
                ["python3", os.path.join(tmpdir, "test.py")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=set_resource_limits,
            )

            time = threading.Timer(timeout_ms / 1000, kill_process, [proc])
            time.start()

            _stdout, stderr = proc.communicate()
            time.cancel()

            if proc.returncode == 0:
                return {"result": "success", "message": "Code Executed Successfully"}
            else:
                return {"result": "failure", "message": stderr.decode("utf-8")}
        except subprocess.CalledProcessError as e:
            return {"result": "error", "message": str(e)}
