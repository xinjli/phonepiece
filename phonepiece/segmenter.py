from ipapy.ipastring import IPAString
import panphon


class PhoneSegmenter:

    def __init__(self):
        self.ft = panphon.FeatureTable()

    def segment(self, ipa_string):
        ipa_string = IPAString(unicode_string=ipa_string, ignore=True)
        phones = ''.join([(u"%s" % c) for c in ipa_string])
        phone_lst = self.ft.ipa_segs(phones)

        return phone_lst