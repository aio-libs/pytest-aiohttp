CHANGES
=======

1.1.0 (2025-01-23)
------------------

- Drop Python 3.8 (#57)

- Export the plugin types at top-level (#60, #61)

- Add host parameter to aiohttp_server fixture (#63)

1.0.5 (2023-09-06)
------------------

- Fix some compatibility with Pytest 7.

1.0.4 (2022-02-12)
------------------

- Fix failure with ``aiohttp_client`` fixture usage when ``asyncio_mode=strict``.
  `#25 <https://github.com/aio-libs/pytest-aiohttp/issue/25>`_

1.0.3 (2022-01-03)
------------------

- Fix ``loop`` and ``proactor_loop`` fixtures.
  `#22 <https://github.com/aio-libs/pytest-aiohttp/issue/22>`_

1.0.2 (2022-01-20)
------------------

- Restore implicit switch to ``asyncio_mode = auto`` if *legacy* mode is detected.

1.0.1 (2022-01-20)
------------------

- Don't implicitly switch from legacy to auto asyncio_mode, the integration doesn't work
  well.

1.0.0 (2022-1-20)
------------------

- The plugin is compatible with ``pytest-asyncio`` now.  It uses ``pytest-asyncio`` for
  async tests running and async fixtures support, providing by itself only fixtures for
  creating aiohttp test server and client.

0.2.0 (2017-11-30)
------------------

- Fix backward incompatibility changes introduced by `pytest` 3.3+

0.1.3 (2016-09-08)
------------------

- Add MANIFEST.in file

0.1.2 (2016-08-07)
------------------

- Fix README markup

0.1.1 (2016-07-22)
------------------

- Fix an url in setup.py

0.1.0 (2016-07-22)
------------------

- Initial release
