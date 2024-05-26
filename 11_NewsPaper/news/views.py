# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import NewsForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives  # класс для создание объекта письма с html
from django.template.loader import render_to_string  # функция, которая рендерит наш html в текст
from django.shortcuts import get_object_or_404, redirect


class NewsList(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsFilter(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def send_post_notification(post, subscribers):
    for user in subscribers:
        # Получаем наш html с учетом пользователя
        html_content = render_to_string(
            'post_created.html',
            {
                'post': post,
                'user': user,
            }
        )

        # Отправка письма
        msg = EmailMultiAlternatives(
            subject=f'{post.title} | {post.date_add.strftime("%Y-%m-%d")}',
            body=post.text,
            from_email='django.emailsender@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        print(f'DEBUG: Sended email - {user.email}')
        msg.send()  # отсылаем


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'news'
        post.save()

        # Сохраняем категории через промежуточную модель PostCategory
        categories = form.cleaned_data['category']
        for category in categories:
            PostCategory.objects.create(post=post, category=category)

        # Отправка уведомлений
        # Собираем все email подписчиков
        subscribers = set()
        for category in post.category.all():
            for user in category.subscribers.all():
                subscribers.add(user)

        # Отправка писем каждому подписчику
        send_post_notification(post, subscribers)

        return super().form_valid(form)




class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'article'
        post.save()

        # Сохраняем категории через промежуточную модель PostCategory
        categories = form.cleaned_data['category']
        for category in categories:
            PostCategory.objects.create(post=post, category=category)

        # Отправка уведомлений
        # Собираем все email подписчиков
        subscribers = set()
        for category in post.category.all():
            for user in category.subscribers.all():
                subscribers.add(user)

        # Отправка писем каждому подписчику
        send_post_notification(post, subscribers)

        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')

    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')

    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class SubscribeToCategory(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.subscribers.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))