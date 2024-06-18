import argparse
import functools
import json
import os
import shutil

import numpy as np
import pika

RGB_TO_COLOR_MAPPING = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}
DEFAULT_COLOR = "other"


# TODO: reduce the number of arguments so it can be easier to use for unit testing
def triage_images(ch, method, properties, body, dest_dir):
    try:
        data = json.loads(body)
        color_name = get_color_name(data["color"])
        save_image_to_directory(data["image_path"], color_name, dest_dir)
    except json.decoder.JSONDecodeError:
        print("WARNING: Image data cannot be read", flush=True)


def get_color_name(average_color):
    min_distance = float("inf")
    closest_color = DEFAULT_COLOR
    for color, value in RGB_TO_COLOR_MAPPING.items():
        distance = sum([(i - j) ** 2 for i, j in zip(average_color, value)])
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color


def save_image_to_directory(image_path, color_name, dest_dir):
    dest_dir = dest_dir.rstrip("/")
    target_directory = f"{dest_dir}/{color_name}_images"
    os.makedirs(target_directory, exist_ok=True)
    new_image_path = os.path.join(target_directory, os.path.basename(image_path))

    print(f"Copying image into '{new_image_path}'...", flush=True)
    shutil.copy(image_path, new_image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest-dir", help="A path to the directory where to triage images")
    parser.add_argument("--color-queue", help="A name of the color queue used in the MQ broker") 
    parser.add_argument("--host", help="A connection string to the MQ broker") 
 
    args = parser.parse_args() 

    connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))

    channel = connection.channel()
    channel.queue_declare(queue=args.color_queue)

    channel.basic_qos(prefetch_count=1)

    callback = functools.partial(triage_images, dest_dir=args.dest_dir)
    channel.basic_consume(queue=args.color_queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
