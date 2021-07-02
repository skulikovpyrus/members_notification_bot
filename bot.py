from utils import get_form, get_members, get_field_by_code
from strategy import NotificationStrategy, strategy_types


class NotificationBot:
    def __init__(self, task, token, settings):
        self.task = task
        self.token = token
        self.settings = settings
        self.form = get_form(self.task["form_id"], self.token)

        self.members = get_members(self.token)
        self.notification_field_code = self.settings["notification_field"]
        self.office_departments = self.settings["office_departments"]
        self.production_departments = self.settings["production_departments"]
        self.leader_positions = ["Начальник", "Директор", "Руководитель"]

    @staticmethod
    def define_notification_strategy(notification_type_id):
        try:
            _strategy: NotificationStrategy = strategy_types[notification_type_id]
            return _strategy
        except KeyError:
            print("Нет типа оповещения с таким ID")

    def main(self):
        notification_field = get_field_by_code(self.form, self.task, self.notification_field_code, self.token)
        if notification_field and "value" in notification_field:
            notification_type_id = notification_field["value"]["choice_id"]

            _strategy = NotificationBot.define_notification_strategy(notification_type_id)

            # если нужно уведомить всех пользователей
            if notification_type_id == 1:
                _strategy.notify_users(self.members, self.task, self.token)

            # если нужно уведомить только руководиителей
            if notification_type_id == 2:
                _strategy.notify_users(self.members, self.task, self.token, positions=self.leader_positions)

            # если нужно уведомить только сотрудников офиса
            if notification_type_id == 3:
                _strategy.notify_users(self.members, self.task, self.token, departments=self.office_departments)

            # если нужно уведомить только сотрудников производства
            if notification_type_id == 4:
                _strategy.notify_users(self.members, self.task, self.token, departments=self.production_departments)
