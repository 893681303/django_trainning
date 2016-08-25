from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from .models import Posts
from .forms import PostsForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from urllib.parse import quote_plus
from django.utils import timezone

# Create your views here.


def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Item Saved", extra_tags="html_tags")
        return HttpResponseRedirect(reverse('posts:detail', kwargs={"slug": instance.slug}))
    context = {
        'title': 'User',
        'form': form,
    }
    return render(request, 'form.html', context)

def posts_list(request):
    object_list = Posts.objects.filter(draft=False).filter(publish__lte=timezone.now()).order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(object_list, 2) # Show 2 contacts per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    context = {
        'title': 'Index',
        'objects': objects,
    }
    return render(request, 'index.html', context)


def posts_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Posts, id=id)
    form = PostsForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href=''>Item</a> Saved", extra_tags="html_tags")
        return HttpResponseRedirect(reverse('posts:detail', kwargs={"id": instance.id}))

    context = {
        'title': 'User',
        'form': form,
    }
    return render(request, 'form.html', context)


def posts_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Posts, id=id)
    instance.delete()
    return HttpResponse('Deleted Successfully')


def posts_detail(request, slug=None):
    instance = get_object_or_404(Posts, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'title': 'User',
        'instance': instance,
        'share_string': share_string,

    }
    return render(request, 'detail.html', context)
    #return HttpResponse('<h1>List</h1>')
