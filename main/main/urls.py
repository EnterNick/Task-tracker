from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from django.views.generic import TemplateView

from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema = get_schema_view(
    Info(
        title="Task-tracker API",
        default_version='v1',
        description="Система управления задачами, которая позволит пользователям создавать и управлять проектами и "
                    "задачами, назначать исполнителей и отслеживать статус выполнения.",
    ),
    patterns=[path('api/v1/', include('task_traker.urls')), ],
)

urlpatterns = [
    re_path(
        r'^api/v1/docs-ui/$',
        TemplateView.as_view(
            template_name='docs/docs.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='docs'
    ),
    re_path(
        r'^api/v1/docs(?P<format>\.json|\.yaml)$',
        schema.without_ui(cache_timeout=0),
        name='docs-json_or_-yaml'
    ),
    re_path(r'^api/v1/admin/', admin.site.urls),
    re_path(r'^api/v1/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^api/v1/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/v1/', include('task_traker.urls')),
    re_path(r'^api/v1/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
