from allauth.headless.usersessions import views
from django.urls import include, path


def build_urlpatterns(client):
    return [
        path(
            "auth/",
            include(
                [
                    path(
                        "sessions",
                        views.SessionsView.as_api_view(client=client),
                        name="sessions",
                    ),
                ]
            ),
        )
    ]
