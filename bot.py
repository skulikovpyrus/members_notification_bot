from utils import get_form, get_flat_fields, get_token, get_members, get_field_id_by_code, get_field_by_code, \
    send_comment
from app import logger
from strategy import NotificationStrategy, strategy_type_ids


class NotificationBot:
    def __init__(self, task, token, settings):
        self.task = task
        self.token = token
        self.settings = settings
        self.form = get_form(self.task["form_id"], self.token)

        self.strategy = self.define_notification_strategy()
        self.members = get_members(self.token)

    def define_notification_strategy(self):
        notification_field = get_field_by_code(self.form, self.task, self.settings["notification_field"], self.token)
        if "value" in notification_field:
            notification_type_id = notification_field["value"]["choice_id"]
            _strategy: NotificationStrategy = strategy_type_ids[notification_type_id]
            return _strategy

