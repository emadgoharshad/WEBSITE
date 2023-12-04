from django.urls import path

from .views import real_video,detail_video,like,subs,upload_video,my_videos,delete_video,update_video,my_subs_video

app_name = 'video'

urlpatterns = [
    path('',real_video,name='videos'),
    path('detail/<int:my_id>',detail_video,name='detail_video'),
    path('like/<int:pk>',like,name='likes'),
    path('subs/<int:pk>',subs,name='subs'),
    path('upload', upload_video, name='upload_video'),
    path('my_videos', my_videos, name='my_videos'),
    path('delete/<int:video_id>', delete_video, name='delete'),
    path('update/<int:pk>', update_video.as_view(), name='update'),
    path('my_subs_video/', my_subs_video, name='my_subs_video'),

]