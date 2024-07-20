from django.urls import path
from .views import NewsList, NewsDetail, NewsFilter, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, SubscribeToCategory

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view()),
   path('search/', NewsFilter.as_view(), name='news_filter'),
   path('create_news/', NewsCreate.as_view(), name='news_create'),
   path('create_article/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('category/<int:category_id>/subscribe/', SubscribeToCategory.as_view(), name='subscribe_to_category'),
]
