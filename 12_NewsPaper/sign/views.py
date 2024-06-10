from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User  # модель формы, которую реализует данный дженерик;
    form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем;
    success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму.


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
