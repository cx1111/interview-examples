# Run with fastapi dev main.py
from dataclasses import dataclass
from typing import Iterator

from fastapi import FastAPI, Request, Response
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
            yield data


@app.get("/bigfile-stream")
async def bigfile_stream():
    # The good solution for streaming content to the client.
    fi = file_iterator("bigfile.txt")
    return StreamingResponse(content=fi, media_type="text/plain")


@dataclass
class User:
    user_id: int
    email: str


def get_user(user_id: int) -> User:
    # Fake DB query
    return User(user_id=user_id, email=f"user-{user_id}@gmail.com")


def get_users(user_ids: list[int]) -> list[User]:
    # Fake batch DB query
    return [
        User(user_id=user_id, email=f"user-{user_id}@gmail.com") for user_id in user_ids
    ]


@app.get("/stream-user-csv")
async def stream_user_csv():
    yield "user_id,email"

    # This is a huge table with 20k users
    # Getting one row at a time - many queries
    for user_id in range(10):
        user = get_user(user_id=user_id)
        yield f"{user.user_id},{user.email}"

    # Getting 100 rows at a time in batched queries


@app.post("/endless-upload")
async def endless_upload(request: Request):
    async for chunk in request.stream():
        print(chunk)


# TODO with websocket
# @app.get("/chat")
# async def chat():
#     return {"message": "Hello World"}
