from __future__ import unicode_literals

from tasker.plugins import Plugin


class WebsiteTLD(Plugin):
    plugin_name = "wtld"
    plugin_name_verbose = "Website TLD"

    @classmethod
    def process(cls, answers):
        import tldextract
        _answers = []
        for answer in answers:
            try:
                tld = tldextract.extract(answer.decode('utf-8'))
                domain = u'%s.%s' % (tld.domain, tld.suffix) if tld.suffix is not '' else ''
            except Exception as e:
                domain = ''
            _answers.append(domain)
        return _answers


class WebsiteTLDSub(Plugin):
    plugin_name = "wtlds"
    plugin_name_verbose = "Website TLD (with subdomain)"

    @classmethod
    def process(cls, answers):
        import re
        import tldextract
        from django.core.validators import EMPTY_VALUES
        _answers = []
        for answer in answers:
            extract = tldextract.extract(answer.decode('utf-8'))
            if extract.domain in EMPTY_VALUES or\
               extract.suffix in EMPTY_VALUES:
                tmp_domain = ''
            else:
                extract = list(extract)
                tmp_domain = ".".join(extract)
                p = re.compile("^[w]{1,3}([\d]{0,2})?\.")
                m = p.search(tmp_domain)
                if m:
                    tmp_domain = tmp_domain[len(m.group(0)):]

            _answers.append(tmp_domain.lstrip(".").lower())
        return _answers


class FuzzyWebsiteMatch(Plugin):
    plugin_name = 'fzweb'
    plugin_name_verbose = 'Fuzzy Website match (with subdomain)'
    COMPUTE_ANSWER = True

    @staticmethod
    def get_majority_item(items):
        from collections import Counter
        c = Counter(items)
        most_common = c.most_common()
        max_freq = most_common[0][1]
        if max_freq == 1:
            return None
        if len(c) > 1 and not max_freq > most_common[1][1]:
            return None
        else:
            return most_common[0][0]

    @staticmethod
    def get_website_tld(domain):
        import re
        import tldextract
        from django.core.validators import EMPTY_VALUES
        domain = domain.strip().lower()
        extract = tldextract.extract(domain)
        if extract.domain in EMPTY_VALUES or\
           extract.suffix in EMPTY_VALUES:
            tmp_domain = ''
        else:
            extract = list(extract)
            tmp_domain = ".".join(extract)
            p = re.compile("^[w]{1,3}([\d]{0,2})?\.")
            m = p.search(tmp_domain)
            if m:
                tmp_domain = tmp_domain[len(m.group(0)):]
        return tmp_domain.lstrip(".").strip()

    @classmethod
    def normalize_website(cls, w):
        from django.core.validators import EMPTY_VALUES
        from urlparse import urlparse, urlunparse, ParseResult
        w = w.decode('utf-8')
        if w in EMPTY_VALUES:
            return None
        w = w.lower().strip()
        if not w.startswith('http://') and not w.startswith('https://'):
            w = 'http://' + w.lstrip('/')
        parsed = urlparse(w)
        new_parsed = ParseResult(scheme='http',
                                 netloc=cls.get_website_tld(w),
                                 path=parsed.path.rstrip('/'),
                                 params='',
                                 query=parsed.query,
                                 fragment='')
        return urlunparse(new_parsed)

    @classmethod
    def process(cls, answers):
        from collections import defaultdict
        websites = map(cls.normalize_website, answers)
        result_website = None
        votes = 0
        website_tlds = defaultdict(list)
        _website_tlds = []
        for w in websites:
            website_tld = cls.get_website_tld(w)
            _website_tlds.append(website_tld)
            website_tlds[website_tld].append(w)
        common_website_tld = cls.get_majority_item(_website_tlds)
        if common_website_tld is None:
            return (None, 0)
        common_websites = website_tlds[common_website_tld]
        common_website = cls.get_majority_item(common_websites)
        if common_website:
                result_website = common_website
        else:
            result_website = cls.normalize_website(cls.get_website_tld(common_websites[0]))
        for website in websites:
            if result_website in website:
                votes += 1
        return (result_website, votes)
