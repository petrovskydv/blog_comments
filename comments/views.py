from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from comments.models import Article, Comment
from comments.serializers import (ArticleSerializer, CommentForArticleSerializer, CommentForCommentSerializer,
                                  CommentListSerializer)


class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


user_response = openapi.Response('response description', CommentListSerializer)


@swagger_auto_schema(method='get', responses={200: user_response})
@swagger_auto_schema(method='post', request_body=CommentForArticleSerializer)
@api_view(['GET', 'POST'])
def comment_for_article(request, article_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(article__id=article_id, level__lte=3)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentForArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Comment.objects.create(
            article=get_object_or_404(Article, pk=article_id),
            text=serializer.validated_data['text']
        )
        return Response(serializer.data, status=HTTP_201_CREATED)


@swagger_auto_schema(method='get', responses={200: user_response})
@swagger_auto_schema(method='post', request_body=CommentForCommentSerializer)
@api_view(['GET', 'POST'])
def comment_for_comment(request, comment_id):
    if request.method == 'GET':
        parent = get_object_or_404(Comment, pk=comment_id)
        comments = parent.get_descendants(include_self=False)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentForCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data['parent']
        Comment.objects.create(
            article=parent.article,
            parent=parent,
            text=serializer.validated_data['text']
        )
        return Response(serializer.data, status=HTTP_201_CREATED)
