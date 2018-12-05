from io import BytesIO
from uuid import uuid4
from requests import post


def print_and_save(content):
    stream = BytesIO(content.encode())
    files = {"file": stream}
    req = post("http://pdf-printer:4999/pdf", files=files)
    filename = str(uuid4()) + ".pdf"
    w = open("/usr/shared/downloads/" + filename, "wb")
    w.write(req.content)
    w.close()
    return filename
