import json

import pytest

from services import image_processor


def test_image_processing(black_image, mock_channel_factory):
    expected_values = json.dumps({"image_path": black_image, "color": [0, 0, 0]})
    mock_channel = mock_channel_factory([expected_values])
    image_processor.process_image(None, None, None, black_image.encode(), mock_channel, None)
    assert mock_channel.expected_values == mock_channel.received_values


@pytest.fixture
def invalid_image_path(tmpdir):
    f = tmpdir.join("error.txt")
    f.write("content")
    return str(f).encode()
    

def test_invalid_image_path(invalid_image_path, mock_channel_factory):
    mock_channel = mock_channel_factory([])
    image_processor.process_image(None, None, None, invalid_image_path, None, None)
    assert mock_channel.expected_values == mock_channel.received_values
