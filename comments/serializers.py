from rest_framework import serializers

from comments.models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text']


class CommentForArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']


class CommentForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'text']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'parent', 'level', 'article']
