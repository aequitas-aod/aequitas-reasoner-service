import os
import subprocess
import sys

from python_on_whales import DockerClient

if __name__ == "__main__":
    docker = DockerClient(compose_env_file=".")
    docker.compose.up(detach=True)
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
    docker.compose.down(volumes=True)
    exit(process.returncode)
