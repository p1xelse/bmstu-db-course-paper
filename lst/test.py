import pytest
from confest import db_all_tables, api_url, clean_users, auth_user
import requests
import classes
from utils import compare_alch_with_dict, \
    compare_json, compare_json_arr, objects_to_dicts
import time

elem_url = "project"

def test_create(db_all_tables, api_url, auth_user):
    input_data = {
        "about": "string",
        "color": "string",
        "is_private": False,
        "name": "string"
    }

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.post(f"{api_url}/{elem_url}/create", 
                             json=input_data, headers=headers)
    project = db_all_tables.query(classes.Project).first()

    excepted = input_data

    assert response.status_code == 200
    assert compare_alch_with_dict(project, excepted)

def test_edit(db_all_tables, api_url, auth_user):
    user_id = auth_user["id"]
    project_db_json = {
        "about": "string",
        "color": "string",
        "is_private": False,
        "user_id": user_id,
        "name": "string"
    }

    project = classes.Project(**project_db_json)
    db_all_tables.add(project)
    db_all_tables.commit()


    input_data = {
        "id": project.id,
        "about": "string",
        "color": "string",
        "is_private": False,
        "name": "new_name"
    }

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.post(f"{api_url}/{elem_url}/edit", 
                             json=input_data, headers=headers)
    db_all_tables.refresh(project)
    assert response.status_code == 200

    project_db_new = db_all_tables.query(classes.Project).first()
    excepted = input_data

    assert compare_alch_with_dict(project_db_new, excepted)

@pytest.mark.negative
def test_edit_not_found(db_all_tables, api_url, auth_user):
    user_id = auth_user["id"]
    input_data = {
        "id": 1,
        "about": "string",
        "color": "string",
        "is_private": False,
        "name": "new_name"
    }

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.post(f"{api_url}/{elem_url}/edit", 
                             json=input_data, headers=headers)
    assert response.status_code == 404

def test_delete(db_all_tables, api_url, auth_user):
    user_id = auth_user["id"]
    project_db_json = {
        "about": "string",
        "color": "string",
        "is_private": False,
        "user_id": user_id,
        "name": "string"
    }

    project = classes.Project(**project_db_json)
    db_all_tables.add(project)
    db_all_tables.commit()

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.delete(f"{api_url}/{elem_url}/{project.id}", 
                               headers=headers)
    assert response.status_code == 204

    count = db_all_tables.query(classes.Project).count()
    db_all_tables.commit()
    assert count == 0

@pytest.mark.negative
def test_delete_not_found(db_all_tables, api_url, auth_user):
    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.delete(f"{api_url}/{elem_url}/1", headers=headers)
    assert response.status_code == 404

@pytest.mark.negative
def test_create_empty(db_all_tables, api_url, auth_user):
    input_data = {}

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.post(f"{api_url}/{elem_url}/create", 
                             json=input_data, headers=headers)

    assert response.status_code != 200


def test_get_by_id(db_all_tables, api_url, auth_user):
    user_id = auth_user["id"]

    project_json = {
        "user_id": user_id,
        "name": 'New project',
        "about": "Some description",
        "color": 'blue',
        "is_private": True,
    }

    project = classes.Project(**project_json)
    db_all_tables.add(project)
    db_all_tables.commit()

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.get(f"{api_url}/{elem_url}/{project.id}", 
                            headers=headers)
    assert response.status_code == 200

    body = response.json()['body']
    assert compare_json(body, project_json)

@pytest.mark.negative
def test_get_by_id_not_found(db_all_tables, api_url, auth_user):
    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.get(f"{api_url}/{elem_url}/1", 
                            headers=headers)
    assert response.status_code == 404

def test_get_my(db_all_tables, api_url, auth_user):
    user_id = auth_user["id"]

    project_json_1 = {
        "user_id": user_id,
        "name": 'New project',
        "about": "Some description",
        "color": 'blue',
        "is_private": True,
    }

    project_1 = classes.Project(**project_json_1)
    db_all_tables.add(project_1)
    db_all_tables.commit()

    project_json_2 = {
        "user_id": user_id,
        "name": 'New project 2',
        "about": "Some description",
        "color": 'blue',
        "is_private": True,
    }

    project_2 = classes.Project(**project_json_2)
    db_all_tables.add(project_2)
    db_all_tables.commit()

    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.get(f"{api_url}/me/{elem_url}s",
                            headers=headers)
    assert response.status_code == 200

    body = response.json()['body']

    excepted_arr = objects_to_dicts([project_1, project_2])
    assert compare_json_arr(body, excepted_arr)

def test_get_my_empty(db_all_tables, api_url, auth_user):
    headers = {"Cookie": auth_user["Cookie"]}
    response = requests.get(f"{api_url}/me/projects", headers=headers)
    assert response.status_code == 200

    body = response.json()['body']

    excepted_arr = []
    assert compare_json_arr(body, excepted_arr)