from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


from .forms import LoginForm, RegisterForm

User = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, "home/index.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # 校验通过
            if user:
                login(request, user)
                return redirect("front:home")
            # 校验失败
            else:
                form.add_error(None, "用户名或密码错误")
                return render(request, "auth/login.html", {"form": form})
        else:
            return render(request, "auth/login.html", {"form": form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                form.add_error(None, "用户名已存在")
                return render(request, "auth/register.html", {"form": form})

            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("front:home")
        else:
            form.add_error(None, "注册失败")
            return render(request, "auth/register.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect("front:home")
