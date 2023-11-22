from django.urls import path, re_path

from websockets.consumers import GroupsConsumer
from .views import (ClearGroupMessagesConfirmView, ClearGroupMessagesView,
                   CreateGroupView, DeleteGroupView, EditGroupView,
                   GroupsListView, GroupView)

app_name = 'groups'

urlpatterns = [
    path('to/<slug:group_slug>', GroupView.as_view(), name='group'),
    path('create', CreateGroupView.as_view(), name='create'),
    path('edit/<slug:group_slug>', EditGroupView.as_view(), name='edit'),
    path('delete/<slug:group_slug>', DeleteGroupView.as_view(), name='delete_group'),
    path('clear_messages_confirm/<slug:group_slug>', ClearGroupMessagesConfirmView.as_view(),
         name='clear_messages_confirm'),
    path('clear_messages/<slug:group_slug>', ClearGroupMessagesView.as_view(), name='clear_messages'),
    path('', GroupsListView.as_view(), name='groups_list'),

    re_path(r'ws/chat/(?P<group_name>\w+)/$',
            GroupsConsumer.as_asgi()),
]
