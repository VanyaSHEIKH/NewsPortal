from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username.title()

    def update_rating(self):
        article_rating = 0
        comment_rating = 0
        article_comment_rating = 0

        # Используем related_name для получения постов
        for post in self.posts.all():  # Теперь используем self.posts вместо self.post_set
            article_rating += post.rating * 3

        # Суммарный рейтинг всех комментариев автора
        for comment in Comment.objects.filter(user=self.user):
            comment_rating += comment.rating

        # Суммарный рейтинг всех комментариев к статьям автора
        for post in self.posts.all():  # Также здесь меняем на self.posts
            for comment in post.comments.all():  # И здесь на post.comments
                article_comment_rating += comment.rating

        # Обновляем рейтинг автора
        self.rating = article_rating + comment_rating + article_comment_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=60, unique=True)
    rating = models.IntegerField(default=0)
    date_in = models.DateTimeField(default=datetime.datetime.now)
    subscribers=models.ManyToManyField(User,related_name='subscribed_posts', blank=True)

    def __str__(self):
        return self.name_category.title()


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    POST_TYPES = [
        (news, "Новость"),
        (article, "Статья")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:255] + "..."

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('new', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name_category.title()}: {self.post.title.title()}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.category.name}"