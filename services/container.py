from typing import Protocol

import docker
from docker.errors import ImageNotFound
from docker.models.containers import Container


class LoggerProtocol(Protocol):
    def send_log(self, message: str): ...

    def close(self): ...


def _create_container(image: str, bash_command: str) -> Container:
    try:
        client = docker.from_env()
        return client.containers.run(
            image,
            ['sh', '-c', bash_command],
            detach=True,
            environment=['PYTHONUNBUFFERED=1'],
        )
    except ImageNotFound:
        print('Docker image not found')


def run_container(image: str, bash_command: str, logger: LoggerProtocol):
    print('Creating container...')
    container = _create_container(image, bash_command)
    if not container:
        return
    print('Container started')
    try:
        logs = container.logs(stream=True)
        for log in logs:
            logger.send_log(log.decode('utf-8').rstrip())
    except KeyboardInterrupt:
        print('Container stops')
    finally:
        container.reload()
        if container.status == 'running':
            container.kill()
        logger.close()
        print('Container stopped')
