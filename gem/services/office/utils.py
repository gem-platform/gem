from io import BytesIO
from os.path import join
from uuid import uuid4
from requests import post


def print_and_save(content):
    """Render specified content to PDF and save to file."""
    # make a request to print PDF using specified content
    stream = BytesIO(content.encode())
    request = post(
        "http://pdf-printer:4999/pdf",
        files={"file": stream})

    # get filename
    filename = str(uuid4()) + ".pdf"
    full_path = join("/", "usr", "shared", "media", filename)

    # write response to file
    with open(full_path, "wb") as file:
        file.write(request.content)

    # return path to file
    return filename
