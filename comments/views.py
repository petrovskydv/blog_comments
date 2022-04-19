from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from comments.models import Article, Comment
from comments.serializers import (ArticleSerializer, CommentForArticleSerializer, CommentForCommentSerializer,
                                  CommentListSerializer)


class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentList(generics.ListAPIView):
    """The list of comments to the article up to the third level of nesting"""

    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def get(self, request, *args, **kwargs):
        qs = Comment.objects.filter(article__id=kwargs['pk'], level__lte=3)
        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentForCommentList(generics.ListAPIView):
    """The list of comments to the comment"""

    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        qs = comment.get_descendants(include_self=False)
        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentForArticleCreate(generics.CreateAPIView):
    """Create comment for article"""

    queryset = Comment.objects.all()
    serializer_class = CommentForArticleSerializer

    def post(self, request, *args, **kwargs):
        serializer = CommentForArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Comment.objects.create(
            article=get_object_or_404(Article, pk=kwargs['pk']),
            text=serializer.validated_data['text']
        )
        return Response(serializer.data, status=HTTP_201_CREATED)


class CommentForCommentCreate(generics.CreateAPIView):
    """Create comment for comment"""

    queryset = Comment.objects.all()
    serializer_class = CommentForCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CommentForCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data['parent']
        Comment.objects.create(
            article=parent.article,
            parent=parent,
            text=serializer.validated_data['text']
        )
        return Response(serializer.data, status=HTTP_201_CREATED)
