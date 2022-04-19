from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from comments import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path("articles/", views.ArticleListCreate.as_view(), name="article"),
    path("articles/<int:article_id>/comments", views.comment_for_article, name="article_comments"),
    path("comments/<int:comment_id>/comments", views.comment_for_comment, name="comments"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
