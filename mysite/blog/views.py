from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from blog.forms import CommentForm
from blog.forms import VoteForm  # Import the VoteForm
from polls.models import Question,Choice  # Import the Question model

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    poll_form = None
    poll_results = None

    if post.poll:  # Check if the post has an associated poll
        poll_form = VoteForm(post.poll.id)
        if request.method == "POST" and 'choice' in request.POST:
            poll_form = VoteForm(post.poll.id, request.POST)
            if poll_form.is_valid():
                choice = poll_form.cleaned_data['choice']
                choice.votes += 1
                choice.save()
                # After saving the vote, calculate the poll results
                poll_results = Choice.objects.filter(question=post.poll)

    if request.method == "POST" and 'author' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "poll_form": poll_form,
        "poll_results": poll_results,
    }
    return render(request, "blog/detail.html", context)
