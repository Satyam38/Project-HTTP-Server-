import aiohttp
from aiohttp import web

async def get_data(request):
    n = request.query.get('n')
    m = request.query.get('m')
    if n:
        file_path = f'/tmp/data/{n}.txt'
        if m:
            return await get_file_line(file_path, int(m))
        else:
            return await get_file_content(file_path)
    else:
        return web.Response(text="File name not provided", status=400)

async def get_file_line(file_path, line_number):
    async with aiohttp.request('GET', file_path) as resp:
        if resp.status == 200:
            lines = await resp.content.readline()
            for _ in range(line_number - 1):
                lines = await resp.content.readline()
            return web.Response(body=lines)
        else:
            return web.Response(text="File not found", status=404)

async def get_file_content(file_path):
    async with aiohttp.request('GET', file_path) as resp:
        if resp.status == 200:
            return web.Response(body=await resp.content.read())
        else:
            return web.Response(text="File not found", status=404)

app = web.Application()
app.router.add_get('/data', get_data)

if __name__ == '__main__':
    web.run_app(app, port=8080)
