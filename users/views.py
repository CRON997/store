from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib import auth,messages
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView,UpdateView
from users.forms import UserLoginForm,UserRegistrationForm,UserProfileForm

from django.contrib.messages.views import SuccessMessageMixin
from products.models import Basket
from users.models import User, EmailVerification
from common.views import TitleMixin

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
    context = {'title': 'ElectroHub - Authorization' ,'form':form}
    return render(request,'users/login.html',context)

class UserRegistrationView(TitleMixin, SuccessMessageMixin,CreateView):
    model = User
    form_class = UserRegistrationForm
    title = 'ElectroHub - Registration'
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'You have successfully checked in!'


    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        return context

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
    context = {'title':'ElectroHub - Profile',
                'form':form,
               'baskets':baskets,
               'total_quantity':total_quantity,
               'total_sum':total_sum}
    return render(request,'users/profile.html',context)
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin,TemplateView):
    title = 'ElectroHub - Email Confirmation'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email = kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user = user, code = code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email  = True
            user.save()
            return  super(EmailVerificationView,self).get(request,*args,**kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

