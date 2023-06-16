"""
URL configuration for mdmq_motor_inferencia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from motorInferencia.views import (
    InferirConsulta,
    Rule,
    Keyword,
    Inferencia,
    KeywordNoMapping,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("motor-inferencia/", InferirConsulta.as_view(), name="motor_inferencia"),
    path("rule/", Rule.as_view(), name="rule"),
    path("keyword/", Keyword.as_view(), name="keyword"),
    path("inferencia/", Inferencia.as_view(), name="inferencia"),
    path(
        "keyword-no-mapping/<str:keyword_no_mapping_id>",
        KeywordNoMapping.as_view(),
        name="keyword_no_mapping",
    ),
]
