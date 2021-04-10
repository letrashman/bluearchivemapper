import requests


def boolparams(**kwargs):
    return {key: 1 for key, value in kwargs.items() if value}


class Wiki:
    def __init__(self, url):
        self.url = url
        self._s = requests.Session()

    def create(self, title, text, summary, bot=True, token=None):
        if token is None:
            token = self.token('csrf')

        r = self._s.post(self.url, data={
            'action': 'edit',
            'title': title,
            'text': text,
            'summary': summary,
            'format': 'json',
            **boolparams(bot=bot, createonly=True),
            'token': token
        })
        data = r.json()
        return data['edit']

    def edit(self, pageid, revid, text, summary, bot=True, token=None):
        if token is None:
            token = self.token('csrf')

        r = self._s.post(self.url, data={
            'action': 'edit',
            'pageid': pageid,
            'revid': revid,
            'text': text,
            'summary': summary,
            'format': 'json',
            **boolparams(bot=bot),
            'token': token
        })
        data = r.json()
        return data['edit']

    def login(self, username, password, token=None):
        if token is None:
            token = self.token('login')

        r = self._s.post(self.url, data={
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': token,
            'format': 'json'
        })

    def parse(self, page, prop, redirects=False):
        r = self._s.get(self.url, params={
            'action': 'parse',
            'page': page,
            'prop': prop,
            'format': 'json',
            **boolparams(redirects=redirects)
        })
        data = r.json()
        return data['parse']

    def token(self, type_):
        r = self._s.get(self.url, params={
            'action': 'query',
            'meta': 'tokens',
            'type': type_,
            'format': 'json'
        })
        data = r.json()
        return data['query']['tokens'][type_ + 'token']

    def upload(self, filename, f, token=None):
        if token is None:
            token = self.token('csrf')

        r = self._s.post(self.url, data={
            'action': 'upload',
            'filename': filename,
            'format': 'json',
            **boolparams(ignorewarnings=True),
            'token': token
        }, files={
            'file': (filename, f, 'multipart/form-data')
        })
        data = r.json()
        try:
            return data['upload']
        except KeyError:
            print(data)
