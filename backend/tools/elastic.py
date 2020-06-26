# -*- coding: utf-8 -*-
"""Fichier de backend pour gérer les requettes elasticsearch"""

import elasticsearch
from elasticsearch import Elasticsearch
import os
import base64
import json
import logging
import datetime
from os.path import expanduser
from os import environ
import unicodedata
from datetime import date
from copy import deepcopy
from pathlib import Path
from shutil import copyfile
import pandas as pd
from tools.converter import pdf2json, save_json


def empty_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            empty_tree(child)


#On établit une connection
es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])
indices = elasticsearch.client.IndicesClient(es)

def simple_request(INDEX_NAME):
    request = {
        "query": {
            "match_all" : {}
            }
    }

    #D = es.search(index=str(INDEX_NAME), size=15, body=request)
    D = es.search(index=str(INDEX_NAME_prop), size=15, body=request)
    return D['hits']['hits']

def build_query(req:str, index_name:str,
        glossary_file=None, expression_file=None,
        from_date=None, to_date=None, author=None) -> dict:
    """
    Build the body of the query
    Args:
        index_name : Le nom de l'index où on effectue la recherche
        req : la requête entrèe par l'utilisateur
        expression_file : Le lien pour la liste des expressions clés analysée
        glossary_file : Fichier glossaire
    Returns:
        dict
    """
    # process gloassary
    if glossary_file:
        with open(glossary_file, 'r') as f:
            content = f.read()
        list_glossary = [x.split('=>') for x in str(content).split(
                                '\n') if '=>' in x]

        dic_glossary = {x[0].strip() : x[1].replace(
                        ',', '').strip() for  x  in list_glossary}
        #print(dic_glossary)

        # If user input contains acronym in glossary, add it to req
        for key, val in dic_glossary.items():
            if key in [word.lower() for word in req.split(' ')]:
                req = req + ' ' + val

    if expression_file:
        # process expression
        with open(expression_file, 'r') as f:
            content = f.read()
        list_expression = [x.split('=>')[1] for x in content.split(
                '\n')[:-1] if '=>' in x] # last empty line
        list_expression = [x.replace('_','').strip() for x in list_expression]

    else:
        list_expression = []
    # TODO : process all keyword???
    # Liste_acronyme

    print(req)
    #Au début on va analyser la requête

    body = {'analyzer':"my_analyzer", "text": req}
    analyse = indices.analyze(index= index_name, body = body)

    analyzed = [ananyse_tokens['token'] for ananyse_tokens in analyse["tokens"]]

    length_of_request = len(analyzed)

    #------------------------Application du filtre 1 -----------------------------
    T = False
    Bande = False
    """ all keyword???
    Bande = False
    for keyword in Liste_acronyme:
        if keyword in analyzed:
            T = True
            break
    """
    # find expression in the request
    req_expression = []


    for expression in list_expression:
        if expression in analyzed :
            req_expression.append(expression)
            print('req_expression :')
            print(req_expression)
    #import pdb; pdb.set_trace()

    body = { "query": {
                    "bool": {
                        "must": [],
                        "filter": [],
                        "should": [],
                        "must_not": []
                                }
                        },
                    "highlight" : {
                        "pre_tags" : ["<mark>"],
                        "post_tags" : ["</mark>"],
                        "fragment_size" : 300,
                        "number_of_fragments" : 3,
                        "order" : "score",
                        "boundary_scanner" : "sentence",
                        "boundary_scanner_locale" : "fr-FR",
                        "fields":{
                            "content":{}
                            }
                    }
                }


    if len(req.strip()) > 0:
        body["query"]['bool']['must'].append({"simple_query_string": {
                                    "fields" : ["content" , "title"],
                                    "query": req ,
                                    "analyze_wildcard": False
                                                }})

    for key in req_expression:
      body['query']['bool']["should"].append({"match":{
                                      'content' :{
                                          "query" : key,
                                          "boost" : 5
                                                }}})


    if from_date:
        body['query']['bool']["filter"].append({"range" :
                                {"date" : {"gte" : from_date}}
                                             })
    if  to_date:
        body['query']['bool']["filter"].append({"range" :
                                {"date" : {"lte" : to_date}}
                                            })

    if author:
      body['query']['bool']["filter"].append({"match" :
                        {"author" : {"query" : author}}})

    print(body)
    return body, length_of_request

def search(req, index_name,
            glossary_file=None, expression_file=None,
            from_date=None, to_date=None, author=None):

    """Fonction qui permet de faire la recherche Elastic dans notre index

    Args:
        index_name : Le nom de l'index où on effectue la recherche
        req : la requête entrèe par l'utilisateur
        expression_file : Le lien pour la liste des expressions clés analysée
        glossary_file : Fichier glossaire
    Output:
        Dictionnaire des résultats de la recherche
    """
    T = False
    Bande = False
    """ all keyword???
    Bande = False
    for keyword in Liste_acronyme:
        if keyword in analyzed:
            T = True
            break
    """
    if (req != '') or from_date or to_date or author:
        body, length_of_request = build_query(req,
                            index_name,
                            glossary_file,
                            expression_file,
                            from_date, to_date, author)

        D = es.search(index = index_name,
                      body = body,
                      size = 10)
    else:
        length_of_request = None
        D = es.search(index = index_name,
                      body = {
                            "query": {
                                "match_all": {}
                            }
                        },
                    size = int(10000)
                    )
    try: #This try is for the case where no match is found
        if not T and D['hits']['hits'][0]["_score"]/length_of_request < seuil: #The first filter then the second filter
          Bande = True
    except:
        pass

    return {'hits': D['hits']['hits'], 'length': length_of_request , 'band': Bande}

