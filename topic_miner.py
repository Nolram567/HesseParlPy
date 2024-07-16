import numpy as np
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.corpora import MmCorpus
import plotly.graph_objects as go


if __name__ == "__main__":

    # Modelle und Daten laden
    model = LdaModel.load('data_outputs/topic_models/topic_model_t29.lda')
    dictionary = Dictionary.load('data_outputs/topic_models/dictionary.dict')
    loaded_corpus = MmCorpus('data_outputs/topic_models/bow_corpus.mm')

    # Themen und ihre Top-Wörter ausgeben
    for topic_id in range(model.num_topics):
        words = model.show_topic(topic_id, topn=10)
        topic_words = ', '.join([word for word, prob in words])
        print(f"Thema {topic_id + 1}: {topic_words}")

    # Themenverteilungen extrahieren
    topic_distributions = [model.get_document_topics(bow, minimum_probability=0) for bow in loaded_corpus]

    # Datenmatrix erstellen
    data_matrix = np.zeros((len(loaded_corpus), model.num_topics))

    for doc_id, dist in enumerate(topic_distributions):
        for topic_id, prob in dist:
            data_matrix[doc_id, topic_id] = prob

    # Pearson-Korrelationen berechnen
    correlation_matrix = np.corrcoef(data_matrix, rowvar=False)
    topic_correlations = {}

    for i in range(model.num_topics):
        for j in range(i + 1, model.num_topics):
            key = f"Thema{i + 1}, Thema{j + 1}"
            topic_correlations[key] = correlation_matrix[i, j]

    # Ausgabe der Korrelationen
    print(topic_correlations)
    labels, values = zip(*topic_correlations.items())

    # Boxplot erstellen
    fig = go.Figure()

    fig.add_trace(go.Box(y=values,
                         boxpoints='all',  # Alle Punkte anzeigen
                         jitter=0.5,  # Punkte horizontal streuen
                         pointpos=-1.8,  # Position der Punkte relativ zum Boxplot
                         hovertext= [f'{label}: {value}' for label, value in zip(labels, values)],  # Tooltips mit den Themenlabels
                         marker_color='blue',
                         name=""))

    # Layout-Anpassungen
    fig.update_layout(title='Korrelationen zwischen Themen',
                      yaxis_title='Pearson-Korrelationskoeffizient',
                      xaxis_title='Themenpaare',
                      showlegend=False)

    # Diagramm anzeigen
    fig.show()