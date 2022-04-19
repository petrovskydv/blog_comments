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
    path("articles/<int:pk>/comments", views.CommentList.as_view(), name="article_comments"),
    path("articles/<int:pk>/comment", views.CommentForArticleCreate.as_view(), name="article_comment"),
    path("comments/<int:pk>/comment", views.CommentForCommentCreate.as_view(), name="comment"),
    path("comments/<int:pk>/comments", views.CommentForCommentList.as_view(), name="comments"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
