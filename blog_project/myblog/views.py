from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordResetView

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('post_list')
        return render(request, 'registration/login.html')

class PostListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'myblog/post_list.html', {'posts': posts})

class PostDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'myblog/post_detail.html', {'post': post})

class CreatePostView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        author = request.user
        title = request.POST['title']
        text = request.POST['text']
        post = Post.objects.create(author=author, title=title, text=text)
        return redirect('post_list')
    def get(self, request):
        return render(request, 'myblog/create_post.html')

class EditPostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post
    template_name = 'myblog/edit_post.html'
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy('post_list')


class LikePostView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})

class ChangePasswordView(LoginRequiredMixin, PasswordChangeForm):
    login_url = '/login/'
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('change_password_done')

class ChangePasswordDoneView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'registration/change_password_done.html'

class ResetPasswordView(PasswordResetView):
    template_name = 'registration/reset_password.html'
    email_template_name = 'registration/reset_password_email.html'
    subject_template_name = 'registration/reset_password_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class ResetPasswordDoneView(TemplateView):
    template_name = 'registration/reset_password_done.html'