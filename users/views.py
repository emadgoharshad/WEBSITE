from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404


from .models import User
from video.models import Subscriber,Video
from .forms import RegisterForm,LoginForm,EditForm

def home(request):
    return render(request,'account/home.html')



def profile_view(request,*args,**kwargs):
    user = request.user
    user_id = kwargs.get('user_id')
    context = {}

    subs = Subscriber.objects.get_or_create(user=User.objects.get(id=user_id))[0]


    try:
        account = User.objects.get(pk=user_id)
    except:
        return HttpResponse('something not user')



    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['avatar'] = account.avatar

        is_self = True
        is_subs = False
        if not user.is_authenticated or user != account:
            is_self = False

        if user in subs.subscribers.all():
            is_subs = True
        else:
            is_subs = False

        count_subs = subs.subscribers.all().count()
        count_videos = Video.objects.filter(user=account).count()



        context['is_self'] = is_self
        context['is_sub'] = is_subs
        context['count_subs'] = count_subs
        context['count_video'] = count_videos





    return render(request,'account/profile.html',context)





def register(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticate as " + str(user.email))
    dic = {}

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=password)
            login(request,account)
            return redirect('users:home')
        else :
            dic['form'] =form
    else:
        form = RegisterForm()
        dic['form'] = form

    return render(request,'account/register.html',dic)


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('users:home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect('users:home')


    else:
        form = LoginForm()
    dic = {
        'form':form
    }

    return render(request,'account/login.html',dic)


def logout_view(request):
    logout(request)
    return redirect('users:home')


def edit_profile(request,*args,**kwargs):

    if not request.user.is_authenticated:
        redirect('users:login')

    user = request.user
    user_id = kwargs.get('user_id')
    account = User.objects.get(pk=user_id)
    if user.pk != account.pk:
        return HttpResponse('you can edit this profile')





    dic = {}

    if request.POST:
        form = EditForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:home')

        else:
            form = EditForm(request.POST,instance=user,initial={
                'id':account.id,
                'username':account.username,
                'email':account.email,
                'avatar':account.avatar,
            })
            dic['form'] = form
    else:
        form = EditForm(initial={
            'id': account.id,
            'username': account.username,
            'email': account.email,
            'avatar': account.avatar,
        })
        dic['form'] = form
    dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request,'account/edit_profile_account.html',dic)


















