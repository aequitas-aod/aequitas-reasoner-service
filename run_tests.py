import os
import sys
import subprocess


if __name__ == "__main__":
    subprocess.run("docker compose up -d", shell=True, check=True)

    os.environ["TEST"] = "true"
    process = subprocess.run(
        args=[
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-v",
            "-s",
            "test",
            "-p",
            "test_*.py",
        ],
        env=os.environ,
    )

    subprocess.run("docker compose down -v", shell=True, check=True)

    exit(process.returncode)
