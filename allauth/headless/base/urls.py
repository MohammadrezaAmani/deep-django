from allauth.headless.base import views
from django.urls import path


def build_urlpatterns(client):
    return [
        path(
            "config",
            views.ConfigView.as_api_view(client=client),
            name="config",
        ),
    ]
