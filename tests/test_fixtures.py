import pytest

pytest_plugins = "pytester"


def test_aiohttp_plugin(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """\
import pytest
from unittest import mock

from aiohttp import web

value = web.AppKey('value', str)


async def hello(request):
    return web.Response(body=b'Hello, world')


async def create_app():
    app = web.Application()
    app.router.add_route('GET', '/', hello)
    return app


async def test_hello(aiohttp_client) -> None:
    client = await aiohttp_client(await create_app())
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text


async def test_hello_from_app(aiohttp_client) -> None:
    app = web.Application()
    app.router.add_get('/', hello)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text


async def test_hello_with_loop(aiohttp_client) -> None:
    client = await aiohttp_client(await create_app())
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text


async def test_noop() -> None:
    pass


async def previous(request):
    if request.method == 'POST':
        with pytest.deprecated_call():  # FIXME: this isn't actually called
            request.app[value] = (await request.post())['value']
        return web.Response(body=b'thanks for the data')
    else:
        v = request.app.get(value, 'unknown')
        return web.Response(body='value: {}'.format(v).encode())


def create_stateful_app():
    app = web.Application()
    app.router.add_route('*', '/', previous)
    return app


@pytest.fixture
async def cli(aiohttp_client):
    return await aiohttp_client(create_stateful_app())


def test_noncoro() -> None:
    assert True


async def test_failed_to_create_client(aiohttp_client) -> None:

    def make_app():
        raise RuntimeError()

    with pytest.raises(RuntimeError):
        await aiohttp_client(make_app())


async def test_custom_port_aiohttp_client(aiohttp_client, unused_tcp_port):
    client = await aiohttp_client(await create_app(),
                                  server_kwargs={'port': unused_tcp_port})
    assert client.port == unused_tcp_port
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text


async def test_custom_port_test_server(aiohttp_server, unused_tcp_port):
    app = await create_app()
    server = await aiohttp_server(app, port=unused_tcp_port)
    assert server.port == unused_tcp_port
"""
    )
    result = testdir.runpytest("--asyncio-mode=auto")
    result.assert_outcomes(passed=8)


def test_aiohttp_raw_server(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """\
import pytest

from aiohttp import web


async def handler(request):
    return web.Response(text="OK")


@pytest.fixture
async def server(aiohttp_raw_server):
    return await aiohttp_raw_server(handler)


@pytest.fixture
async def cli(aiohttp_client, server):
    client = await aiohttp_client(server)
    return client


async def test_hello(cli) -> None:
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'OK' in text
"""
    )
    result = testdir.runpytest("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)


def test_aiohttp_client_cls_fixture_custom_client_used(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
import pytest
from aiohttp.web import Application
from aiohttp.test_utils import TestClient


class CustomClient(TestClient):
    pass


@pytest.fixture
def aiohttp_client_cls():
    return CustomClient


async def test_hello(aiohttp_client) -> None:
    client = await aiohttp_client(Application())
    assert isinstance(client, CustomClient)

"""
    )
    result = testdir.runpytest("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)


def test_aiohttp_client_cls_fixture_factory(testdir: pytest.Testdir) -> None:
    testdir.makeconftest(
        """\

def pytest_configure(config):
    config.addinivalue_line("markers", "rest: RESTful API tests")
    config.addinivalue_line("markers", "graphql: GraphQL API tests")

"""
    )
    testdir.makepyfile(
        """
import pytest
from aiohttp.web import Application
from aiohttp.test_utils import TestClient


class RESTfulClient(TestClient):
    pass


class GraphQLClient(TestClient):
    pass


@pytest.fixture
def aiohttp_client_cls(request):
    if request.node.get_closest_marker('rest') is not None:
        return RESTfulClient
    elif request.node.get_closest_marker('graphql') is not None:
        return GraphQLClient
    return TestClient


@pytest.mark.rest
async def test_rest(aiohttp_client) -> None:
    client = await aiohttp_client(Application())
    assert isinstance(client, RESTfulClient)


@pytest.mark.graphql
async def test_graphql(aiohttp_client) -> None:
    client = await aiohttp_client(Application())
    assert isinstance(client, GraphQLClient)

"""
    )
    result = testdir.runpytest("--asyncio-mode=auto")
    result.assert_outcomes(passed=2)
