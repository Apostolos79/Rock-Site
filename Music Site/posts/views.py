from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import generic
from django.views.generic import DetailView, UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from posts.models import Post
from django.db.models import F
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse

# pip install django-braces
from braces.views import SelectRelatedMixin

from . import forms
from . import models

import operator
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"
    paginate_by = 3

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class ThumbsUpPosts(generic.ListView):
    model = Post
    # context_object_name = 'posts'
    # template_name = 'posts/post_detail.html'
    # success_url = reverse_lazy("posts:all")

    # def get_context_data(self, **kwargs):
    #     self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
    #     u = User.objects.get(username=self.post.user.username)
    #     pop = u.profiles.first()
    #     self.post.thumbsup +=1
    #     pop.popularity +=1
    #     pop.save()
    #     #print(pop.popularity)
    #     self.post.save()
    #     kwargs['post'] = self.post
    #     return super().get_context_data(**kwargs)

    # def get_success_url(self):
    #     return HttpResponse(status=204)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
            u = User.objects.get(username=self.post.user.username)
            pop = u.profiles.first()
            self.post.thumbsup = F('thumbsup') + 1
            pop.popularity = F('popularity') + 1
            pop.save()
            print(self.post.thumbsup)
            self.post.save()
            kwargs['post'] = self.post
            return redirect(self.post)
        else:
            return HttpResponseForbidden()

    # def get_queryset(self):
    #     #print(self.kwargs.get('pk'))
    #     self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
    #     #print(self.post)
    #     return self.post


class ThumbsDownPosts(generic.ListView):
    model = Post
    # context_object_name = 'posts'
    # template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        #self.post.thumbsdown += 1
        self.post.thumbsdown = F('thumbsdown') + 1
        #print(self.post.user)
        self.post.save()
        kwargs['post'] = self.post
        return super().get_context_data(**kwargs)

    # def get_queryset(self):
    #     print(self.kwargs.get('pk'))
    #     self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
    #     #print(self.post)
    #     return self.post


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


# class SearchListView(generic.ListView):
#     """
#     Display a List page filtered by the search query.
#     """
#     model = models.Post
#     template_name = 'posts/search_post_results.html'
#     paginate_by = 3
#
#     def get_queryset(self):
#
#         if 'q' in self.request.GET:
#             q = self.request.GET['q']
#             queryset = super().get_queryset()
#             return queryset.filter(Q(message__icontains=q) | Q(user__username__icontains=q))
#         else:
#             return models.Post.objects.none()


class SearchListView(generic.ListView):
    model = models.Post
    template_name = 'posts/search_post_results.html'

    def get_queryset(self):

        if 'q' in self.request.GET:
            q = self.request.GET['q']
            objects = Post.objects.filter(Q(message__icontains=q) | Q(user__username__icontains=q))
        else:
            objects = Post.objects.all()

        return objects
