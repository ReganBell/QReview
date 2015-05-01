import nltk
from collections import Counter

class TFIDFCalculator:

    def __init__(self, documents):
        documents_dict = {}
        for document in documents:
            title = document[0]
            comments = document[1]
            doc_counter = Counter()
            for comment in comments:
                for word in nltk.word_tokenize(comment):
                    doc_counter[word] += 1
            documents_dict[title] = doc_counter
        self.documents = documents_dict

    def word_tf_idf_in_doc(self, word, document):
        doc_counter = self.documents[document[0]]
        tf = doc_counter[word]
        df = 0
        for doc in self.documents:
            df += 1 if word in self.documents[doc] else 0
        return tf / float(df)

doc = ["Hello", ["This is a q comment about CS50. This is another", "This is a second comment."]]
calc = TFIDFCalculator([doc])
tf_idf = calc.word_tf_idf_in_doc("This", doc)
