pytest-aiohttp
==============

pytest plugin for aiohttp support

The library allows to use [aiohttp pytest
pugin](http://aiohttp.readthedocs.io/en/stable/testing.html#pytest-example)
without need for implicitly loading it like `pytest_plugins =
'aiohttp.pytest_plugin'`.


Just run:

    $ pip install pytest-aiohttp

and write tests with the plugin support:

    from aiohttp import web

    async def hello(request):
        return web.Response(body=b'Hello, world')

    def create_app(loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', hello)
        return app

    async def test_hello(test_client):
        client = await test_client(create_app)
        resp = await client.get('/')
        assert resp.status == 200
        text = await resp.text()
        assert 'Hello, world' in text
