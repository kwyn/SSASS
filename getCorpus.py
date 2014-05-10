import wikipedia
import logging
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def get_corpus():
  queries = ['meditation', 'big sur', 'vipassana', 'osho', 'krishna', 'compilers', 'mpfc', 'triune brain', 'javascript', 'http', 'burning man']
  titles = [wikipedia.search(q) for q in queries]
  pages = []
  print len(titles)
  for title in titles:
    try:
      pages.append(wikipedia.WikipediaPage(title).content)
    except wikipedia.exceptions.DisambiguationError:
      print 'Skipping ambiguous page title: %s' % title
  print len(pages)

  return pages

corpus = open('data.pkl', 'wb')

pages = get_corpus()
pickle.dump(pages, corpus)

print pages
corpus.close()