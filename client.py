import time
from typing import Iterator

import requests


SERVER_URL = "localhost:8000"


MAX_CHUNK_SIZE = 10

# Stream data from streaming endpoint
with requests.get(f"http://{SERVER_URL}/bigfile-stream", stream=True) as response:
    with open("downloaded-file-stream.txt", "wb") as f_write:
        # Note: chunk_size param jus specifies max. We might get less per iteration if server sends less
        # Each chunk here in the loop is the size of the server block wize which is < CHUNK_SIZE
        for chunk in response.iter_content(chunk_size=MAX_CHUNK_SIZE):
            print(chunk)
            f_write.write(chunk)


# Note: Even if server is streaming, you can just get it all like this if you don't mind the
# full response size.
with requests.get(f"http://{SERVER_URL}/bigfile-stream", stream=False) as response:
    d = response.content
    print(d)


with requests.get(f"http://{SERVER_URL}/stream-user-csv", stream=False) as response:
    d = response.content
    print(d)


def endless_data() -> Iterator[bytes]:
    print("Uploading endless data")
    i = 0
    while True:
        yield f"chunk-{i}\n".encode()
        i += 1
        time.sleep(1)


# Endless upload stream
requests.post("http://localhost:8000/endless-upload", data=endless_data())
