import sys
import time

from botocore.client import BaseClient
from botocore.exceptions import ClientError, EndpointConnectionError, InvalidRegionError

import settings
from services.aws.resources import ResourceError, create_group, create_stream
from services.aws.session import CredentialsError, get_session
from services.utils import batched, timestamp_ms


class AwsCloudWatchLogger:
    def __init__(self, client: BaseClient, group: str, stream: str):
        self._client = client
        self._group = group
        self._stream = stream
        self._buffer_size = 0
        self._message_buffer = []
        self._last_sending = time.time()

    def send_log(self, message: str):
        message_size = sys.getsizeof(message)
        if message_size < settings.EVENT_LIMIT_SIZE:
            self._process_message(message)
        else:
            self._process_big_message(message)

    def close(self):
        self._send_all_from_buffer()

    def _process_message(self, message: str, timestamp: int = None):
        if message:
            self._message_buffer.append(
                {
                    'timestamp': timestamp or timestamp_ms(),
                    'message': message,
                }
            )
            self._buffer_size += sys.getsizeof(message)
            self._check_message_buffer()

    def _process_big_message(self, message: str):
        ts = timestamp_ms()
        for chunk_message in batched(message, settings.EVENT_LIMIT_SIZE):
            self._process_message(chunk_message, timestamp=ts)

    def _check_message_buffer(self):
        if (
            self._buffer_size >= settings.BUTCH_LIMIT_SIZE
            or len(self._message_buffer) > settings.MAXIMUM_NUMBER_EVENTS
            or time.time() - self._last_sending > settings.SEND_INTERVAL
        ):
            self._send_all_from_buffer()

    def _send_all_from_buffer(self):
        try:
            if self._message_buffer:
                self._client.put_log_events(
                    logGroupName=self._group,
                    logStreamName=self._stream,
                    logEvents=self._message_buffer,
                )
        except ClientError:
            ...
        self._flush_buffer()

    def _flush_buffer(self):
        self._message_buffer = []
        self._buffer_size = 0
        self._last_sending = time.time()


def get_logger(
    region: str, access_key_id: str, secret_access_key: str, group: str, stream: str
) -> AwsCloudWatchLogger:
    try:
        session = get_session(access_key_id, secret_access_key, region)
        client = session.client('logs')
        create_group(client, group)
        create_stream(client, group, stream)
        return AwsCloudWatchLogger(client=client, group=group, stream=stream)
    except EndpointConnectionError as error:
        print(f'{error}\nCheck internet connection and aws-region')
    except CredentialsError:
        print('Invalid credentials')
    except InvalidRegionError:
        print('Invalid region')
    except ResourceError:
        print('Invalid group name')
