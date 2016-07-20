from __future__ import unicode_literals

from tasker.plugins import Plugin


class WebsiteTLD(Plugin):
    plugin_name = "wtld"
    plugin_name_verbose = "Website TLD"

    @classmethod
    def process(self, answers):
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
