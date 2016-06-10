from channels.routing import route
from .consumers import tasker_questions_create

channel_routing = [
    route('tasker-questions-create', tasker_questions_create),
]
