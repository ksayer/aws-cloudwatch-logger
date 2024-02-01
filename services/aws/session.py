import boto3
from boto3 import Session
from botocore.exceptions import ClientError, NoCredentialsError


class CredentialsError(BaseException):
    ...


def get_session(access_key: str, secret_key: str, region: str) -> Session:
    session = boto3.session.Session(
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    validate_credentials(session)
    return session


def validate_credentials(session: Session):
    try:
        sts = session.client("sts")
        sts.get_caller_identity()
    except (ClientError, NoCredentialsError):
        raise CredentialsError('Invalid Credentials')
