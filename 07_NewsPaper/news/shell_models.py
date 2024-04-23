
# use in NewsPaper/
# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell

from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создаем пользователей
user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

# Создаем авторов, связанных с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавляем категории
category1 = Category.objects.create(name='Category 1')
category2 = Category.objects.create(name='Category 2')
category3 = Category.objects.create(name='Category 3')
category4 = Category.objects.create(name='Category 4')

# Добавляем статьи и новость
post1 = Post.objects.create(author=author1, title='Post 1', text='Text for post 1')
post2 = Post.objects.create(author=author2, title='Post 2', text='Text for post 2')
news1 = Post.objects.create(author=author1, title='News 1', text='Text for news 1', type='news')

# Присваиваем категории
post1.category.add(category1, category2)
post2.category.add(category3, category4)
news1.category.add(category1, category3)

# Создаем комментарии
comment1 = Comment.objects.create(post=post1, user=author1.user, text='Comment 1 for post 1')
comment2 = Comment.objects.create(post=post1, user=author2.user, text='Comment 2 for post 1')
comment3 = Comment.objects.create(post=post2, user=author1.user, text='Comment 1 for post 2')
comment4 = Comment.objects.create(post=news1, user=author2.user, text='Comment for news 1')

# Применяем функции like() и dislike()
post1.like()
post2.dislike()
comment1.like()
comment3.dislike()

# Обновляем рейтинги пользователей
author1.update_rating()
author2.update_rating()

# Выводим username и рейтинг лучшего пользователя
best_user = Author.objects.all().order_by('-rating').first()
print(f"Лучший пользователь: {best_user.user.username}, рейтинг: {best_user.rating}")

# Выводим информацию о лучшей статье
best_post = Post.objects.filter(type='article').order_by('-rating').first()
print(f"Лучшая статья:\nДата добавления: {best_post.date_add}\nАвтор: {best_post.author.user.username}\nРейтинг: {best_post.rating}\nЗаголовок: {best_post.title}\nПревью: {best_post.preview()}")

# Выводим все комментарии к лучшей статье
comments_to_best_post = Comment.objects.filter(post=best_post)
for comment in comments_to_best_post:
    print(f"Дата: {comment.date_add}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")


#
