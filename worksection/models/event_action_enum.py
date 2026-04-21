from enum import Enum


class EventActionEnum(str, Enum):
    Post = 'post'
    Update = 'update'
    Delete = 'delete'
    TaskClose = 'close'
    TaskReopen = 'reopen'