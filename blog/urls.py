from django.urls import path
from . import views
from .views import (PostDeleteView, PostListView,
        PostDetailView, PostCreateView, PostUpdateView, UserPostListView,portfolio,Homepage,companyGraph)


urlpatterns = [
    path('',Homepage, name='blog-home'),
    path('graph-<str:cmpname>/',companyGraph,name="company-graph"),

    path('blog/', PostListView.as_view(),),
    path('portfolio/', portfolio,),
    
    path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    
    path('newsSection/',views.NewsFunc,name="news"),
   
   
    path('company-news/<str:cmpname>/',views.CompanyInformation,name="company-information"),
    path('company-information/',views.companyGraph,name="company-graph-default"),
]



