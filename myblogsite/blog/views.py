from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm, commentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required #for automated login required functionality
from django.contrib.auth.mixins import LoginRequiredMixin #localy
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    #to get post model from backend sqlite databe and return it ordering by published date
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    #LoginRequiredMixin is just an analogy og decorator we hav used before
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') # to return user from login page to home page after succ login

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name  = 'blog/post_detail.html'
    model = Post
    # as drafts are unpublished, below query will return from database only post created_date where published date is null
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#################################################################################
#function base view for comments
#################################################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish() #when calling such method, add () to execute it
    return redirect('post_detail',pk=pk)


@login_required #decorator to enforce login before posting a comment
def add_comment_to_post(request, pk): #pk primary key that links comment to the actual post
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST': # if somoeone writes a post then if it is valid ...
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = commentForm()
    return render(request, 'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = Comment.post.pk #to save post primary key as a seperate variable before deleting it
    comment.delete()
    return rediect('post_detail',pk=post_pk)

#login views
