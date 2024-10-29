import pytest

from pytest_aiohttp.plugin import LEGACY_MODE

pytest_plugins: str = "pytester"


def test_warning_for_legacy_mode(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """\
async def test_a():
    pass

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=legacy")
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(["*" + str(LEGACY_MODE) + "*"])


def test_auto_mode(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """\
async def test_a():
    pass

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=auto")
    result.assert_outcomes(passed=1)
    result.stdout.no_fnmatch_line("*" + str(LEGACY_MODE) + "*")


def test_strict_mode(testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """\
import pytest


@pytest.mark.asyncio
async def test_a():
    pass

"""
    )
    result = testdir.runpytest_subprocess("--asyncio-mode=strict")
    result.assert_outcomes(passed=1)
    result.stdout.no_fnmatch_line("*" + str(LEGACY_MODE) + "*")
