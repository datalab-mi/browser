import os
import pytest
from pathlib import Path

from elasticsearch import Elasticsearch

from application import create_app
from flask_jwt_extended import create_access_token

INDEX_NAME = 'bld'

USER_DATA = 'tests/iga/data'
filename = 'ignit_pnigitis.pdf'

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def access_headers(app, role):
    """header with token with role logic inside."""
    with app.test_request_context():
        access_token = create_access_token(role, fresh=True)
    return {'Authorization': 'Bearer %s'%access_token}

@pytest.fixture
def search_data():
    return dict(index_name=INDEX_NAME,
                must=[{"multi_match": {"fields": ["titre", "question", "reponse"], "query": "moteur de recherche"}}],
                highlight=["question","reponse","pieces jointes"])

@pytest.fixture
def es():
    return Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])

@pytest.fixture
def dummy_index():
    return {
          "settings": {
            "analysis": {
              "filter" : {
                "my_synonym": {
                  "type": "synonym",
                  "synonyms": [
                    "chat => lion"
                      ]
                  }
            },
              "analyzer": {
                "my_analyzer": {
                  "tokenizer": "standard",
                  "filter": [
                    "my_synonym"
                    ]
                  }
                }
            }
          },
          "mappings":{
              "properties": {
                 "content": {
                    "type": "text",
                    "analyzer" : "my_analyzer",
                    "search_analyzer" : "my_analyzer"
                }
              }
            }
        }

@pytest.fixture
def form_to_upload():
    yield {"file": (open(USER_DATA + '/' + filename, "rb"), filename),
            "mots cles": '["- docker","- python","babar"]'
                }

@pytest.fixture
def bad_form_to_upload():
    yield {"file": (open(USER_DATA + '/' + filename, "rb"), filename),
            "date": '14/1451-52'
                }

@pytest.fixture
def file_name():
    return filename

@pytest.fixture
def index_name():
    yield INDEX_NAME

@pytest.fixture
def pdf_file():
    yield filename

@pytest.fixture
def sections():
    yield [{'key': 'SITE', 'array':False},
            {'key': 'DIRECTION', 'array':False},
            {'key': 'DOMAINE', 'array':False},
            {'key': 'TITRE', 'array':False},
            {'key': 'Mots clés', 'array':True},
            {'key': 'Date', 'array':False},
            {'key': 'Question', 'array':False},
            {'key': 'Réponse', 'array':False},
            {'key': 'Réponse', 'array':False},
            {'key': 'Pièces jointes', 'array':True},
            {'key': 'Liens', 'array':False},
            {'key': 'Références', 'array':False}
            ]
