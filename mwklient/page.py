import time
import six
from six import text_type
from mwklient.util import strip_namespace, parse_timestamp
import mwklient.listing
import mwklient.errors


class Page():
    def __init__(self, site, name, info=None, extra_properties=None):
        if type(name) is type(self):
            self.__dict__.update(name.__dict__)
            return
        self.site = site
        self.name = name
        self._textcache = {}

        if not info:
            if extra_properties:
                prop = 'info|' + '|'.join(six.iterkeys(extra_properties))
                extra_props = []
                for extra_prop in six.itervalues(extra_properties):
                    extra_props.extend(extra_prop)
            else:
                prop = 'info'
                extra_props = ()

            if isinstance(name, int):
                info = self.site.get(
                    'query',
                    prop=prop,
                    pageids=name,
                    inprop='protection',
                    *extra_props)
            else:
                info = self.site.get(
                    'query',
                    prop=prop,
                    titles=name,
                    inprop='protection',
                    *extra_props)
            info = six.next(six.itervalues(info['query']['pages']))
        self._info = info

        if 'invalid' in info:
            raise mwklient.errors.InvalidPageTitle(info.get('invalidreason'))

        self.namespace = info.get('ns', 0)
        self.name = info.get('title', u'')
        if self.namespace:
            self.page_title = strip_namespace(self.name)
        else:
            self.page_title = self.name

        self.touched = parse_timestamp(info.get('touched'))
        self.revision = info.get('lastrevid', 0)
        self.exists = 'missing' not in info
        self.length = info.get('length')
        self.protection = {
            i['type']: (i['level'], i['expiry'])
            for i in info.get('protection', ()) if i
        }
        self.redirect = 'redirect' in info
        self.pageid = info.get('pageid', None)
        self.contentmodel = info.get('contentmodel', None)
        self.pagelanguage = info.get('pagelanguage', None)
        self.restrictiontypes = info.get('restrictiontypes', None)

        self.last_rev_time = None
        self.edit_time = None

    def redirects_to(self):
        """ Returns the redirect target page, or None if the page is not a
        redirect page."""
        info = self.site.get(
            'query', prop='pageprops', titles=self.name, redirects='')['query']
        if 'redirects' in info:
            for page in info['redirects']:
                if page['from'] == self.name:
                    return Page(self.site, page['to'])
        return None

    def resolve_redirect(self):
        """ Returns the redirect target page, or the current page if it's not a
        redirect page."""
        target_page = self.redirects_to()
        if target_page is None:
            return self
        return target_page

    def __repr__(self):
        return "<Page object '%s' for %s>" % (self.name.encode('utf-8'),
                                              self.site)

    def __unicode__(self):
        return self.name

    def can(self, action):
        """Check if the current user has the right to carry out some action
        with the current page.

        Example:
            >>> page.can('edit')
            True

        """
        level = self.protection.get(action, (action, ))[0]
        if level == 'sysop':
            level = 'editprotected'

        return level in self.site.rights

    def __get_token__(self, type_t, force=False):
        return self.site.get_token(type_t, force, title=self.name)

    def text(self,
             section=None,
             expandtemplates=False,
             cache=True,
             slot='main'):
        """Get the current wikitext of the page, or of a specific section.

        If the page does not exist, an empty string is returned. By
        default, results will be cached and if you call text() again
        with the same section and expandtemplates the result will come
        from the cache. The cache is stored on the instance, so it
        lives as long as the instance does.

        Args:
            section (int): numbered section or `None` to get the whole page
            (default: `None`)
            expandtemplates (bool): set to `True` to expand templates
            (default: `False`)
            cache (bool): set to `False` to disable caching (default: `True`)
        """

        if not self.can('read'):
            raise mwklient.errors.InsufficientPermission(self)
        if not self.exists:
            return u''
        if section is not None:  # can be 0
            section = text_type(section)

        key = hash((section, expandtemplates))
        if cache and key in self._textcache:
            return self._textcache[key]

        revs = self.revisions(
            prop='content|timestamp', limit=1, section=section, slots=slot)
        try:
            rev = next(revs)
            if 'slots' in rev:
                text = rev['slots'][slot]['*']
            else:
                text = rev['*']
            self.last_rev_time = rev['timestamp']
        except StopIteration:
            text = u''
            self.last_rev_time = None
        if not expandtemplates:
            self.edit_time = time.gmtime()
        else:
            # The 'rvexpandtemplates' option was removed in MediaWiki 1.32, so
            # we have to make an extra API call.
            # See: https://github.com/mwclient/mwclient/issues/214
            text = self.site.expandtemplates(text)

        if cache:
            self._textcache[key] = text
        return text

    def __check_edit__(self):
        if not self.site.logged_in and self.site.force_login:
            raise mwklient.errors.AssertUserFailedError()
        if self.site.blocked:
            raise mwklient.errors.UserBlocked(self.site.blocked)
        if not self.can('edit'):
            raise mwklient.errors.ProtectedPageError(self)

        if not self.site.writeapi:
            raise mwklient.errors.NoWriteApi(self)

    def __do_edit__(self, **kwargs):
        result = self.site.post(
            'edit',
            token=self.__get_token__('edit'),
            **kwargs)
        if result['edit'].get('result').lower() == 'failure':
            raise mwklient.errors.EditError(self, result['edit'])
        return result

    def save(self,
             text,
             summary=u'',
             minor=False,
             bot=True,
             section=None,
             **kwargs):
        """Update the text of a section or the whole page by performing an edit
         operation.
        """

        self.__check_edit__()

        data = {}
        if minor:
            data['minor'] = '1'
        if not minor:
            data['notminor'] = '1'
        if self.last_rev_time:
            data['basetimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                  self.last_rev_time)
        if self.edit_time:
            data['starttimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                   self.edit_time)
        if bot:
            data['bot'] = '1'
        if section:
            data['section'] = section

        data['title'] = self.name
        data['text'] = text
        data['summary'] = summary
        data.update(kwargs)

        if self.site.force_login:
            data['assert'] = 'user'

        try:
            result = self.__do_edit__(**data)
        except mwklient.errors.APIError as err:
            if err.code == 'badtoken':
                # Retry, but only once to avoid an infinite loop
                self.__get_token__('edit', force=True)
                try:
                    result = self.__do_edit__()
                except mwklient.errors.APIError as err:
                    self.handle_edit_error(err, summary)
            else:
                self.handle_edit_error(err, summary)

        # 'newtimestamp' is not included if no change was made
        if 'newtimestamp' in result['edit'].keys():
            self.last_rev_time = parse_timestamp(
                result['edit'].get('newtimestamp'))

        # clear the page text cache
        self._textcache = {}
        return result['edit']

    def undo(self, rev_id, summary=u'', bot=False, **kwargs):
        """Revert an edit with revision id `rev`
        """

        self.__check_edit__()
        data = {}
        if self.last_rev_time:
            data['basetimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                  self.last_rev_time)
        if self.edit_time:
            data['starttimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                   self.edit_time)

        data['undo'] = rev_id
        data['bot'] = '1' if bot else '0'
        data['title'] = self.name
        data['summary'] = summary
        data.update(kwargs)

        if self.site.force_login:
            data['assert'] = 'user'

        try:
            result = self.__do_edit__(**data)
        except mwklient.errors.APIError as err:
            if err.code == 'badtoken':
                # Retry, but only once to avoid an infinite loop
                self.__get_token__('edit', force=True)
                try:
                    result = self.__do_edit__(**data)
                except mwklient.errors.APIError as err:
                    self.handle_edit_error(err, summary)
            else:
                self.handle_edit_error(err, summary)

        # 'newtimestamp' is not included if no change was made
        if 'newtimestamp' in result['edit'].keys():
            self.last_rev_time = parse_timestamp(
                result['edit'].get('newtimestamp'))

        # clear the page text cache
        self._textcache = {}
        return result['edit']

    def handle_edit_error(self, err, summary):
        if err.code == 'editconflict':
            raise mwklient.errors.EditError(self, summary, err.info)
        if err.code in {
                'protectedtitle', 'cantcreate', 'cantcreate-anon',
                'noimageredirect-anon', 'noimageredirect', 'noedit-anon',
                'noedit', 'protectedpage', 'cascadeprotected',
                'customcssjsprotected', 'protectednamespace-interface',
                'protectednamespace'
        }:
            raise mwklient.errors.ProtectedPageError(self, err.code, err.info)
        if err.code == 'assertuserfailed':
            raise mwklient.errors.AssertUserFailedError()
        raise err

    def move(self, new_title, reason='', move_talk=True, no_redirect=False):
        """Move (rename) page to new_title.

        If user account is an administrator, specify no_redirect as True to not
        leave a redirect.

        If user does not have permission to move page, an
        InsufficientPermission exception is raised.

        """
        if not self.can('move'):
            raise mwklient.errors.InsufficientPermission(self)

        if not self.site.writeapi:
            raise mwklient.errors.NoWriteApi(self)

        data = {}
        if move_talk:
            data['movetalk'] = '1'
        if no_redirect:
            data['noredirect'] = '1'
        result = self.site.post(
            'move', ('from', self.name),
            to=new_title,
            token=self.__get_token__('move'),
            reason=reason,
            **data)
        return result['move']

    def delete(self, reason='', watch=False, unwatch=False, oldimage=False):
        """Delete page.

        If user does not have permission to delete page, an
        InsufficientPermission exception is raised.

        """
        if not self.can('delete'):
            raise mwklient.errors.InsufficientPermission(self)

        if not self.site.writeapi:
            raise mwklient.errors.NoWriteApi(self)

        data = {}
        if watch:
            data['watch'] = '1'
        if unwatch:
            data['unwatch'] = '1'
        if oldimage:
            data['oldimage'] = oldimage
        result = self.site.post(
            'delete',
            title=self.name,
            token=self.__get_token__('delete'),
            reason=reason,
            **data)
        return result['delete']

    def purge(self):
        """Purge server-side cache of page. This will re-render templates and
        other dynamic content.

        """
        self.site.post('purge', titles=self.name)

    # def watch: requires 1.14

    # Properties
    def backlinks(self,
                  namespace=None,
                  filterredir='all',
                  redirect=False,
                  limit=None,
                  generator=True):
        """List pages that link to the current page, similar to
        Special:Whatlinkshere.

        API doc: https://www.mediawiki.org/wiki/API:Backlinks

        """
        prefix = mwklient.listing.List.get_prefix('bl', generator)
        kwargs = dict(
            mwklient.listing.List.generate_kwargs(
                prefix,
                namespace=namespace,
                filterredir=filterredir,
            ))
        if redirect:
            kwargs['%sredirect' % prefix] = '1'
        kwargs[prefix + 'title'] = self.name

        return mwklient.listing.List.get_list(generator)(
            self.site,
            'backlinks',
            'bl',
            limit=limit,
            return_values='title',
            **kwargs)

    def categories(self, generator=True, show=None):
        """List categories used on the current page.

        API doc: https://www.mediawiki.org/wiki/API:Categories

        Args:
            generator (bool): Return generator (Default: True)
            show (str): Set to 'hidden' to only return hidden categories
                or '!hidden' to only return non-hidden ones.

        Returns:
            mwklient.listings.PagePropertyGenerator
        """
        prefix = mwklient.listing.List.get_prefix('cl', generator)
        kwargs = dict(mwklient.listing.List.generate_kwargs(prefix, show=show))

        if generator:
            return mwklient.listing.PagePropertyGenerator(
                self, 'categories', 'cl', **kwargs)
        # TODO: return sortkey if wanted
        return mwklient.listing.PageProperty(
            self, 'categories', 'cl', return_values='title', **kwargs)

    def embeddedin(self,
                   namespace=None,
                   filterredir='all',
                   limit=None,
                   generator=True):
        """List pages that transclude the current page.

        API doc: https://www.mediawiki.org/wiki/API:Embeddedin

        Args:
            namespace (int): Restricts search to a given namespace
            (Default: None)
            filterredir (str): How to filter redirects, either 'all' (default),
                'redirects' or 'nonredirects'.
            limit (int): Maximum amount of pages to return per request
            generator (bool): Return generator (Default: True)

        Returns:
            mwklient.listings.List: Page iterator
        """
        prefix = mwklient.listing.List.get_prefix('ei', generator)
        kwargs = dict(
            mwklient.listing.List.generate_kwargs(
                prefix, namespace=namespace, filterredir=filterredir))
        kwargs[prefix + 'title'] = self.name

        return mwklient.listing.List.get_list(generator)(
            self.site,
            'embeddedin',
            'ei',
            limit=limit,
            return_values='title',
            **kwargs)

    def extlinks(self):
        """List external links from the current page.

        API doc: https://www.mediawiki.org/wiki/API:Extlinks

        """
        return mwklient.listing.PageProperty(
            self, 'extlinks', 'el', return_values='*')

    def images(self, generator=True):
        """List files/images embedded in the current page.

        API doc: https://www.mediawiki.org/wiki/API:Images

        """
        if generator:
            return mwklient.listing.PagePropertyGenerator(self, 'images', '')
        return mwklient.listing.PageProperty(self, 'images', '',
                                             return_values='title')

    def iwlinks(self):
        """List interwiki links from the current page.

        API doc: https://www.mediawiki.org/wiki/API:Iwlinks

        """
        return mwklient.listing.PageProperty(
            self, 'iwlinks', 'iw', return_values=('prefix', '*'))

    def langlinks(self, **kwargs):
        """List interlanguage links from the current page.

        API doc: https://www.mediawiki.org/wiki/API:Langlinks

        """
        return mwklient.listing.PageProperty(
            self, 'langlinks', 'll', return_values=('lang', '*'), **kwargs)

    def links(self, namespace=None, generator=True, redirects=False):
        """List links to other pages from the current page.

        API doc: https://www.mediawiki.org/wiki/API:Links

        """
        prefix = mwklient.listing.List.get_prefix('pl', generator)
        kwargs = dict(
            mwklient.listing.List.generate_kwargs(prefix, namespace=namespace))

        if redirects:
            kwargs['redirects'] = '1'
        if generator:
            return mwklient.listing.PagePropertyGenerator(
                self, 'links', 'pl', **kwargs)
        return mwklient.listing.PageProperty(self, 'links', 'pl',
                                             return_values='title', **kwargs)

    def revisions(self,
                  startid=None,
                  endid=None,
                  start=None,
                  end=None,
                  direc='older',
                  user=None,
                  excludeuser=None,
                  limit=50,
                  prop='ids|timestamp|flags|comment|user',
                  expandtemplates=False,
                  section=None,
                  diffto=None,
                  slots=None):
        """List revisions of the current page.

        API doc: https://www.mediawiki.org/wiki/API:Revisions

        Args:
            startid (int): Revision ID to start listing from.
            endid (int): Revision ID to stop listing at.
            start (str): Timestamp to start listing from.
            end (str): Timestamp to end listing at.
            direc (str): Direction to list in: 'older' (default) or 'newer'.
            user (str): Only list revisions made by this user.
            excludeuser (str): Exclude revisions made by this user.
            limit (int): The maximum number of revisions to return per request.
            prop (str): Which properties to get for each revision,
                default: 'ids|timestamp|flags|comment|user'
            expandtemplates (bool): Expand templates in rvprop=content output
            section (int): If rvprop=content is set, only retrieve the contents
            of this section.
            diffto (str): Revision ID to diff each revision to. Use "prev",
                          "next" and "cur" for the previous, next and current
                          revision respectively.
            slots (str): The content slot (Mediawiki >= 1.32) to retrieve
                content from.

        Returns:
            mwklient.listings.List: Revision iterator
        """
        kwargs = dict(
            mwklient.listing.List.generate_kwargs(
                'rv',
                startid=startid,
                endid=endid,
                start=start,
                end=end,
                user=user,
                excludeuser=excludeuser,
                diffto=diffto,
                slots=slots))

        if self.site.version[:2] < (1, 32) and 'rvslots' in kwargs:
            # https://github.com/mwclient/mwclient/issues/199
            del kwargs['rvslots']

        kwargs['rvdir'] = direc
        kwargs['rvprop'] = prop
        if expandtemplates:
            kwargs['rvexpandtemplates'] = '1'
        if section is not None:
            kwargs['rvsection'] = section

        return mwklient.listing.RevisionsIterator(
            self, 'revisions', 'rv', limit=limit, **kwargs)

    def templates(self, namespace=None, generator=True):
        """List templates used on the current page.

        API doc: https://www.mediawiki.org/wiki/API:Templates

        """
        prefix = mwklient.listing.List.get_prefix('tl', generator)
        kwargs = dict(
            mwklient.listing.List.generate_kwargs(prefix, namespace=namespace))
        if generator:
            return mwklient.listing.PagePropertyGenerator(
                self, 'templates', prefix, **kwargs)
        return mwklient.listing.PageProperty(self, 'templates', prefix,
                                             return_values='title', **kwargs)
