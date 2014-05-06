#! /usr/local/bin/python

from flask import Flask, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from gensim import utils
from simserver import SessionServer
import os, shutil
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)


########################################################################  
#Define Local Variables
########################################################################  

corpus = list()
documents = dict()

########################################################################  
#Define Helper functions
########################################################################

parser = reqparse.RequestParser()
parser.add_argument('corpus_name', type=str, help='name of target corpus')
parser.add_argument('document_body', type=str, help='body of document to be parsed')
parser.add_argument('document_id', type=str, help="the document's id :P")

def abort_if_document_doesnt_exist(document_id):
  if document_id not in documents:
    abort(404, message="Document {} doesn't exit".format(document_id))

def get_service():
  SERVER_DIR = '/tmp/simserver/'
  try:
    os.mkdir(SERVER_DIR)
  except:
    pass
  service = SessionServer(SERVER_DIR)
  service.set_autosession()
  return service

def add_document(document):
  service = get_service()
  doc_id = 'doc_%s' % len(corpus)
  doc = dict()
  tokens = utils.simple_preprocess(document)
  doc = {'id': doc_id, 'tokens': tokens , 'body':document}
  documents[doc_id] = doc
  corpus.append(doc)
  return doc_id

def find_similar(doc_id):
  service = get_service()
  service.train(corpus)
  service.index(corpus)
  return service.find_similar(doc_id)

########################################################################  
#Define Handlers
########################################################################  

class Corpus(Resource):
  def get(self):
    abort_if_corpus_doesnt_exist(corpus_name)
    return corpuses[corpus_name]
  def post(self):
    args = parser.parse_args()
    document_id = add_document(args['document_body'])
    return jsonify({ 'doc_id' : document_id, 'body': args['document_body'] })

class Documents(Resource):
  def get(self, document_id):
    abort_if_document_doesnt_exist(document_id)
    return jsonify({'results' : documents[document_id]})

class Search(Resource):
  def get(self):
    args = parser.parse_args()
    service = get_service()
    print args.keys()
    doc_id = args['document_id']
    return jsonify({'result': find_similar(doc_id)})

########################################################################  
#Define endpoints
########################################################################  

api.add_resource(Corpus, '/corpus')
api.add_resource(Documents, '/documents')
api.add_resource(Search, '/search')

if __name__ == "__main__":
  app.run(host="0.0.0.0")

