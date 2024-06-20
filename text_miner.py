import re
from typing import List
import gensim
from gensim import corpora
import pandas as pd
from corpus_manager import CorpusManager
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

def preprocess(corpus: list[str]) -> list[str]:
    """
    Diese Funktion kombiniert einige Methoden für die Vorverarbeitung.

    Args:
        corpus: Ein Korpus als Liste
    Return:
        Das vorverarbeitete Korpus.
    """
    corpus = CorpusManager.clean_corpus(corpus)
    corpus = CorpusManager.lemmatize_corpus(corpus)
    corpus = CorpusManager.normalize_case(corpus)
    corpus = [re.sub("--", "", entry) for entry in corpus]
    return corpus

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

    corpus_cdu = CorpusManager("cdu")
    corpus_afd = CorpusManager("afd")
    corpus_linke = CorpusManager("linke")
    corpus_gruene = CorpusManager("gruene")
    corpus_fdp = CorpusManager("fdp")
    corpus_spd = CorpusManager("spd")

    corpus_cdu.processed = corpus_cdu.get_speaches_from_party("CDU")
    corpus_afd.processed = corpus_afd.get_speaches_from_party("AfD")
    corpus_linke.processed = corpus_linke.get_speaches_from_party("DIE LINKE")
    corpus_gruene.processed = corpus_gruene.get_speaches_from_party("BÜNDNIS 90/DIE GRÜNEN")
    corpus_fdp.processed = corpus_fdp.get_speaches_from_party("Freie Demokraten")
    corpus_spd.processed = corpus_spd.get_speaches_from_party("SPD")

    corpus_cdu.processed = preprocess(corpus_cdu.processed)
    corpus_afd.processed = preprocess(corpus_afd.processed)
    corpus_linke.processed = preprocess(corpus_linke.processed)
    corpus_gruene.processed = preprocess(corpus_gruene.processed)
    corpus_fdp.processed = preprocess(corpus_fdp.processed)
    corpus_spd.processed = preprocess(corpus_spd.processed)


    documents = [corpus_cdu.processed, corpus_afd.processed, corpus_linke.processed, corpus_gruene.processed, corpus_fdp.processed, corpus_spd.processed]

    calculate_mean_tf_idf(documents)

    '''
    
    # Generation eines Wörterbuchs
    dictionary = corpora.Dictionary(documents)

    # Generation eines Bag-of-Words-Korpus
    corpus = [dictionary.doc2bow(document) for document in documents]

    lda_model = gensim.models.LdaModel(corpus,
     num_topics=20,
      id2word=dictionary,
       passes=15)

    # Themen drucken
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)

    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis_data, 'lda_visualization.html')
    '''

    """
    tokens = [entry for entry in tokens if len(entry) > 2]
    
    bi_grams = list(bigrams(tokens))

    bigram_counts = Counter(bi_grams)

    
    for bigram, count in bigram_counts.items():
        if count > 25:
            print(f"{bigram}: {count}")

    '''
    CDU:
    ('ländlich', 'raum'): 230
    ('schülerin', 'schüler'): 253
    ('landesamt', 'verfassungsschutz'): 26
    ('erneuerbar', 'energie'): 36
    ('hessisch', 'polizei'): 80
    ('unser', 'polizei'): 28
    ('europäisch', 'union'): 79
    ('europäisch', 'ebene'): 27
    
    AFD:
    ('ländlich', 'raum'): 108
    ('schülerin', 'schüler'): 40
    ('hass', 'hetze'): 26
    ('cancel', 'culture'): 31
    ('innerer', 'sicherheit'): 51
    ('seit', '2015'): 30
    ('sogenannter', 'klimaschutz'): 39
    ('europäisch', 'union'): 80
    
    '''"""