from abc import ABC, abstractmethod
from utils import add_user_to_approvals_list, prepare_comment, send_comment


class NotificationStrategy(ABC):
    @abstractmethod
    def notify_users(self, members, task, token, positions=None, departments=None):
        pass


class NotifyAllUsers(NotificationStrategy):
    def notify_users(self, members, task, token, positions=None, departments=None):
        comment = prepare_comment(task)
        for member in members:
            comment = add_user_to_approvals_list(task, member["id"], comment)
        send_comment(task["id"], token, comment)


class NotifyUsersByPosition(NotificationStrategy):
    def notify_users(self, members, task, token, positions=None, departments=None):
        if not positions:
            return
        comment = prepare_comment(task)
        leaders = [member for member in members if "position" in member and member["position"] in positions]
        if leaders:
            for leader in leaders:
                comment = add_user_to_approvals_list(task, leader["id"], comment)
            send_comment(task["id"], token, comment)


class NotifyUsersByDepartment(NotificationStrategy):
    def notify_users(self, members, task, token, positions=None, departments=None):
        if not departments:
            return
        comment = prepare_comment(task)
        employees = [member for member in members if "department_name" in member
                     and member["department_name"] in departments]
        if employees:
            for employee in employees:
                comment = add_user_to_approvals_list(task, employee["id"], comment)
            send_comment(task["id"], token, comment)


strategy_types = {
    1: NotifyAllUsers(),
    2: NotifyUsersByPosition(),
    3: NotifyUsersByDepartment(),
    4: NotifyUsersByDepartment()
}
