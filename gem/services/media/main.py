from uuid import uuid4
from aiohttp import web

app = web.Application()


async def upload(request):
    data = await request.post()
    mp3 = data["file"]
    filename = str(uuid4()) + mp3.filename
    mp3_file = data["file"].file
    content = mp3_file.read()

    file = open("/usr/shared/downloads/"+filename, "wb")
    file.write(content)
    file.close()

    return web.json_response({"success": True, "path": filename})

if __name__ == "__main__":
    app.router.add_post("/upload", upload)
    web.run_app(app, port=8090)
