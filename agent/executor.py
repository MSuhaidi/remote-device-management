import subprocess
import datetime

ALLOWED_SCRIPTS = {
    "health_check": ["echo", "OK"],
    "echo_test": ["echo", "hello world"],
    "fail_test": ["bash", "-c", "exit 1"]
}

def run_script(script_name: str):
    if script_name not in ALLOWED_SCRIPTS:
        return {
            "stdout": "",
            "stderr": "Script not allowed",
            "status": "failed"
        }

    try:
        command = ALLOWED_SCRIPTS[script_name]
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "status": "success" if process.returncode == 0 else "failed"
        }
    except subprocess.TimeoutExpired as e:
        return {
            "stdout": "",
            "stderr": f"Timeout expired after {e.timeout} seconds.",
            "status": "failed"
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "status": "failed"
        }
