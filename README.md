# sopel-cancelx

A Sopel plugin to cancel X links

## Project archival

> [!IMPORTANT]
> This plugin is unmaintained.

Nitter, XCancel, and probably others got legal notices from X Corp. in late August
2026. From XCancel's homepage:

> On Monday 24th August at 8PM EST, we received at letter from X Corp. asking to cease and desist the service XCancel.\
> The service XCancel is stopped until further notice.\
> We are seeking legal advice and won't share more details for now.\
> Thank you for the trust you have put in these two years of XCancel.

Since it no longer has an alternate front-end to point at, this plugin has been
archived on GitHub and PyPI. Open to resurrecting it if circumstances improve.
— 2026-08-26

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-cancelx
```

## Configuring

The easiest way to configure `sopel-cancelx` is via Sopel's configuration
wizard—simply run `sopel-plugins configure cancelx` and enter the values for
which it prompts you.

### `alternate_domains`

This is a list of alternate X/Twitter domains to cancel. By default it contains:

- `vxtwitter.com`
- `fixvx.com`
- `nitter.net`

You will need to include any of the default entries that you want to keep when
creating your own list using Sopel's config wizard or manually editing your
config file.

## Using

Post a link to Twitter and watch Sopel automatically provide a canceled version:

```
<dgw> https://x.com/i/status/2016567703478194406
<SopelTest> [X Cancelled] https://xcancel.com/i/status/2016567703478194406
<dgw> the link that started me down this path, vanquished!
```
