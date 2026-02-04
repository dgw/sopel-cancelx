"""Tests for ``cancelx`` Sopel plugin

Adapted from sopel-url <https://github.com/sopel-irc/sopel-url/blob/631036dbdbd1ddeb483b90a9067f2b33198e9467/tests/test_plugin.py>.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sopel.tests import rawlist

from sopel_cancelx import plugin as cancelx_plugin

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


def test_basic_cancel():
    url = 'https://x.com/melonhusk'
    assert cancelx_plugin._cancel_x_link(url) == 'https://xcancel.com/melonhusk'


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
@pytest.mark.parametrize('irc_input, result', (
    ('https://x.com/foo/status/12345', 'https://xcancel.com/foo/status/12345'),
    ('http://twitter.com/bar', 'https://xcancel.com/bar'),
    ('https://vxtwitter.com/baz', 'https://xcancel.com/baz'),
    ('https://fixvx.com/i/status/67890', 'https://xcancel.com/i/status/67890'),
    ('https://nitter.net/quux', 'https://xcancel.com/quux'),
))
def test_irc_inputs(
    preloadedbot,
    prefix,
    irc_input,
    suffix,
    result,
):
    """Make sure the urlban command privilege check functions correctly."""
    line = f':Foo!foo@example.com PRIVMSG #test :{prefix}{irc_input}{suffix}'
    preloadedbot.on_message(line)

    messages = preloadedbot.backend.message_sent
    assert len(messages) == 1
    assert messages == rawlist(
        f'PRIVMSG #test :{cancelx_plugin.OUTPUT_PREFIX}{result}',
    )
