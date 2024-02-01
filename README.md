# AWS logger for any docker image

### Functionality
- The program creates a Docker container using the given Docker image name, and
the given bash command
- The program handles the output logs of the container and send them to the given
AWS CloudWatch group/stream using the given AWS credentials. If the corresponding
AWS CloudWatch group or stream does not exist, it creates it using the given
AWS credentials.

### Usage
If you use poetry:

    - poetry install

    - poetry run python main.py ...

else:

    - install virtualenv with python ^3.11

    - pip install -r requirements.txt

    - python main.py ...

#### Arguments
```
--docker-image - A name of a Docker image
--bash-command - A bash command (to run inside the Docker image)
--aws-cloudwatch-group - A name of an AWS CloudWatch group
--aws-cloudwatch-stream - A name of an AWS CloudWatch stream
--aws-access-key-id - AWS Acces key id
--aws-secret-access-key - AWS secret access key
--aws-region - A name of an AWS region
```

#### Example:
`python main.py --docker-image python --bash-command $'pip install pip pip install tqdm && python -c \"import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"' --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 --aws-access-key-id ... --aws-secret-access-key ... --aws-region ...`

#### Settings

You can configure logger behaviour by .env file

SEND_INTERVAL =  interval between sending butch to the cloud (seconds). default=60

EVENT_LIMIT_SIZE = maximum log size (bytes). default=100kB. (The logger divides large message into small ones if necessary)

BUTCH_LIMIT_SIZE = maximum log butch size (single request, bytes). default=10MB

MAXIMUM_NUMBER_EVENTS = max number logs in a request. default=1000