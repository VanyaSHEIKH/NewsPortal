from django.urls import path

from .views import *


urlpatterns = [
   path('', PostList.as_view(),name='new_list'),
   path('<int:pk>', PostDetail.as_view(),name='new'),
   path('create/',PostCreate.as_view(),name='new_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='new_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),
   path('search/', PostSearch.as_view(), name='new_search'),
   path('articles/create/', PostCreate.as_view(), name='news_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('category/', CategoryList.as_view(), name='categories_list'),
   path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('category/<int:pk>/',CategoryDetail.as_view(),name='category'),
   path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),

]

