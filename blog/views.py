from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment

''' Function based view of home
def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)
'''


# LIST VIEW for all Post #
# template convention for class views => <app>/<model>_<viewtype>.html
# default context_object_name = object
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # from newest to oldest
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(announcement=False).order_by('-date_posted')


# LIST VIEW for all Post of one User #
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):  # override
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, announcement=False).order_by('-date_posted')


# LIST VIEW for Announcement #
class AnnouncementListView(ListView):
    model = Post
    template_name = 'blog/announcements.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(announcement=True).order_by('-date_posted')


# DETAIL VIEW for Post #
# <app>/<model>_detail.html
# default context_object_name = object
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=context['object'])
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


# CREATE VIEW for Post #
# <app>/<model>_form.html
# default context_object_name = form
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # override
        form.instance.author = self.request.user
        return super().form_valid(form)


# CREATE VIEW for Announcement #
class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'announcement']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# UPDATE VIEW for Post #
# no template required
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # override
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # override from UserPassesTestMixin
        post = self.get_object()
        return self.request.user == post.author


# DELETE VIEW for Post #
# <app>/<model>_confirm_delete.html
# default context_object_name = object
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):  # override from UserPassesTestMixin
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
