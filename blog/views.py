from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from blog.forms import PostForm, CommentForm, ReplyForm
from blog.models import Post, Category, Tag, ContentImage, Comment, Reply
# Create your views here.


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 1


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'
    paginate_by = 1

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(
            Category, slug=category_slug)
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagListView(ListView):
    queryset = Tag.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'
    paginate_by = 1

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return super().get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchPostView(ListView):
    model = Post
    template_name = 'blog/search_post.html'
    paginate_by = 1

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (Q(title__icontains=query) |
                   Q(content__icontains=query) |
                   Q(category__name__icontains=query) |
                   Q(tags__name__icontains=query))
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class PostFormView(CreateView):
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = '/'


class PostSaveView(PostFormView):
    def post(self, request, *args, **kwargs):
        form = PostForm(data=request.POST)
        if form.is_valid():
            is_public = form.save(commit=False)
            is_public.is_public = True
            is_public.save()
            form.save_m2m()
            return redirect('/')


class CommentFormView(CreateView):
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_disapprove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.disapprove()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)


class ReplyFormView(CreateView):
    template_name = 'blog/reply_form.html'
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('blog:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_disapprove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.disapprove()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)
