from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.views import View 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from blog.models import News
from django.views.generic.detail import DetailView

class UserLogin(View):
    form_class = UserLoginForm
    template_name = "account/login-page.html"
    
    def get(self, request):
        form =  self.form_class
        return render(request=request, template_name=self.template_name, context={'form':form})

    def post(self, request):
        next = request.GET.get('next')
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request=request, username = cd['username'] ,password = cd['password'])
            if user is not None:
                 login(request=request, user=user)
                 messages.success(request=request, message='با موفقیت وارد سایت شدید')
                 if next:
                     return redirect(next)
                 return redirect(to='blog:index')
            messages.error(request=request, message='رمز یا نام کاربری اشتباه است ')
        return render(request=request, template_name = self.template_name, context={'form':form})

class UserRegister(View):
    form_class = UserRegisterForm
    template_name = "account/sign-in-page.html"
    
    def get(self, request):
        form =  self.form_class
        return render(request=request, template_name=self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
             cd = form.cleaned_data
             user= User.objects.create_user(cd['username'],cd['email'],cd['password'])
             login(request, user)
             messages.success(request, message='با موفقیت عضو سایت شدید')
             return redirect(to='blog:index')
        messages.error(request, message='لطفا فیلد ها را با مقادیر درست پر کنید')
        return render(request, template_name = self.template_name, context={'form':form})


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, message='با موفقیت از  سایت خارج شدید')
        return redirect(to='blog:index')

    
class UserNewsListView(ListView):
    model = News
    paginate_by = 2
    template_name = 'blog/user-news-list-page.html'

    def get_queryset(self):
        print(self.request.GET.get('user'))
        queryset = News.objects.filter(author__id = self.kwargs['user'])
        return queryset

    
class UserDetailView(DetailView):
    
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user'
    slug_url_kwarg = "user"
    slug_field = "username" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user =  get_object_or_404(User, username= self.kwargs['user'])
        if self.request.user == user:
            context['self_profile'] = True
        return context
    
    def get_queryset(self):
        return super().get_queryset()


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user.profile, files=request.FILES)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'پروفایل شما با موفقیت تغییر یافت ')
            return redirect('blog:index')
    else:
        form = ProfileEditForm(instance=user.profile, initial={'email':request.user.email})
    return render(request, 'account/edit_profile.html', {'form':form})
