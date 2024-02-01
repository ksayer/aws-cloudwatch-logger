from services.aws.logger import get_logger
from services.container import run_container
from services.parse_args import parse_args


def main(
    image: str,
    region: str,
    access_key_id: str,
    secret_access_key: str,
    group: str,
    stream: str,
    bash_command: str,
):
    logger = get_logger(
        region=region,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        group=group,
        stream=stream,
    )
    if logger:
        run_container(image, bash_command, logger)


if __name__ == '__main__':
    args = parse_args()
    main(
        image=args.image,
        region=args.region,
        access_key_id=args.access_key,
        secret_access_key=args.secret_key,
        group=args.group,
        stream=args.stream,
        bash_command=args.bash_command,
    )
