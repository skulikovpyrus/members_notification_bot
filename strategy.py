from abc import ABC, abstractmethod
from utils import add_user_to_approvals_list, prepare_comment, send_comment


class NotificationStrategy(ABC):
    @abstractmethod
    def notify_users(self, members, task, token):
        pass


class NotifyAllUsers(NotificationStrategy):
    def notify_users(self, members, task, token):
        comment = prepare_comment(task)
        for member in members:
            comment = add_user_to_approvals_list(task, member["id"], comment)
        send_comment(task["id"], token, comment)


class NotifyLeaders(NotificationStrategy):
    def notify_users(self, members, task, token):
        comment = prepare_comment(task)
        leader_positions = ["Начальник", "Директор", "Руководитель"]
        leaders = [member for member in members if "position" in member and member["position"] in leader_positions]
        if leaders:
            for leader in leaders:
                comment = add_user_to_approvals_list(task, leader["id"], comment)
            send_comment(task["id"], token, comment)


class NotifyOfficeEmployees(NotificationStrategy):
    def notify_users(self, members, task, token):



class NotifyProductionEmployees(NotificationStrategy):
    def notify_users(self, members, task, token):
        pass


strategy_type_ids = {
    0: NotifyAllUsers,
    1: NotifyLeaders,
    2: NotifyOfficeEmployees,
    3: NotifyProductionEmployees
}
