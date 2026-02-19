from django.contrib import admin
from django.urls import path
from Overview import views
from django.conf.urls import include
from Blog import views
from PersonalProjects import settings
from django.conf.urls.static import static

app_name = 'blog'


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    path('post/publish/', views.PostCreateFuncView, name='post_create'),
    
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(), name='post_update'),

    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    path('post/<int:pk>/comment', views.add_comment, name='add_comment'),
    
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
    
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    
    path('draft/', views.DraftListView.as_view(), name='post_drafts'),
    
    path('about/', views.BlogHomeView.as_view(), name='about'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

