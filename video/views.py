from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from .models import Video,Comment,Subscriber
from users.models import User
from .forms import CommentForm

def real_video(request):

    try:
        videos = Video.objects.all()
    except:
         HttpResponse('dont find')



    context = {
        'videos':videos,
    }

    return render(request,'video/new_release_video.html',context)


def detail_video(request,my_id):
    video = get_object_or_404(Video,pk=my_id)

    count_likes = video.count_like()

    new_comment = None
    comments = video.comments.all()
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.video = video
            new_comment.user = request.user
            new_comment.save()
        else:
            form = CommentForm()
    else:
        form = CommentForm()


    ip = request.META.get('REMOTE_ADDR')
    ips = request.session.get('viewed_ips',[])
    if ip not in ips:
        video.views += 1
        video.save()
        ips.append(ip)
    request.session['viewed_ips'] = ips


    is_self = True
    is_like = False

    if not request.user.is_authenticated or request.user != video.user:
        is_self = False

    if video.likes.filter(pk=request.user.id):
        is_like = True


    dic = {
        'video':video,
        'is_self':is_self,
        'is_like':is_like,
        'count_like':count_likes,
        'comment':comments,
        'comment_form':form,
        'new_comment':new_comment,

    }

    return render(request,'video/detail_video.html',dic)




def like(request,pk):
    is_liked = False
    video = get_object_or_404(Video,id = request.POST.get('video_id'))

    if video.likes.filter(id=request.user.id):
        video.likes.remove(request.user)
        is_liked = False
    else:
        video.likes.add(request.user)
        is_liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subs(request,pk):
        is_subs = False
        subscriber = get_object_or_404(Subscriber,user = User.objects.get(id=pk))

        if subscriber.subscribers.filter(id=request.user.id):
            subscriber.subscribers.remove(request.user)
            is_subs = False
        else:
            subscriber.subscribers.add(request.user)
            is_subs = True

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def upload_video(request):
    if request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        file = request.FILES['fileName']
        user = request.user
        video = Video(user=user,title=title,desc=desc,file=file)
        video.save()

        return redirect('video:videos')
    return render(request,'video/upload_video.html')



def my_videos(request):

    my_video = Video.objects.filter(user=request.user).order_by('pub_date')

    dic = {
        'my_video':my_video,
    }

    return render(request,'video/my_videos.html',dic)



def delete_video(request,video_id):
    video = get_object_or_404(Video,id=video_id)

    if request.POST:
        video.delete()

    return HttpResponseRedirect(reverse('video:videos'))


class update_video(UpdateView):
    model = Video
    template_name = 'video/edit-video.html'
    fields = ('title','desc')

    def get_success_url(self):
        return reverse('video:my_videos')



def my_subs_video(request):
    subscribers = Subscriber.objects.filter(subscribers = request.user)

    list = []
    for item in subscribers:
        list.append(item.user.id)



    videos = Video.objects.filter(user__id__in=list)

    dic = {
        'my_subs_videos':videos
    }

    return render(request,'video/my_subscribers.html',dic)













