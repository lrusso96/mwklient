<div align="center"><img src="docs/source/logo.svg" width="300"/></div>

# mwclient
[![Build Status](https://travis-ci.com/lrusso96/mwklient.svg?token=uoNxtXYBDHpqERGMiZA8&branch=master)](https://travis-ci.com/lrusso96/mwklient)

[![Test coverage][test-coverage-img]](https://coveralls.io/r/mwclient/mwclient)
[![Latest version][latest-version-img]](https://pypi.python.org/pypi/mwclient)
[![MIT license][mit-license-img]](http://opensource.org/licenses/MIT)
[![Documentation status][documentation-status-img]](http://mwclient.readthedocs.io/en/latest/)

[test-coverage-img]: https://img.shields.io/coveralls/mwclient/mwclient.svg
[latest-version-img]: https://img.shields.io/pypi/v/mwclient.svg
[mit-license-img]: https://img.shields.io/github/license/mwclient/mwclient.svg
[documentation-status-img]: https://readthedocs.org/projects/mwclient/badge/

mwclient is a lightweight Python client library to the
[MediaWiki API](https://mediawiki.org/wiki/API)
which provides access to most API functionality.
It works with Python 2.7 as well as 3.5 and above,
and supports MediaWiki 1.16 and above.
For functions not available in the current MediaWiki,
a `MediaWikiVersionError` is raised.

The current stable
[version 0.9.3](https://github.com/mwclient/mwclient/archive/v0.9.3.zip)
is [available through PyPI](https://pypi.python.org/pypi/mwclient):

```
$ pip install mwclient
```

The current [development version](https://github.com/mwclient/mwclient)
can be installed from GitHub:

```
$ pip install git+git://github.com/mwclient/mwclient.git
```

Please see the [changelog
document](https://github.com/mwclient/mwclient/blob/master/CHANGELOG.md)
for a list of changes.

## Documentation

Up-to-date documentation is hosted [at Read the Docs](http://mwclient.readthedocs.io/en/latest/).
It includes a user guide to get started using mwclient, a reference guide,
implementation and development notes.

There is also some documentation on the [GitHub wiki](https://github.com/mwclient/mwclient/wiki)
that hasn't been ported yet.
If you want to help, you're welcome!

## Contributing

Patches are welcome! See [this page](https://mwclient.readthedocs.io/en/latest/development/)
for information on how to get started with mwclient development.