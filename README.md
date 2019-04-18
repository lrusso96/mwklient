<div align="center"><img src="docs/source/logo.svg" width="300"/></div>

# mwklient
[![Build Status](https://travis-ci.com/lrusso96/mwklient.svg?token=uoNxtXYBDHpqERGMiZA8&branch=master)](https://travis-ci.com/lrusso96/mwklient)

[![Test coverage][test-coverage-img]](https://coveralls.io/r/lrusso96/mwklient)
[![Latest version][latest-version-img]](https://pypi.python.org/pypi/mwklient)
[![MIT license][mit-license-img]](http://opensource.org/licenses/MIT)

[test-coverage-img]: https://img.shields.io/coveralls/lrusso96/mwklient.svg
[latest-version-img]: https://img.shields.io/pypi/v/mwklient.svg
[mit-license-img]: https://img.shields.io/github/license/lrusso96/mwklient.svg

mwklient (forked from [mwclient v0.9.3](https://github.com/mwclient/mwclient)) is a lightweight Python client library to the [MediaWiki API](https://mediawiki.org/wiki/API) which provides access to most API functionality.
It works with Python 3.5+ and supports MediaWiki API 1.16+,
for functions not available in the current MediaWiki, a `MediaWikiVersionError` is raised.

## mwklient and mwclient
The original project mwclient is still active and supports Python 2.7 too.
mwklient is forked from the version 0.9.3 of mwclient and wraps some more api_calls (see next section).
Moreover, it will support default error handlers for the most common calls (more details in next commits).
Finally, it has a MIT license as well as the original mwclient.

### List of new methods
* page.undo(), revert a given edit page

The current stable
[version 0.0.1](https://github.com/lrusso96/mwklient/archive/v0.0.1.zip)
is **not yet** [available through PyPI](https://pypi.python.org/pypi/mwklient):

```
$ pip install mwklient
```

The current [development version](https://github.com/lrusso96/mwklient) can be installed from GitHub:

```
$ pip install git+git://github.com/lrusso96/mwklient.git
```

## Documentation
[TODO]

For now, see [the original repo](https://github.com/mwclient/mwclient).

## Contributing
Patches and PR are welcome! Consider also contributing to the original repo.
