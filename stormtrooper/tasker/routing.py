from channels.routing import route
from .consumers import tasker_questions_create, tasker_export_create, tasker_export_send

channel_routing = [
    route('tasker-questions-create', tasker_questions_create),
    route('tasker-export-create', tasker_export_create),
    route('tasker-export-send', tasker_export_send)
]
