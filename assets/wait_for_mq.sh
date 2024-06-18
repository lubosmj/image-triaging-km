#!/bin/bash

# wait until the MQ is available for usage
while ! nc -z rabbitmq 5672; do sleep 3; done
