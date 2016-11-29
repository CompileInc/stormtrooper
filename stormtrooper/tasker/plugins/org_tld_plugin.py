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
