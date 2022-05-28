from app import app
from flask import json

def test_add_actor():
    response = app.test_client().post(
        '/actors',
        data = json.dumps(
            {
                'name': 'Jack Nicholson'
            }
        ),
        content_type = 'application/json',
    )

    assert response.status_code == 200