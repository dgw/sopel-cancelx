"""sopel-cancelx

A Sopel plugin to cancel X links
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse

from sopel import config, plugin
from sopel.config import types


if TYPE_CHECKING:
    from sopel import bot, trigger


DOMAIN_REGEX = r"(?P<url>https?://(?:(?:www|m(?:obile)?)\.)?(?:twitter|x)\.com/\S+)"
OUTPUT_PREFIX = '[X Cancelled] '


class CancelXSection(types.StaticSection):
    alternate_domains = types.ListAttribute(
        "alternate_domains",
        default=["vxtwitter.com", "fixvx.com", "nitter.net"],
    )


def setup(bot):
    bot.settings.define_section("cancelx", CancelXSection)


def configure(settings):
    settings.define_section("cancelx", CancelXSection)
    settings.cancelx.configure_setting(
        'alternate_domains',
        'List of alternate X/Twitter domains to cancel (one per line).',
    )


def _twitter_alt_domains():
    """Build a url_lazy loader for the specified callback type.

    :param str path_regex: The path to be appended to each domain regex
    :return: A loader to be called by url_lazy()
    :rtype: Callable[[Config], List[re.Pattern]]
    """
    def loader(settings: config.Config):
        """Lazy loader for configured alt domains

        :param settings: bot.config
        :type settings: :class:`~sopel.config.Config`
        :return: A list of compiled regexes
        :rtype: List[re.Pattern]
        """
        # Use a set to mitigate duplicate entries
        patterns = set()
        for domain in settings.cancelx.alternate_domains:
            patterns.add(r"(?P<url>https?://{}/\S+)".format(re.escape(domain)))

        return [
            re.compile(pattern) for pattern in patterns
            if '//xcancel.com/' not in pattern
        ]

    return loader


def _cancel_x_link(url: str) -> str:
    """Cancel a ``url`` (modify it to use ``xcancel.com``).

    Returns empty string if the URL is already cancelled.
    """
    parsed = urlparse(url)
    if parsed.hostname == 'xcancel.com':
        return ''  # Already cancelled

    canceled_netloc = 'xcancel.com'
    if parsed.port:
        canceled_netloc += f":{parsed.port}"
    return urlunparse(parsed._replace(scheme='https', netloc=canceled_netloc))


@plugin.url_lazy(_twitter_alt_domains())
@plugin.url(DOMAIN_REGEX)
@plugin.output_prefix(OUTPUT_PREFIX)
def cancel_x_links(bot: bot.Sopel, trigger: trigger.Trigger):
    if canceled_link := _cancel_x_link(trigger.group(1)):
        bot.say(canceled_link)
