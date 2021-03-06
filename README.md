# mwklient

[![Build Status](https://travis-ci.com/lrusso96/mwklient.svg?token=uoNxtXYBDHpqERGMiZA8&branch=master)](https://travis-ci.com/lrusso96/mwklient)
![License: MIT](https://img.shields.io/github/license/lrusso96/mwklient.svg?color=blue)

[![Test Coverage](https://img.shields.io/coveralls/github/lrusso96/mwklient.svg)](https://coveralls.io/github/lrusso96/mwklient)
[![Latest Version](https://img.shields.io/pypi/v/mwklient.svg)](https://pypi.org/project/mwklient)
![Python Version](https://img.shields.io/pypi/pyversions/mwklient.svg)
[![Doc Status](https://readthedocs.org/projects/mwklient/badge/?version=latest)](https://mwklient.readthedocs.io/en/latest/?badge=latest)

mwklient (forked from [mwclient v0.9.3](https://github.com/mwclient/mwclient)) is a lightweight Python client library to the [MediaWiki API](https://mediawiki.org/wiki/API) which provides access to most API functionality.
It works with Python 3.5+ and supports MediaWiki API 1.16+,
for functions not available in the current MediaWiki, a `MediaWikiVersionError` is raised.

## mwklient vs mwclient

The original project mwclient is still active and supports Python 2.7 too.
mwklient is forked from the version 0.9.3 of mwclient and wraps some more api_calls (see next section).
Moreover, it will support default error handlers for the most common calls (more details in next commits).
Finally, it has a MIT license as well as the original mwclient.

### List of new methods

* page.undo(), revert a given edit page

## Installation

The current stable [version 0.1.0](https://github.com/lrusso96/mwklient/archive/v0.1.0.zip)
is [available through PyPI](https://pypi.python.org/pypi/mwklient):

```bash
pip install mwklient
```

## Documentation

Up-to-date documentation is hosted [at Read the Docs](http://mwklient.readthedocs.io/en/latest/).
It includes a user guide to get started using mwklient, a reference guide, implementation and development notes.

## Contributing

Patches and PR are welcome! Consider also contributing to the original repo.
The current [development version](https://github.com/lrusso96/mwklient) can be
easily installed from GitHub, simply cloning the repo:

```bash
git clone https://github.com/lrusso96/mwklient.git
```

In order to test your edits, build an *editable* version with the command:

```bash
pip install -e .
```

Finally, if you want to run tests, do

```bash
python setup.py test
```
