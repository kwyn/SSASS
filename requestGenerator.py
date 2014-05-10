import wikipedia
import requests
import logging
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus = open('data.pkl', 'rb')
pages = pickle.load(corpus)
corpus.close()

def make_requests(pages):
  results = list()
  print len(pages)
  for page in pages:
    parameters = { 'document_body':  page }
    r = requests.post('http://172.12.8.150/corpus', params=parameters)
    results.append((r.text))
    # print r.text
  parameters = { 'document_body':  "Meditation is fucking awesome. Vapassana for the win." }
  r = requests.post('http://172.12.8.150/corpus', params=parameters)
  print r.text
  result = r.json()
  parameters = { 'document_id': result['doc_id'] }
  r = requests.get('http://172.12.8.150/search', params=parameters)
  print r.text
  parameters = { 'document_id': 'doc_1' }
  r = requests.get('http://172.12.8.150/search', params=parameters)
  print r.text
  results.append((r.text, parameters))
  return results

make_requests(pages)
# parameters = { 'document_id': 'doc_1' }
# r = requests.get('http://172.12.8.150/documents', params=parameters)
# print r.url, r.text