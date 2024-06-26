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
    GrupoFormularios,
    Inferencia,
    InferirConsulta,
    Keyword,
    KeywordNoMapping,
    KeywordsByRule,
    Rule,
    Tuplas,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("motor-inferencia/", InferirConsulta.as_view(), name="motor_inferencia"),
    path("rule/", Rule.as_view(), name="rule_create"),
    path("rule/<str:id>", Rule.as_view(), name="rule"),
    path("keyword/", Keyword.as_view(), name="keyword_create"),
    path("keyword/<str:id>", Keyword.as_view(), name="keyword"),
    path("inferencia/", Inferencia.as_view(), name="inferencia_create"),
    path("inferencia/<str:id>", Inferencia.as_view(), name="inferencia"),
    path(
        "keyword-no-mapping/<str:keyword_no_mapping_id>",
        KeywordNoMapping.as_view(),
        name="keyword_no_mapping",
    ),
    path(
        "keyword-no-mapping/",
        KeywordNoMapping.as_view(),
        name="get-keywords-no-mapping",
    ),
    path(
        "keywords/by-rule/<str:rule_id>",
        KeywordsByRule.as_view(),
        name="keywords_by_rule",
    ),
    path("tuplas/", Tuplas.as_view(), name="tuplas"),
    path(
        "grupo-formularios/",
        GrupoFormularios.as_view(),
        name="create_list_grupo_formulario",
    ),
    path(
        "grupo-formularios/<str:id>",
        GrupoFormularios.as_view(),
        name="list_grupo_formulario_id",
    ),
]
