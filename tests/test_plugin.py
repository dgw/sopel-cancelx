"""Tests for ``cancelx`` Sopel plugin"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sopel.tests import rawlist

from sopel_cancelx.plugin import (
    DEFAULT_ALTERNATE_DOMAINS,
    DEFAULT_REPLACEMENT_DOMAIN,
    OUTPUT_PREFIX,
)

if TYPE_CHECKING:
    from sopel import bot
    from sopel.tests.factories import BotFactory, ConfigFactory


TMP_CONFIG = """
[core]
owner = testnick
nick = TestBot
enable = coretasks
"""


@pytest.fixture
def mockbot(configfactory: ConfigFactory) -> bot.Sopel:
    tmpconfig = configfactory('test.cfg', TMP_CONFIG)
    sopel = bot.Sopel(tmpconfig)
    return sopel


PRELOADED_CONFIG = """
[core]
owner = testnick
nick = TestBot
enable =
    coretasks
    url
"""


@pytest.fixture
def preloadedbot(configfactory: ConfigFactory, botfactory: BotFactory):
    tmpconfig = configfactory('preloaded.cfg', PRELOADED_CONFIG)
    return botfactory.preloaded(tmpconfig, ['cancelx'])


@pytest.mark.parametrize('prefix', (
    '',
    'wow ',
    'some fancy Unicode text 👀 ',
))
@pytest.mark.parametrize('suffix', (
    '',
    ' bro really',
    ' 💢💢💢',
))
@pytest.mark.parametrize('scheme', ('http', 'https'))
@pytest.mark.parametrize('domain', (
    'x.com',
    'twitter.com',
    *DEFAULT_ALTERNATE_DOMAINS,
))
@pytest.mark.parametrize('path', (
    'foo',
    'foo/status/12345',
    'i/status/67890',
))
@pytest.mark.parametrize('query', (
    '',
    '?s=20',
))
def test_irc_inputs(
    preloadedbot,
    prefix,
    scheme,
    domain,
    path,
    query,
    suffix,
):
    """Make sure links are canceled regardless of scheme, domain, path, or presence of query string."""
    line = f':Foo!foo@example.com PRIVMSG #test :{prefix}{scheme}://{domain}/{path}{query}{suffix}'
    preloadedbot.on_message(line)

    messages = preloadedbot.backend.message_sent
    assert len(messages) == 1
    assert messages == rawlist(
        f'PRIVMSG #test :{OUTPUT_PREFIX}https://{DEFAULT_REPLACEMENT_DOMAIN}/{path}{query}',
    )
