#! /usr/local/bin/python

import wikipedia
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from gensim import utils
from simserver import SessionServer
import os
import logging

app = Flask(__name__)
api = Api(app)


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

########################################################################  
#Define Local Variables
########################################################################  

corpuses = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}
documents = dict()

########################################################################  
#Define Helper functions
########################################################################  

def abort_if_corpus_doesnt_exist(corpus_name):
  if corpus_name not in corpuses:
    abort(404, message="Corpus {} doesn't exist".format(corpus_name))

def abort_if_document_doesnt_exist(document_id):
  if document_id not in documets:
    abort(404, message="Document {} doesn't exit".format(document_id))

def get_service():
  SERVER_DIR = '/tmp/simserver/'
  try:
    os.mkdir(SERVER_DIR)
  except:
    pass

  return SessionServer(SERVER_DIR)

########################################################################  
#Define Handlers
########################################################################  

class Corpus(Resource):
  def get(self, corpus_name):
    # abort_if_corpus_doesnt_exist(corpus_name)
    return corpuses

class Documents(Resource):
  def get(self, document_id):
    abort_if_document_doesnt_exist(document_id)
    return documents


########################################################################  
#Define endpoints
########################################################################  

api.add_resource(Corpus, '/corpus')
api.add_resource(Documents, '/documents')
# api.add_recource(Search)

def get_corpus():
  queries = ['meditation', 'big sur', 'vipassana', 'osho', 'krishna', 'compilers', 'mpfc', 'triune brain', 'javascript', 'http', 'burning man']
  titles = [wikipedia.search(q) for q in queries]
  pages = []
  for title in titles:
    try:
      pages.append(wikipedia.summary(title))
    except wikipedia.exceptions.DisambiguationError:
      print 'Skipping ambiguous page title: %s' % title

  return [{'id': 'doc_%s' % num, 'tokens': utils.simple_preprocess(text)} for num, text in enumerate(pages)]




# @app.route('/')
# def setup():
#   corpus = get_corpus()
#   service = get_service()
#   service.train(corpus, method='lsi')
#   service.index(corpus)
#   return "setup complete"

# @app.route('getsim/<documentID>')
# def get_sim(documentID):
#   find_similar(documentID)


# @app.route('/reindex')
# def reindex():
#   try:
#     corpus
#   except:
#     return "no corpus defined yet"
#   else:
#     service.index(corpus)
#     return "Reindexed!"

if __name__ == "__main__":
  app.run(host="0.0.0.0")

