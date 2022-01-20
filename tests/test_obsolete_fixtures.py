from typing import Any

pytest_plugins: str = "pytester"


def test_loop_fixture(testdir: Any) -> None:
    testdir.makepyfile(
        """\
async def test_a(loop):
    pass

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(
        [
            "*DeprecationWarning: 'loop' fixture is deprecated "
            "and scheduled for removal, "
            "please use 'event_loop' instead*"
        ]
    )


def test_proactor_loop_fixture(testdir: Any) -> None:
    testdir.makepyfile(
        """\
async def test_a(proactor_loop):
    pass

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(
        [
            "*DeprecationWarning: 'proactor_loop' fixture is deprecated "
            "and scheduled for removal, "
            "please use 'event_loop' instead*"
        ]
    )


def test_aiohttp_unused_port(testdir: Any) -> None:
    testdir.makepyfile(
        """\
async def test_a(aiohttp_unused_port):
    aiohttp_unused_port()

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(
        [
            "*DeprecationWarning: 'aiohttp_unused_port' fixture is deprecated "
            "and scheduled for removal, "
            "please use 'unused_tcp_port_factory' instead*"
        ]
    )
