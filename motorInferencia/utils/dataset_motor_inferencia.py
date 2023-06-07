from django.conf import settings
from motorInferencia.models import KeywordsModel


def get_keywords():
    keywordsResponse = KeywordsModel.objects.all()
    data_keywords = []
    for keyword in keywordsResponse:
        data_keywords.append((keyword.keyword, keyword.rule.rule))

    return data_keywords


def set_keywords():
    # keywordsResponse = KeywordsModel.objects.all()
    # data_keywords = []
    # for keyword in keywordsResponse:
    #     data_keywords.append((keyword.keyword, keyword.rule.rule))

    return
