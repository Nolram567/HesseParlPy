import numpy as np
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.corpora import MmCorpus
import plotly.graph_objects as go
import plotly.io as pio
import networkx as nx
import matplotlib.pyplot as plt

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

    label_id_map = {
        1: "Gesetzgebung",
        2: "Covid-19-Pandemie_I",
        3: "Medizinische Versorgung",
        4: "Covid-19-Pandemie_II",
        5: "Kultur",
        6: "Justizwesen",
        7: "Hochschulwesen",
        8: "Landesfinanzen_I",
        9: "(Erneuerbare) Energie",
        10: "Covid-19-Pandemie_III",
        11: "Barrierefreiheit",
        12: "ÖRR",
        13: "Europäische Union",
        14: "Verwaltung im Landtag_I",
        15: "Gewalt/Polizei*",
        16: "Familie",
        17: "Wirtschaft",
        18: "Russisch-ukrainischer Krieg",
        19: "Landesfinanzen_II",
        20: "Kommunalwesen",
        21: "Verwaltung im Landtag_II",
        22: "**_I",
        23: "Wohnraum",
        24: "Terrorismus",
        25: "Migration und Asyl",
        26: "Demokratie",
        27: "Schulwesen",
        28: "**_II",
        29: "Vereinswesen"
    }

    for i in range(model.num_topics):
        for j in range(i + 1, model.num_topics):
            key = f"{label_id_map[i + 1]}, {label_id_map[j + 1]}"
            topic_correlations[key] = correlation_matrix[i, j]

    # Ausgabe der Korrelationen
    #print(topic_correlations)
    labels, values = zip(*topic_correlations.items())

    # Boxplot erstellen
    fig = go.Figure()

    # Berechnung der Perzentile
    lower_whisker = np.percentile(values, 2.5)
    upper_whisker = np.percentile(values, 97.5)

    print(upper_whisker, lower_whisker)

    fig.add_trace(go.Box(y=values,
                         boxpoints='all',  # Alle Punkte anzeigen
                         jitter=0.5,  # Punkte horizontal streuen
                         pointpos=-1.8,  # Position der Punkte relativ zum Boxplot
                         # hovertemplate= f"{label, value for label, value in zip(labels, values)}",
                         hovertext=[f'{label}: {value}' for label, value in zip(labels, values)],
                         marker_color='blue',
                         name="Pearson-Korrelation"))

    # Layout-Anpassungen
    fig.update_layout(
        title='Korrelationen zwischen Themen',
        yaxis_title='Pearson-Korrelationskoeffizient',
        showlegend=False
    )

    # Diagramm anzeigen und serialisieren
    pio.write_html(fig, file='docs/correlation_boxplot.html')

    # Wir durchsuchen das Dictionary nach allen Korrelationen, die größer als das .975-Perzentil sind.
    extreme_correlations = {key: value for key, value in topic_correlations.items() if value >= upper_whisker}

    # Wir instanziieren das Netzwerk und fügen die Kanten hinzu
    G = nx.Graph()
    for (topic_pair, correlation) in extreme_correlations.items():
        topic1, topic2 = topic_pair.split(", ")
        G.add_edge(topic1, topic2, weight=correlation)

    # Wir berechnen das Layout und definieren die optischen Eigenschaften.
    pos = nx.spring_layout(G, seed=450, k=0.3)  # Diese Parametrisierung ergab die beste "Lesbarkeit" des Netzwerks.
    plt.figure(figsize=(12, 10))
    edges = nx.draw_networkx_edges(G, pos, edge_color='lightblue', width=2)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=700, node_color='orange', edgecolors='none', linewidths=0)
    labels = nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    # Wir fügen die Kantengewichte hinzu und runden sie bis auf die zweite Nachkommastelle.
    edge_labels = nx.get_edge_attributes(G, 'weight')
    formatted_edge_labels = {(n1, n2): f'{weight:.2f}' for (n1, n2), weight in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, font_color='black')

    plt.show()