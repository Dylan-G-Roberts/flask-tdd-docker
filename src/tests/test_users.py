import json
from src.api.models import User
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'dylan',
            'email': 'dylan@test.org'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'dylan@test.org was added!' in data['message']

def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'badusername': 'ohno'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'example',
            'email': 'dylan@test.org'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'example',
            'email': 'dylan@test.org'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400 
    assert 'Sorry. That email already exists' in data['message']

def test_single_user(test_app, test_database, add_user):
    user = add_user('dylan', 'dylan@example.com')
    client = test_app.test_client()
    resp = client.get(
        f'/users/{user.id}'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'dylan' in data['username']
    assert 'dylan@example.com' in data['email'] 

def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        f'/users/{9999}'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 9999 does not exist' in data['message']

def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user('test1', 'test1@test.com')
    add_user('test2', 'test2@test.com') 
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2 
    assert 'test1' in data[0]['username'] 
    assert 'test1@test.com' in data[0]['email']
    assert 'test2' in data[1]['username'] 
    assert 'test2@test.com' in data[1]['email']
