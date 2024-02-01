from functools import wraps

from botocore.client import BaseClient
from botocore.exceptions import ClientError


class ResourceError(BaseException):
    ...


def handle_resource_exists_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ClientError as error:
            if error.response.get('Error', {}).get('Code') != 'ResourceAlreadyExistsException':
                raise ResourceError(error)

    return wrapper


@handle_resource_exists_exception
def create_group(client: BaseClient, group: str):
    client.create_log_group(logGroupName=group, logGroupClass='STANDARD')


@handle_resource_exists_exception
def create_stream(client: BaseClient, group: str, stream: str):
    client.create_log_stream(logGroupName=group, logStreamName=stream)
