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
    replacement_domain = types.ValidatedAttribute(
        "replacement_domain",
        default="xcancel.com",
    )


def setup(bot):
    bot.settings.define_section("cancelx", CancelXSection)


def configure(settings):
    settings.define_section("cancelx", CancelXSection)
    settings.cancelx.configure_setting(
        'alternate_domains',
        'List of alternate X/Twitter domains to cancel (one per line).',
    )
    settings.cancelx.configure_setting(
        'replacement_domain',
        'The domain to use for cancelled X/Twitter links.',
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
            if f'//{re.escape(settings.cancelx.replacement_domain)}/' not in pattern
        ]

    return loader


def _cancel_x_link(url: str, replacement_domain: str = "xcancel.com") -> str:
    """Cancel a ``url`` (modify it to use ``xcancel.com``).

    Returns empty string if the URL is already cancelled.
    """
    parsed = urlparse(url)
    if parsed.hostname == replacement_domain:
        return ''  # Already cancelled

    if parsed.port:
        replacement_domain += f":{parsed.port}"
    return urlunparse(parsed._replace(scheme='https', netloc=replacement_domain))


@plugin.url_lazy(_twitter_alt_domains())
@plugin.url(DOMAIN_REGEX)
@plugin.output_prefix(OUTPUT_PREFIX)
def cancel_x_links(bot: bot.Sopel, trigger: trigger.Trigger):
    replacement_domain = bot.settings.cancelx.replacement_domain
    if canceled_link := _cancel_x_link(trigger.group(1), replacement_domain):
        bot.say(canceled_link)
