from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = self.calculate_post_rating() + self.calculate_comment_rating() + self.calculate_post_comment_rating()
        self.save()

    def calculate_post_rating(self):
        return (self.post_set.aggregate(total=models.Sum(models.F('rating') * 3))['total'] or 0)

    def calculate_comment_rating(self):
        return (self.user.comment_set.aggregate(total=models.Sum('rating'))['total'] or 0)

    def calculate_post_comment_rating(self):
        return (self.post_set.aggregate(total=models.Sum('comment__rating'))['total'] or 0)

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # Рассылка новостей
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name.title()}'


class Post(models.Model):
    article = 'article'
    news = 'news'

    post_type = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=post_type, default=article)
    date_add = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def preview(self):
        short_text = self.text[:124] + '...'
        return short_text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.preview()
        # return f'{self.title.title()}: {self.text[:20]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.title()}'