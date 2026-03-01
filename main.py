# Run with fastapi dev main.py
from typing import Iterator

from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/bigfile-disk")
async def bigfile_disk():
    # Built in file streaming.
    # This works well if you can reference the file on disk directly. Not realistic these days.
    return FileResponse(
        "bigfile.txt",
        # media_type helps client interpret content. Doesn't change data returned.
        media_type="text/plain",
        filename="bigfile.txt",
    )


# Download in browser: localhost:8000/bigfile-memory
# Curl works too: curl -OJ localhost:8000/bigfile-memory
@app.get("/bigfile-memory")
async def bigfile_memory():
    # The shitty way to do it. Imagine reading this from remote server into memory.
    file_bytes = (
        b"Hello, this is an in-memory file!\nSecond line.\nI am a huge file this is bad"
    )
    return Response(
        content=file_bytes,
        media_type="text/plain",
        headers={
            "Content-Disposition": 'attachment; filename="downloaded-file-memory.txt"'
        },
    )


BLOCK_SIZE = 2


def file_iterator(file_path: str) -> Iterator[bytes]:
    # Recall that functions with yield need to include the "loop".
    # Unlike __next__ which just returns one iteration.
    with open(file_path, "rb") as f:
        while data := f.read(BLOCK_SIZE):
            # data = f.read(BLOCK_SIZE)
            yield data


@app.get("/bigfile-stream")
async def bigfile_stream():
    fi = file_iterator("bigfile.txt")
    return StreamingResponse(content=fi, media_type="text/plain")


# TODO with websocket
# @app.get("/chat")
# async def chat():
#     return {"message": "Hello World"}
