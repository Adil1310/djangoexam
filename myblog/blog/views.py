from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import *
from .models import *

class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        #вызываем метод get_context_data() родительского класса и сохраняет его результаты в переменную context. 
        
        posts = Post.objects.all().annotate(comment_count=Count('comment')).order_by('-id') 
        #Здесь мы получаем все объекты модели Post из базы данных с использованием метода all().
        
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #разбивает список постов на страницы. На каждой странице будет отображаться 6 постов.

        latest  = Post.objects.all().order_by('-id')[:3] #для упорядочивания постов по убыванию значения поля id.
        context['posts'] = posts
        context['latest'] = latest
        context['paginator'] = paginator

        return context

class PostView(generic.ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).annotate(comment_count=Count('comment'))

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(blog=self.get_object())
        print(len(comments))
        context['comments'] = comments
        return context
    
    def post(self, request, *args, **kwargs):
        comment = Comment()
        comment.blog = self.get_object()
        comment.user = request.user
        comment.content = request.POST['content']
        comment.save()
        messages.success(request, "Comment added successfully")
        messages.get_messages(request).used = True
        return self.get(request, *args, **kwargs)

class PostBlog(LoginRequiredMixin, generic.FormView):
    template_name = "postBlog.html"
    form_class = PostForm
    success_url = "/postBlog/"

    def form_valid(self, form):
        blogpost = form.save(commit=False)
        blogpost.author = self.request.user
        blogpost.save()
        messages.success(self.request, "Blog post created successfully"); messages.get_messages(self.request).used = True
        return super().form_valid(form)

class EditPostView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'editPost.html'
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully')
        messages.get_messages(self.request).used = True
        return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'deletePost.html'
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully')
        messages.get_messages(self.request).used = True
        return super().delete(request, *args, **kwargs)

class LoginView(generic.View):
    template_name = 'registration/login.html'
    success_url = "/"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:index')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('blog:index')
        else:
            messages.error(request, 'Invalid Username or Password')
            messages.get_messages(request).used = True
            return render(request, self.template_name)

class SignupView(generic.View):
    template_name = 'registration/signup.html'
    success_url = "/"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:index')
        return render(request, self.template_name)

    def post(self, request):
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password != cpassword:
            messages.error(request, 'Confirm Password does not match')
            messages.get_messages(request).used = True
            return render(request, self.template_name)
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                messages.get_messages(request).used = True
                return render(request, self.template_name)
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    messages.get_messages(request).used = True
                    return render(request, self.template_name)
                else:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
                    user.save()
                    messages.success(request, 'Account created successfully')
                    messages.get_messages(request).used = True
                    return redirect('blog:login')

class LogoutView(generic.View):

    def get(self, request):
        auth_logout(request)
        return redirect('blog:index')

class PostList(LoginRequiredMixin, generic.ListView):
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        posts = Post.objects.all()
        
        if query:
            posts = posts.filter(title__icontains=query)
        
        return posts