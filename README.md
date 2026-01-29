# sopel-cancelx

A Sopel plugin to cancel X links

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
