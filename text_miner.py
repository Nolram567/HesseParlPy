import re
from typing import List
import gensim
from gensim import corpora
import pandas as pd
from corpus_manager import CorpusManager
from nltk import word_tokenize, bigrams, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

def preprocess_LDA(corpus: list[str]) -> list[list[str]]:
    """
    Diese Funktion kombiniert einige Methoden für die Vorverarbeitung.

    Args:
        corpus: Ein Korpus als Liste
    Return:
        Das vorverarbeitete Korpus.
    """
    corpus = CorpusManager.clean_corpus(corpus)
    corpus = CorpusManager.lemmatize_corpus(corpus)
    polished_corpus = []
    for doc in corpus:

        # Wir entfernen aller 'stumps', das sind Reden mit weniger als 100 Termen.
        if len(doc) < 100:
            print(doc)
            continue

        # Alle fehlerhaften Token sowie Token, die weniger als 4 Zeichen haben, werden entfernt.
        temp = [token for token in doc if token not in ["--", " "] and len(token) > 3]

        temp = CorpusManager.normalize_case(doc)
        temp = CorpusManager.clean_with_custom_stopwords("data_outputs/stopwords.txt", temp)
        polished_corpus.append(temp)
    polished_corpus = CorpusManager.union_multiword_expression(polished_corpus, ['öffentlich dienst', 'hass hetze'])
    return polished_corpus

def serialize_corpus(corpus: CorpusManager) -> None:
    """
    Diese Funktion serialisiert ein verarbeitetes Korpus.

    Args:
        Das Korpus
    """

    with open(f"data/processed_corpus/corpus_{corpus.name}", "w", encoding="utf-8") as f:
        f.write(corpus.processed)

def calculate_mean_tf_idf(documents: list[list[str]], path: str = "") -> None:
    """
    Diese Funktion berechnet für eine Liste aus tokenisierten Dokumenten die TF-IDF und bestimmt das arithmetische Mittel.
    Die Ergebnisse werden in einer CSV-Datei serialisiert.

    Args:
        documents: Die Liste mit Listen von Token.
        path: Der Dateipfad unter dem die Ergebnisse serialisiert werden sollen.
    """

    # Konkatenieren der tokenisierten Dokumente
    documents = [' '.join(doc) for doc in documents]

    # Instanziiere den TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Berechne der TF-IDF
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Extrahiere Terme
    feature_names = vectorizer.get_feature_names_out()

    # Instanziierung einen DataFrame mit den TF-IDF-Werten
    df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    with open(f'{path}tfidf_results.csv', 'w', encoding='utf-8') as f:
        for term in feature_names:
            # Berechnung den mittleren TF-IDF-Wert für den Term über alle Dokumente
            mean_tfidf = df_tfidf[term].mean()
            f.write(f'{term},{mean_tfidf}\n')

    print(f'Die TF-IDF-Werte wurden serialisiert.')

if __name__ == "__main__":

    '''test = ["Ich sollte anständige Tests schreiben das ist ein test öffentlicher dienst test",
                "das ist ein test öffentlicher dienst",
                "das hass hetze ist ein Bedrohung test öffentlicher dienst test"
                 "das hass unmöglich Problem Klima öffentlicher dienst test"]'''

    #print(preprocess_LDA(test))
    '''documents = preprocess_LDA(corpus.processed)

    # Generation eines Wörterbuchs
    dictionary = corpora.Dictionary(documents)

    # Generation eines Bag-of-Words-Korpus
    corpus = [dictionary.doc2bow(document) for document in documents]

    lda_model = gensim.models.LdaModel(corpus,
     num_topics=50,
      id2word=dictionary,
       passes=15)

    # Themen drucken
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)

    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis_data, 'lda_visualization.html')
'''