import argparse
from dataclasses import dataclass


@dataclass
class Args:
    image: str
    bash_command: str
    group: str
    stream: str
    access_key: str
    secret_key: str
    region: str


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--docker-image', required=True)
    parser.add_argument('--bash-command', required=True)
    parser.add_argument('--aws-cloudwatch-group', required=True)
    parser.add_argument('--aws-cloudwatch-stream', required=True)
    parser.add_argument('--aws-access-key-id', required=True)
    parser.add_argument('--aws-secret-access-key', required=True)
    parser.add_argument('--aws-region', required=True)
    args = parser.parse_args()
    return Args(
        image=args.docker_image,
        bash_command=args.bash_command,
        group=args.aws_cloudwatch_group,
        stream=args.aws_cloudwatch_stream,
        access_key=args.aws_access_key_id,
        secret_key=args.aws_secret_access_key,
        region=args.aws_region,
    )
