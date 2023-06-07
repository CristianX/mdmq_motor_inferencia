from django.conf import settings
from motorInferencia.models import KeywordsModel


def get_keywords(self):
    return self.keywords


def set_keywords():
    keywordsResponse = KeywordsModel.objects.all()
    data_keywords = []
    for keyword in keywordsResponse:
        data_keywords.append((keyword.keyword, keyword.rule.rule))

    # print(data_keywords)
    settings.DATA_KEYWORDS = data_keywords
    print(settings.DATA_KEYWORDS)
