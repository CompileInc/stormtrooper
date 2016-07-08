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
            tld = tldextract.extract(answer)
            domain = "%s.%s" % (tld.domain, tld.suffix) if tld.suffix is not '' else ''
            _answers.append(domain)
        return _answers
