from os.path import join
from uuid import uuid4
from aiohttp import web

app = web.Application()


async def upload(request):
    data = await request.post()
    mp3 = data["file"]
    filename = str(uuid4()) + mp3.filename
    mp3_file = data["file"].file
    content = mp3_file.read()

    # save file content
    full_path = join("/", "usr", "shared", "media", filename)
    with open(full_path, "wb") as file:
        file.write(content)

    # response
    return web.json_response({"success": True, "path": filename})

if __name__ == "__main__":
    app.router.add_post("/upload", upload)
    web.run_app(app, port=8090)
