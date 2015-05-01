import nltk
from math import log
from collections import Counter

class TFIDFCalculator:

    def __init__(self, documents):
        documents_dict = {}
        for document in documents:
            title = document[0]
            comments = document[1]
            doc_counter = Counter()
            total = 0
            for comment in comments:
                for word in nltk.word_tokenize(comment):
                    doc_counter[word.lower()] += 1
                    total += 1
            documents_dict[title] = {"counter": doc_counter,"total": total}
        self.documents = documents_dict

    def word_tf_idf_in_doc(self, word, document):

        doc_counter = self.documents[document[0]]["counter"]
        count = doc_counter[word.lower()]
        total = self.documents[document[0]]["total"]
        tf = count / float(total)

        total_docs = len(self.documents)
        all_docs_occurrences = 0
        for doc in self.documents:
            all_docs_occurrences += 1 if word.lower() in self.documents[doc] else 0
        all_docs_occurrences = 1 if all_docs_occurrences == 0 else all_docs_occurrences
        idf = log(total_docs / float(all_docs_occurrences))

        return tf / idf