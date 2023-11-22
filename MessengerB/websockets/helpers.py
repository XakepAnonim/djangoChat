from chats.models import Chat
from django.shortcuts import get_object_or_404
from groups.models import Group
from users_messages.models import DailyChatMessages, DailyGroupMessages

from .connection_types import CHATS_CONNECTION, GROUPS_CONNECTION
from .errors import ConnectionTypeDoesNotExist


def get_group_slug(connection_name: str) -> str:
    """
    Убирает GROUPS_CONNECTION из имени подключения и возвращает slug группы.
    Если имя подключения не соответствует подключению группы, то возвращается None

    Args:
        connection_name (str): имя подключения, для групп - GROUPS_CONNECTION_<group_slug>

    Returns:
        str: slug группы

     Raises:
        ConnectionTypeDoesNotExist: несуществующий тип подключения
    """
    if connection_name.startswith(GROUPS_CONNECTION):
        return connection_name[len(GROUPS_CONNECTION) + 1:]
    raise ConnectionTypeDoesNotExist("Данный тип подключения не существует!")


def get_group_daily_messages(group_slug: str) -> DailyGroupMessages:
    group: Group = get_object_or_404(Group, pk=group_slug)

    return DailyGroupMessages.objects.get(group=group)


def get_chat_id(connection_name: str) -> str:
    """
    Убирает CHATS_CONNECTION из имени подключения и возвращает id чата.
    Если имя подключения не соответствует подключению чата, то возвращается None

    Args:
        connection_name (str): имя подключения, для чатов - CHATS_CONNECTION_<chat_id>

    Returns:
        int: id чата

    Raises:
        ConnectionTypeDoesNotExist: несуществующий тип подключения
    """
    if connection_name.startswith(CHATS_CONNECTION):
        return int(connection_name[len(CHATS_CONNECTION) + 1:])

    raise ConnectionTypeDoesNotExist("Данный тип подключения не существует!")


def get_chat_daily_messages(chat_id: int) -> DailyChatMessages:
    chat: Chat = get_object_or_404(Chat, pk=chat_id)

    return DailyChatMessages.objects.get(chat=chat)
