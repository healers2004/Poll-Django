from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from blog.models import Post, Comment, Feedback, ContactUsPageText
from blog.forms import VoteForm, FeedbackForm, CommentForm
from polls.models import Question,Choice
from taggit.models import Tag
from django.db.models import Count
from .utils import get_geolocation
from django.core.paginator import Paginator

def blog_index(request):
    posts_list = Post.objects.all().order_by("created_on")
    
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')
    context = {
        "posts": posts,
        "tags": tags,
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

    if post.poll:  # Checking if the post has an associated poll
        poll_form = VoteForm(post.poll.id)
        if request.method == "POST" and 'choice' in request.POST:
            poll_form = VoteForm(post.poll.id, request.POST)
            if poll_form.is_valid():
                choice = poll_form.cleaned_data['choice']
                choice.votes += 1
                choice.save()
                # After saving the vote, calculating the poll results
                poll_results = Choice.objects.filter(question=post.poll)

    if request.method == "POST" and 'author' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
                state=Comment.State.PENDING,  # Setting the initial state to Pending
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post, state=Comment.State.APPROVED)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "poll_form": poll_form,
        "poll_results": poll_results,
    }
    return render(request, "blog/detail.html", context)

def blog_tag(request, tag_slug):
    posts = Post.objects.filter(tags__slug=tag_slug).order_by("-created_on")
    if not posts:
        print(f"No posts found for tag: {tag_slug}")
    context = {
        'posts': posts,
        'tag': tag_slug
    }
    return render(request, 'blog/tag.html', context)

class GeolocationView(View):
    def get(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)
        geolocation_data = get_geolocation(ip_address)
        return JsonResponse(geolocation_data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Public IP for local testing
        if ip == '127.0.0.1' or ip.startswith('192.168.'):
            ip = '8.8.8.8'  # Google's public DNS server IP for testing

        return ip

def about(request):
    return render(request, "blog/about.html")

def contact(request):
    form = FeedbackForm()
    success = False

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            form = FeedbackForm()  # Reset the form after submission
            success = True

    contact_text = ContactUsPageText.objects.first()

    return render(request, "blog/contact.html", {
        'form': form,
        'success': success,
        'contact_text': contact_text,
    })
