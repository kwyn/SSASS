#! /usr/local/bin/python

import wikipedia
from gensim import utils
from simserver import SessionServer
import os
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
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

def get_service():
  SERVER_DIR = '/tmp/simserver/'
  try:
    os.mkdir(SERVER_DIR)
  except:
    pass

  return SessionServer(SERVER_DIR)


corpus = get_corpus()
service = get_service()
service.train(corpus, method='lsi')
service.index(corpus)

import pdb; pdb.set_trace()

