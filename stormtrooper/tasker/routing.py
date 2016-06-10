from channels.routing import route
from .consumers import tasker_questions_create, tasker_export_create

channel_routing = [
    route('tasker-questions-create', tasker_questions_create),
    route('tasker-export-create', tasker_export_create)
]
