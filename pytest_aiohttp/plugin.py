from collections.abc import Awaitable, Iterator
from typing import (
    Any,
    Dict,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    overload,
)

import pytest
import pytest_asyncio
from aiohttp.test_utils import BaseTestServer, RawTestServer, TestClient, TestServer
from aiohttp.web import Application, BaseRequest, Request
from aiohttp.web_protocol import _RequestHandler

_Request = TypeVar("_Request", bound=BaseRequest)


class AiohttpClient(Protocol):
    @overload
    async def __call__(
        self,
        __param: Application,
        *,
        server_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> TestClient[Request, Application]: ...

    @overload
    async def __call__(
        self,
        __param: BaseTestServer,  # TODO(aiohttp4): BaseTestServer[_Request]
        *,
        server_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> TestClient[_Request, None]: ...


class AiohttpServer(Protocol):
    def __call__(
        self, app: Application, *, port: Optional[int] = None, **kwargs: Any
    ) -> Awaitable[TestServer]: ...


class AiohttpRawServer(Protocol):
    def __call__(
        self,
        handler: _RequestHandler,  # TODO(aiohttp4): _RequestHandler[BaseRequest]
        *,
        port: Optional[int] = None,
        **kwargs: Any,
    ) -> Awaitable[RawTestServer]: ...


LEGACY_MODE = DeprecationWarning(
    "The 'asyncio_mode' is 'legacy', switching to 'auto' for the sake of "
    "pytest-aiohttp backward compatibility. "
    "Please explicitly use 'asyncio_mode=strict' or 'asyncio_mode=auto' "
    "in pytest configuration file."
)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config) -> None:
    val = config.getoption("asyncio_mode")
    if val is None:
        val = config.getini("asyncio_mode")
    if val == "legacy":
        config.option.asyncio_mode = "auto"
        config.issue_config_time_warning(LEGACY_MODE, stacklevel=2)


@pytest_asyncio.fixture
async def aiohttp_server() -> Iterator[AiohttpServer]:
    """Factory to create a TestServer instance, given an app.

    aiohttp_server(app, **kwargs)
    """
    servers = []

    async def go(
        app: Application,
        *,
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        **kwargs: Any,
    ) -> TestServer:
        server = TestServer(app, host=host, port=port)
        await server.start_server(**kwargs)
        servers.append(server)
        return server

    yield go

    while servers:
        await servers.pop().close()


@pytest_asyncio.fixture
async def aiohttp_raw_server() -> Iterator[AiohttpRawServer]:
    """Factory to create a RawTestServer instance, given a web handler.

    aiohttp_raw_server(handler, **kwargs)
    """
    servers = []

    async def go(
        handler: _RequestHandler,  # TODO(aiohttp4): _RequestHandler[BaseRequest]
        *,
        port: Optional[int] = None,
        **kwargs: Any,
    ) -> RawTestServer:
        server = RawTestServer(handler, port=port)
        await server.start_server(**kwargs)
        servers.append(server)
        return server

    yield go

    while servers:
        await servers.pop().close()


@pytest_asyncio.fixture
def aiohttp_client_cls() -> Type[TestClient[Any, Any]]:
    """
    Client class to use in ``aiohttp_client`` factory.

    Use it for passing custom ``TestClient`` implementations.

    Example::

       class MyClient(TestClient):
           async def login(self, *, user, pw):
               payload = {"username": user, "password": pw}
               return await self.post("/login", json=payload)

       @pytest.fixture
       def aiohttp_client_cls():
           return MyClient

       def test_login(aiohttp_client):
           app = web.Application()
           client = await aiohttp_client(app)
           await client.login(user="admin", pw="s3cr3t")

    """
    return TestClient


@pytest_asyncio.fixture
async def aiohttp_client(
    aiohttp_client_cls: Type[TestClient[Any, Any]]
) -> Iterator[AiohttpClient]:
    """Factory to create a TestClient instance.

    aiohttp_client(app, **kwargs)
    aiohttp_client(server, **kwargs)
    aiohttp_client(raw_server, **kwargs)
    """
    clients = []

    @overload
    async def go(
        __param: Application,
        *,
        server_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> TestClient[Request, Application]: ...

    @overload
    async def go(
        __param: BaseTestServer,  # TODO(aiohttp4): BaseTestServer[_Request]
        *,
        server_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> TestClient[_Request, None]: ...

    async def go(
        __param: Union[
            Application, BaseTestServer
        ],  # TODO(aiohttp4): BaseTestServer[Any]
        *,
        server_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> TestClient[Any, Any]:
        if isinstance(__param, Application):
            server_kwargs = server_kwargs or {}
            server = TestServer(__param, **server_kwargs)
            client = aiohttp_client_cls(server, **kwargs)
        elif isinstance(__param, BaseTestServer):
            client = aiohttp_client_cls(__param, **kwargs)
        else:
            raise ValueError(f"Unknown argument type: {type(__param)!r}")

        await client.start_server()
        clients.append(client)
        return client

    yield go

    while clients:
        await clients.pop().close()
