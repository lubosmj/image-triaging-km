import pytest

import numpy as np

from PIL import Image


class MockChannel:
    def __init__(self, expected_values):
        self.expected_values = expected_values
        self.received_values = []

    def basic_publish(self, exchange, routing_key, body):
        self.received_values.append(body)


@pytest.fixture
def mock_channel_factory():
    def _mock_channel_factory(expected_values):
        return MockChannel(expected_values)

    return _mock_channel_factory


@pytest.fixture
def black_image(tmpdir):
    image_path = str(tmpdir.join("black_image.png"))
    image = Image.fromarray(np.zeros((10, 10)).astype('uint8')).convert('RGB')
    image.save(image_path)
    return image_path


@pytest.fixture
def green_image(tmpdir):
    image_path = str(tmpdir.join("green_image.png"))
    image = Image.fromarray(np.array((50,205,50)).astype('uint8')).convert('RGB')
    image.save(image_path)
    return image_path
