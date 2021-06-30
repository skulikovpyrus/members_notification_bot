import json
import requests
import hmac
import hashlib
from app import logger


def get_token(login, secret):
    data = {"login": login, "security_key": secret}
    url = "https://api.pyrus.com/v4/auth"
    response = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)

    token = response.json()["access_token"]
    return token


def get_form(form_id, token):
    url = f"https://api.pyrus.com/v4/forms/{form_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
        return
    form = response.json()
    return form


def get_forms(token):
    url = f"https://api.pyrus.com/v4/forms"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
    forms = response.json()["forms"]
    return forms



def get_form_tasks(form_id, token):
    url = f"https://api.pyrus.com/v4/forms/{form_id}/register"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
    tasks = response.json()["tasks"]
    return tasks


def get_task(task_id, token):
    url = f"https://api.pyrus.com/v4/tasks/{task_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
    task = response.json()
    return task["task"]


def get_members(token):
    url = f"https://api.pyrus.com/v4/members"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
    members = response.json()["members"]
    return members


def send_comment(task_id, token, comment):
    url = f"https://api.pyrus.com/v4/tasks/{task_id}/comments"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps(comment)
    )
    if not response.status_code == 200 or "Error" in response.text:
        logger.info(response.text)
    return response


def get_flat_fields(fields, is_form=True):
    res = []
    if not fields:
        return res
    for field in fields:
        res.append(field)
        prop_name = "info" if is_form else "value"

        if field["type"] == "table" and is_form:
            res.extend(field[prop_name]["columns"])
        if field["type"] == "title":
            res.extend(field[prop_name]["fields"])
    return res


def get_field_by_id(fields: list, _id: int):
    field = [field for field in fields if field["id"] == _id]
    if field:
        return field[0]


def get_field_id_by_code(form, code, source_task_id, token):
    flat_fields = [field for field in get_flat_fields(form["fields"]) if "info" in field]
    fields_with_code = list(filter(lambda x: "code" in x["info"], flat_fields))

    field_id = [field["id"] for field in fields_with_code if field["info"]["code"] == code]
    if field_id:
        return field_id[0]

    comment = {"text": f"Не найдено поле по коду {code}, проверьте правильно ли вы ввели код поля"}
    send_comment(source_task_id, token, comment)


def get_field_by_code(form, task, code, token):
    desired_field_id = get_field_id_by_code(form, code, task["id"], token)
    if not desired_field_id:
        logger.info(f"Не найдено поле по коду {code}")
        send_comment(task["id"], token, {"text": f"Не найдено по коду {code}"})
        return

    task_fields = get_flat_fields(task["fields"], is_form=False)
    desired_field = get_field_by_id(task_fields, desired_field_id)
    return desired_field


def get_field_value_by_id(fields, field_id):
    filtered_fields = [field for field in fields if field["id"] == field_id]
    if filtered_fields:
        field = filtered_fields[0]
        if "value" in field:
            field_value = field["value"]
            if field["type"] == "multiple_choice":
                return field_value["choice_names"][0]
            if field["type"] == "form_link":
                task_id = field_value["task_id"]
                return task_id
            return field_value


def add_user_to_approvals_list(task, user_id, comment):
    new_approvals_list = comment["approvals_added"]
    current_step = task["current_step"]
    new_approvals_list[current_step - 1].append({"id": user_id})
    return comment


def prepare_comment(task):
    comment = {"approvals_added": [], "approval_choice": "approved"}
    for _ in range(len(task["approvals"])):
        comment["approvals_added"].append([])
    return comment
