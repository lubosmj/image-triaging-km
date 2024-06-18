import argparse
import os
import sys
import time

import pika

READ_INTERVAL = 60
IMAGE_TYPES = (".jpg", "jpeg", ".png")


def send_image_to_queue(source_dir, image_queue, channel, repeat_indifinitely=True):
    for image_path in read_directory(source_dir, repeat_indifinitely):
        print(f"Publishing image '{image_path}'...", flush=True)
        channel.basic_publish(exchange='', routing_key=image_queue, body=image_path)


def read_directory(source_dir, repeat_indefinitely=True):
    if not os.path.exists(source_dir):
        print(f"WARNING: Directory '{source_dir}' does not exist", flush=True)
        return

    while True:
        for filename in os.listdir(source_dir):
            if filename.lower().endswith(IMAGE_TYPES):
                image_path = os.path.join(source_dir, filename)
                yield image_path

        if not repeat_indefinitely:
            break
        else:
            time.sleep(READ_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", help="A path to the directory to read images from")
    parser.add_argument("--image-queue", help="A name of the queue used in the MQ broker")
    parser.add_argument("--host", help="A connection string to the MQ broker")

    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))

    channel = connection.channel()
    channel.queue_declare(queue=args.image_queue)

    send_image_to_queue(args.source_dir, args.image_queue, channel)
