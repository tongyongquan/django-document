from django.urls import path, include
from . import views

app_name = 'comment'
urlpatterns = [

    path("comment", views.write_comment, name='comment'),
    path("replies/<int:comment_id>/", views.comment_replies, name='replies'),
    path("reply", views.reply, name='reply'),
    path("reply_reply", views.reply_reply, name='reply_reply'),
    path("read_comment/<int:story_id>/", views.read_comment, name='read_comment'),
    path("comment_good", views.comment_good, name='comment_good'),
    path("reply_good", views.reply_good, name='reply_good'),
]