def corriger(req , INDEX_NAME):
  """
    Fonction qui permet de corriger la requête de l'utilisateur
    Arguments:
      INDEX_NAME : Le nom de l'index où on effectue la recherche des mots
      req : la requête entrèe par l'utilisateur
    Output:
      Liste des suggestions de correction
"""
  D = es.search(index = INDEX_NAME , body = {
  "suggest" : {
   "mytermsuggester" : {
      "text" : req,
      "phrase" : {
         "field" : "Réponse"
       }
    }
  }
  })
  L = []
  for i in range (len(list(D['suggest']['mytermsuggester'][0]['options']))):
    L.append(D['suggest']['mytermsuggester'][0]['options'][i]['text'])
  return L

def get_index_name(alias_name):
    try:
        res = es.indices.get_alias(name=alias_name)
        if len(res.keys()) == 1 and list(res.keys())[0] != "":
            index_name = list(res.keys())[0]
        else:
            raise Exception
    except elasticsearch.exceptions.NotFoundError:
        # create alias pointing to the blue index.
        index_name = alias_name + '_blue'
        es.indices.put_alias(index=alias_name, name=index_name)
    return index_name

def replace_blue_green(index_name, alias_name):
    if 'blue' in index_name:
        index_name = index_name.replace('blue', 'green')
    elif 'green' in index_name:
        index_name = index_name.replace('green', 'blue')
    else:
        raise Exception

    return index_name

def put_alias(index_name, alias_name):
    #es.indices.delete_alias(index=index_name, name=alias_name, ignore=[400, 404])
    es.indices.put_alias(index=index_name, name=alias_name)
    #es.indices.put_alias(index=index_name, name=alias_name)

def delete_alias(index_name, alias_name):
    es.indices.delete_alias(index=index_name, name=alias_name, ignore=[400, 404])

def get_alias(alias_name):
    return  es.indices.get_alias(name=alias_name)

def create_index(INDEX_NAME,
            user_data,
            es_data,
            mapping_file,
            glossary_file=None,
            expression_file=None):

    synonym_file = os.path.join(es_data, 'synonym.txt')
    print(os.path.join(user_data, mapping_file))
    with open(os.path.join(user_data, mapping_file) , 'r' , encoding = 'utf-8') as json_file:
        map = json.load(json_file)
    # Copy glossary and experssion file to elastic search mount volume
    print(map)

    with open(synonym_file, 'w') as outfile:
        if glossary_file:
            print('Use glossary file %s'%glossary_file)
            with open(os.path.join(user_data, glossary_file), 'r') as f1:
                outfile.write(f1.read())
        outfile.write('\n')
        if expression_file:
            print('Use expresion file %s'%expression_file)
            with open(os.path.join(user_data, expression_file), 'r') as f2:
                outfile.write(f2.read())

        else:
            outfile.write('')

    map['settings']["analysis"]["filter"]["synonym"].update(
            {"synonyms_path" : os.path.join(es_data, synonym_file)})

    print(map)
    with open(os.path.join(es_data, mapping_file), 'w') as outfile:
        json.dump(map, outfile)

    # Drop index
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    # create index
    es.indices.create(index=INDEX_NAME, body=map)


def inject_documents(INDEX_NAME, user_data, pdf_path, json_path,
            meta_path=None):

    no_match = 0

    (Path(user_data) / json_path).mkdir(parents=True, exist_ok=True)
    # empty it in case
    empty_tree(Path(user_data) / json_path)

    for path_document in (Path(user_data) / pdf_path).glob('**/*.pdf'):
        try:
            #path_document = pdf_path / filename
            print('Read %s'%str(path_document))

            index_file(path_document.name, INDEX_NAME, user_data, pdf_path, json_path,
                        meta_path)
            print('Document %s just uploaded'% path_document)

        except Exception as e:
            no_match += 1
            print(e)
            #break
            print(20*'*')
            print('Error, cannot upload %s'%path_document)
            print(20*'*')

    print("There is %s documents without metadata match"%no_match)

def index_file(filename, INDEX_NAME, user_data, pdf_path, json_path,
            meta_path):
    """
    Index json file to elastic with metadata
    Todo : substitue this function in inject_document
    """
    path_file = Path(user_data) / pdf_path / filename
    data = pdf2json(str(path_file))

    path_meta =  Path(user_data) / meta_path / filename
    path_json =  Path(user_data) / json_path / filename
    path_meta = path_meta.with_suffix('').with_suffix('.json') # replace extension
    path_json = path_json.with_suffix('').with_suffix('.json') # replace extension

    if path_meta.exists():
        with open(path_meta, 'r' , encoding = 'utf-8') as json_file:
            meta = json.load(json_file)
            data.update(meta)

    save_json(data, path_json)

    res = es.index(index = INDEX_NAME, body=data , id = filename)
    return res

def delete_file(filename, INDEX_NAME):
    try:
        res = es.delete(index = INDEX_NAME, id = filename)
        return 200, res
    except elasticsearch.exceptions.NotFoundError as e:
        return e.status_code, e.info
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == '__main__':

    INDEX_NAME = 'prod'
    USER_DATA = '/data/user'
    ES_DATA = '/usr/share/elasticsearch/data/extra'

    GLOSSARY_FILE = 'glossaire.txt'
    EXPRESSION_FILE = 'syn_expressions_metier.txt'
    MAPPING_FILE = 'map.json'
    METADATA_FILE = 'METADATA.xlsx'

    PDF_DIR = 'Data_Pdf'
    JSON_DIR = 'Data_Json'

    create_index(INDEX_NAME, USER_DATA, ES_DATA, MAPPING_FILE,
                GLOSSARY_FILE,
                EXPRESSION_FILE)

    inject_documents(INDEX_NAME, USER_DATA, PDF_DIR, JSON_DIR,
            metada_file = METADATA_FILE)
