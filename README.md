# Simple Image Triaging Tool

A utility for triaging images based on their average/mean color. It consists of three microservices
operating on their own. The first one reads the images specified in a source directory. The second
one calculates the average/mean color of the images. Finally, the third one copies the parsed images
to a destination directory.

Run the services and define the source and destination directory for mounted volumes:
```
$ sudo HOST_SOURCE_DIR=/home/user/Downloads/ HOST_DEST_DIR=/home/user/Workplace/ docker compose up --build
```

Additionally, use `--force-recreate` or `--remove-orphans` to enforce clean startup.

### Note

The utility runs RabbitMQ along with the three microservices in the docker-compose format. Users
are allowed to override default values for the source and destination directory inside the containers.
Visit `.env` file to see which environment values can be modified and consult [docker-compose documentation](https://docs.docker.com/compose/environment-variables/set-environment-variables/#set-environment-variables-with-docker-compose-run---env) to learn more.

### Running Tests

First, download required packages and execute the pytest utility, like so:
```
python -m venv venv
source venv/bin/activate

python -m pip install -r tests/test_requirements.txt

python -m pytest -vv tests
```
