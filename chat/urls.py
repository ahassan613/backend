from django.urls import path, re_path
from .views import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcustomerroom/', AddRoom.as_view()),
    path("chatusers/<int:id>/", GetAllRooms.as_view()),
    path("messages/<int:roomid>/<int:items>/", GetMessages.as_view()),

    # url(r'^messages/(?P<id>\w{0,50})/(?P<items>[-\w.,/_\-].+?)$', views.GetMessagesByRoomName),

    # path('getroom/', GetRoom.as_view()),


    # url(r'^allrooms/', views.AddandGetRooms),



    path('<str:room_name>/', views.room, name='room'),
]
