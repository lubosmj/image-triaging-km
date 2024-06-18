from services import image_reader


def test_directory_reading(tmpdir, mock_channel_factory):
    f1 = tmpdir.join("hello.jpeg")
    f1.write("content")

    f2 = tmpdir.join("mello.png")
    f2.write("content")

    f3 = tmpdir.join("error.txt")
    f3.write("content")

    mock_channel = mock_channel_factory([str(f1), str(f2)])

    image_reader.send_image_to_queue(
        str(tmpdir),
        image_queue=None,
        channel=mock_channel,
        repeat_indifinitely=False,
    )

    assert sorted(mock_channel.expected_values) == sorted(mock_channel.received_values)


def test_empty_directory(tmpdir, mock_channel_factory):
    mock_channel = mock_channel_factory([])

    image_reader.send_image_to_queue(
        str(tmpdir),
        image_queue=None,
        channel=mock_channel,
        repeat_indifinitely=False,
    )
    assert sorted(mock_channel.expected_values) == sorted(mock_channel.received_values)


def test_non_existing_directory(tmpdir, mock_channel_factory):
    mock_channel = mock_channel_factory([])

    image_reader.send_image_to_queue(
        str(tmpdir / "error"),
        image_queue=None,
        channel=mock_channel,
        repeat_indifinitely=False,
    )
    assert sorted(mock_channel.expected_values) == sorted(mock_channel.received_values)
