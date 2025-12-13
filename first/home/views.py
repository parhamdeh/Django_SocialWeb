from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm, PostCreateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts})
    

    def post(self, request):
        return render(request, 'home/index.html')

class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instnce = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        comments = self.post_instnce.pcomments.filter(is_reply=False)
        can_like = True
        if request.user.is_authenticated and self.post_instnce.user_can_like(request.user):
            can_like = False
        return render(request, 'home/detail.html', {'post':self.post_instnce, 'comments': comments, 'form':self.form_class(), 'reply_form':self.form_class_reply(), 'can_like':can_like})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form1 = self.form_class(request.POST)
        if form1.is_valid():
            new_comment = form1.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instnce
            new_comment.save()
            messages.success(request, 'your comment sent', 'success')
            return redirect('home:post_detail', self.post_instnce.id, self.post_instnce.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted successfly', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('home:home')
    

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant updated this post!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})


    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you updated post!', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm #a form class
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kewargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form':form})


    def post(self, request, *args, **kewargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post created!!', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
        return redirect('home:post_create')
        

class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply sent!', 'success')
        return redirect('home:post_detail', post.id, post.slug)
    

class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user = request.user)
        if like.exists():
            messages.error(request, 'you already liked this post', 'error')
        else:
            Vote.objects.create(user = request.user, post=post)
            messages.success(request, 'you liked this post', 'success')
        return redirect('home:post_detail', post.id, post.slug)