from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view, name='delete_post'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('change_password/', ChangePasswordView, name='change_password'),
    path('change_password_done/', ChangePasswordDoneView.as_view(), name='change_password_done'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_done/', ResetPasswordDoneView.as_view(), name='reset_password_done'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls'))
]