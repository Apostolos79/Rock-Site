from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView, TemplateView
from accounts.models import Profile

class SignUp(CreateView):
    """docstring for SignUp."""
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


# class UpdateProfile(TemplateView):
#     model = Profile
#
#     def get_context_data(self, **kwargs):
#         self.popularity +=1
#         self.save()
#         kwargs['popularity'] = self.popularity
#         return super().get_context_data(**kwargs)
#
#     def get_queryset(self):
#         print(self.kwargs.get('username'))
#         self.user = User.objects.get(username__iexact=self.kwargs.get("username"))
#         print(self.user)
#         return self.user
