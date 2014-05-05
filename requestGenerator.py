import wikipedia
import requests
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def get_corpus():
  queries = ['meditation', 'big sur', 'vipassana', 'osho', 'krishna', 'compilers', 'mpfc', 'triune brain', 'javascript', 'http', 'burning man']
  titles = [wikipedia.search(q) for q in queries]
  pages = []
  print len(titles)
  for title in titles:
    try:
      pages.append(wikipedia.summary(title))
    except wikipedia.exceptions.DisambiguationError:
      print 'Skipping ambiguous page title: %s' % title
  print len(pages)
  return pages

def make_requests(pages):
 	results = list()
 	for page in pages:
		parameters = { 'document_body':  page }
 		r = requests.post('http://172.12.8.150/corpus', params=parameters)
 		results.append((r.text))
 		print r.text
 	parameters = { 'document_id': 'doc_1' }
 	r = requests.get('http://172.12.8.150/search', params=parameters)
 	results.append((r.text, parameters))
 	return results

corpus = get_corpus()
print make_requests(corpus)
