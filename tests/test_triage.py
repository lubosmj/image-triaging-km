import json

import pytest

from pathlib import Path

from services import image_triager


@pytest.mark.parametrize(
    "image_path, dir_name, rgb_color",
    [("black_image", "black_images", [0, 0, 0]), ("green_image", "green_images", [50, 205, 50])],
    ids=["black_image", "green_image"]
)
def test_image_triaging(tmpdir, image_path, dir_name, rgb_color, request):
    image_path = request.getfixturevalue(image_path)
    image_data = json.dumps({"image_path": image_path, "color": rgb_color})
    image_triager.triage_images(None, None, None, image_data, str(tmpdir))

    new_image_path = tmpdir / dir_name / Path(image_path).name
    assert Path(image_path).exists()
    assert Path(new_image_path).exists()


def test_invalid_image_data():
    image_triager.triage_images(None, None, None, "error", None)
