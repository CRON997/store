from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth,messages

from users.forms import UserLoginForm,UserRegistrationForm,UserProfileForm
from products.models import Basket
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username= request.POST["username"]
            password= request.POST['password']
            user = auth.authenticate(username=username,password = password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form':form}
    return render(request,'users/login.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'users/register.html',context)

def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data = request.POST,instance=user,files = request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
    baskets = Basket.objects.filter(user=user)
    total_quantity = sum(basket.quantity for basket in baskets)
    total_sum = sum(basket.sum() for basket in baskets)
    context = {'form':form,
               'baskets':baskets,
               'total_quantity':total_quantity,
               'total_sum':total_sum}
    return render(request,'users/profile.html',context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


