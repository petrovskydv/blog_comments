from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Article(models.Model):
    title = models.CharField('Название статьи', max_length=200)
    text = models.TextField('Текст статьи')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.id} {self.title}'


class Comment(MPTTModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )
    text = models.TextField('Текст комментария')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.id}'
