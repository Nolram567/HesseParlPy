import gensim
from gensim import corpora
from gensim.corpora import MmCorpus
from gensim.models import CoherenceModel
import pandas as pd
import json
import os
from corpus_manager import CorpusManager
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
    print(sum(len(s) for s in corpus))
    corpus = CorpusManager.clean_corpus(corpus)
    corpus = CorpusManager.lemmatize_corpus(corpus)
    print(sum(len(s) for sublist in corpus for s in sublist))
    polished_corpus = []

    for doc in corpus:

        # Wir entfernen alle 'stumps', das sind Reden mit weniger als 100 Termen.
        if len(doc) < 100:
            #print(doc)
            continue

        # Alle fehlerhaften Token sowie Token, die weniger als 4 Zeichen haben, werden entfernt.
        temp = [token for token in doc if token not in ["--", " "] and len(token) > 2]

        temp = CorpusManager.normalize_case(temp)
        temp = CorpusManager.clean_with_custom_stopwords("data_outputs/stopwords.txt", temp)
        polished_corpus.append(temp)
    print(sum(len(s) for sublist in polished_corpus for s in sublist))
    polished_corpus = CorpusManager.union_multiword_expression(polished_corpus)
    print(sum(len(s) for sublist in polished_corpus for s in sublist))
    return polished_corpus


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

    '''
    Wir instanziieren ein CorpusManager-Objekt, laden alle Reden, vorverarbeiten das Korpus und speichern das Produkt.
    
    corpus = CorpusManager("All_Speaches_LDA_preprocessed")

    corpus.processed = corpus.get_all_speaches()

    corpus.processed = preprocess_LDA(corpus.processed)

    corpus.serialize_corpus()
    '''

    #Das vorverarbeitete Korpus wird geladen.
    corpus = CorpusManager(name="All_Speaches_LDA_preprocessed", load_processed=True)

    print(f"Es gibt {len(corpus.processed)} verarbeitete Dokumente im Korpus.")
    print(f"Ein Dokument hat durchschnittlich {sum(len(doc) for doc in corpus.processed)/len(corpus.processed)} Zeichen.")


    # Generation des Wörterbuchs
    dictionary = corpora.Dictionary(corpus.processed)

    # Berechnung des Bag-of-Words-Korpus
    bag_of_words_model = [dictionary.doc2bow(document) for document in corpus.processed]

    coherence_map = {}

    '''
    Wir generieren zunächst eine Population aus 10 Modellen mit t aus dem Intervall [30, 100] mit 10er Schritten.
    Im Anschluss können wir das Intervall reduzieren und in 1er Schritten nach der optimalen Themenzahl hinsichtlich der
    Kohärenzmetrik C_v suchen.
    '''

    #for t in range(30, 101, 10):
    #for t in range(20, 31):
    for t in range(29, 30):

        # Wir berechnen das Model uns lassen die Hyperparameter alpha und eta vom Algorithmus optimieren.
        lda_model = gensim.models.LdaModel(bag_of_words_model,
                                           num_topics=t,
                                           id2word=dictionary,
                                           passes=30,
                                           iterations=100,
                                           alpha='auto',
                                           eta='auto')

        # Wir berechnen die Kohärenz des Themenmodells mit t Themen nach der Kohärenzmetrik C_v nach Röder et al. (2015)
        coherence_model = CoherenceModel(model=lda_model, texts=corpus.processed, dictionary=dictionary,
                                         coherence='c_v')

        coherence = coherence_model.get_coherence()
        coherence_map[t] = coherence
        print(f'Kohärenzscore C_v mit {t} Themen: {coherence}')

    #Wir speichern die Themenzahl t mit den korrespondierenden Kohärenzwerten ab.
    with open("data_outputs/coherence_map_2", "w", encoding="utf-8") as f:
        json.dump(coherence_map, f, indent=2, ensure_ascii=False)

    # Wir visualisieren das Themenmodell und speichern die dynamische Grafik ab.
    vis_data = gensimvis.prepare(lda_model, bag_of_words_model, dictionary)
    pyLDAvis.save_html(vis_data, 'lda_visualisation/lda_visualization_t29_4.html')

    #Wir serialisieren das LDA-Model, das BoW-Korpus und das Dictionary, um das Model vollständig wiederherstellen zu können.
    dictionary.save(os.path.join('data_outputs/topic_models', 'dictionary_4.dict'))
    lda_model.save(os.path.join('data_outputs/topic_models', 'topic_model_t29_4.lda'))
    MmCorpus.serialize('data_outputs/topic_models/bow_corpus.mm', bag_of_words_model)
