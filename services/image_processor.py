import argparse
import functools
import json

import pika
import numpy as np

from PIL import Image, UnidentifiedImageError

# temporarily disable DecompressionBombWarning raised when parsing larger images
Image.MAX_IMAGE_PIXELS = None


# TODO: reduce the number of arguments so it can be easier to use for unit testing
def process_image(ch, method, properties, body, color_channel, routing):
    image_path = body.decode()
    try:
        average_color = compute_average_color(image_path)
    except UnidentifiedImageError:
        print(f"WARNING: Image '{image_path}' cannot be read", flush=True)
        return
    send_color_to_queue(image_path, average_color, color_channel, routing)


def compute_average_color(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    average_color = np.mean(pixels, axis=(0, 1))
    return np.int64(average_color).tolist()


def send_color_to_queue(image_path, average_color, color_channel, routing_key):
    print(f"Publishing image '{image_path}' with RGB '{average_color}'...", flush=True)
    message = json.dumps({"image_path": image_path, "color": average_color})
    # TODO: add the persistent delivery mode
    color_channel.basic_publish(exchange='', routing_key=routing_key, body=message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-queue", help="A name of the image queue used in the MQ broker")
    parser.add_argument("--color-queue", help="A name of the color queue used in the MQ broker")
    parser.add_argument("--host", help="A connection string to the MQ broker")

    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))

    image_channel = connection.channel()
    image_channel.queue_declare(queue=args.image_queue)

    color_channel = connection.channel()
    # TODO: make the queue durable to node restarting
    color_channel.queue_declare(queue=args.color_queue)

    image_channel.basic_qos(prefetch_count=1)

    callback = functools.partial(process_image, color_channel=color_channel, routing=args.color_queue)
    image_channel.basic_consume(queue=args.image_queue, on_message_callback=callback, auto_ack=True)
    image_channel.start_consuming()
