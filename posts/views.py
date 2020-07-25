from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, GroupForm, CommentForm
from .models import User, Post, Group, Comment, Follow


def index(request):
    post_list = Post.objects.select_related(
        'author', 'group').order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "group.html",
        {
            "group": group,
            "page": page,
            'paginator': paginator
        }
    )


def groups(request):
    group_list = Group.objects.order_by('title')
    paginator = Paginator(group_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "groups.html",
        {
            "page": page,
            'paginator': paginator
        }
    )


@login_required
def create_group(request):
    title = 'Новая группа'
    button = 'Создать группу'
    if request.method == 'POST':
        form = GroupForm(request.POST or None)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            return redirect('group', slug=group.slug)
    else:
        form = GroupForm()
    return render(
        request, 'create_group.html',
        {
            'form': form,
            'title': title,
            'button': button
        }
    )


@login_required
def group_edit(request, slug):
    group = get_object_or_404(Group, slug=slug)
    title = 'Редактировать группу'
    button = 'Сохранить'
    if request.user == group.author:
        if request.method == "POST":
            form = GroupForm(request.POST or None, instance=group)
            if form.is_valid():
                group = form.save(commit=False)
                group.author = request.user
                group.save()
                return redirect('group', slug=group.slug)
        else:
            form = GroupForm(instance=group)
        return render(
            request, 'group_edit.html',
            {
                'form': form,
                'group': group,
                'title': title,
                'button': button
            }
        )
    return redirect('group', slug=slug)


@login_required
def delete_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    if request.user == group.author:
        group.delete()
        return redirect('groups')
    return redirect('group', slug=slug)


@login_required
def new_post(request):
    title = 'Новая запись'
    button = 'Опубликовать'
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(
        request, 'posts/create_post.html',
        {
            'form': form,
            'title': title,
            'button': button
        }
    )


@login_required
def post_edit(request, username, post_id):
    post_author = User.objects.get(username=username)
    post = get_object_or_404(Post, author=post_author, id=post_id)
    title = 'Редактировать запись'
    button = 'Сохранить'
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST or None,
                            files=request.FILES or None, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post', username=post.author, post_id=post.id)
        else:
            form = PostForm(instance=post)
        return render(
            request, 'posts/edit_post.html', {'form': form,
                                              'post': post, 'title': title,
                                              'button': button}
        )
    return redirect('post', username=post.author, post_id=post.id)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.select_related(
        'author', 'group').order_by('-pub_date').filter(author=profile.id)
    following = False
    if request.user.is_authenticated:
        follow_count = Follow.objects.filter(
            user=request.user, following=profile
        ).count()
        if follow_count > 0:
            following = True
    followers = Follow.objects.filter(following=profile).count()
    follow = Follow.objects.filter(user=profile).count()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "posts/profile.html",
        {
            'profile': profile,
            'posts': posts,
            'paginator': paginator,
            'page': page,
            'following': following,
            'followers': followers,
            'follow': follow
        }
    )


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    form = CommentForm()
    post = Post.objects.select_related(
        'author', 'group'
    ).annotate(
        comment_count=Count('post_comments')
    ).get(id=post_id)
    followers = Follow.objects.filter(following=profile).count()
    follow = Follow.objects.filter(user=profile).count()
    comments = Comment.objects.filter(post=post_id)
    # мб костыль
    posts = Post.objects.select_related(
        'author', 'group').order_by('-pub_date').filter(author=profile.id)
    return render(
        request, 'posts/post_detail.html',
        {
            'profile': profile,
            'post': post,
            'posts': posts,
            'comments': comments,
            'form': form,
            'followers': followers, 'follow': follow
        }
    )


@login_required
def post_delete(request, username, post_id):
    post_author = User.objects.get(username=username)
    post = get_object_or_404(Post, author=post_author, id=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('profile', username=post.author)
    return redirect('post', username=post.author, post_id=post.id)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()
    return redirect('post', username=post.author.username, post_id=post_id)


@login_required
def follow_index(request):
    favorites = Follow.objects.filter(user=request.user)
    favorite_authors = [favorite.following.id for favorite in favorites]
    post_list = Post.objects.select_related(
        'author', 'group'
    ).filter(
        author__in=favorite_authors
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "posts/follow.html", {'page': page, 'paginator': paginator}
    )


@login_required
def profile_follow(request, username):
    if request.user.username != username:
        user = request.user
        author = get_object_or_404(User, username=username)
        follow_count = Follow.objects.filter(
            user=user, following=author.id).count()
        if follow_count == 0:
            Follow.objects.create(user=user, following=author)
            return redirect('profile', username=author)
    return redirect('index')


@login_required
def profile_unfollow(request, username):
    if request.user.username != username:
        user = request.user
        author = get_object_or_404(User, username=username)
        follow_count = Follow.objects.filter(
            user=user, following=author.id).count()
        if follow_count == 1:
            Follow.objects.filter(user=user, following=author).delete()
            return redirect('profile', username=author)
    return redirect('index')
