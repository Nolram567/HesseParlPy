import json
from nltk import bigrams, Counter
import pandas as pd
from corpus_manager import CorpusManager


def calculate_cooccurrence(documents: list[str]) -> None:
    """
    Mit dieser Methode lassen sich bedeutsame mehrteilige Ausdrücke in ihrer lemmatisierten Form ausfindig machen.
    Dafür werden für eine Liste aus Dokumenten kookkurrierende Terme (2-Gramme) berechnet und ihre Frequenz bestimmt.
    Alle Bigramme und ihre Frequenz werden als CSV-Datei serialisiert.

    Args:
        documents: Die List aus Strings.
    """
    # Bereinigung und Lemmatisierung der Dokumente.
    documents = CorpusManager.clean_corpus(documents)
    lemmatised_docs = CorpusManager.lemmatize_corpus(documents)
    tokens = [item for sublist in lemmatised_docs for item in sublist]
    temp = [token.strip() for token in tokens if token.isalnum()]
    temp = CorpusManager.normalize_case(temp)
    temp = CorpusManager.clean_with_custom_stopwords("data_outputs/stopwords.txt", temp)

    # Erzeugen der Bigramme
    bi_grams = list(bigrams(temp))

    # Zählen der Bigramme
    bigram_counts = Counter(bi_grams)

    # Wir schreiben die Bigramme in einen Dataframe ein.
    cooccurrence = pd.DataFrame(columns=["Bigramm", "Count"])
    rows = []
    for bigram, count in bigram_counts.items():
        rows.append({"Bigramm": bigram, "Count": count})

    cooccurrence = pd.concat([cooccurrence, pd.DataFrame(rows)], ignore_index=True)

    # Wir speichern die Kookkurrenzen in einer CSV-Datei für die qualitative Begutachtung ab.
    cooccurrence.to_csv("data_outputs/cooccurrence.csv", index=False)

if __name__ == "__main__":

    #Wir laden das Korpus und berechnen die Kookkurrenzen.
    corpus = CorpusManager("All_Speaches")

    corpus.processed = corpus.get_all_speaches()

    calculate_cooccurrence(corpus.processed)

    '''
    Relevante, mehrteilige Ausdrücke und namend entities (Auszug):
        Begriff                                     Lemmatisiertes N-Gramm
        Rechte Szene                                ('rechter', 'szene')
        Rechte Gewalt                               ('recht', 'gewalt'), ('rechter', 'gewalt')
        Rechter Terror                              ('rechter', 'terror')
        Turgut Yüksel                               ('turgut', 'yüksel')
        Christian Lindner                           ('christian', 'lindner')
        Kassenärtzliche Vereinigung                 ('kassenärztliche', 'vereinigung')
        Dannenröder Forst                           ('dannenröder', 'forst'), ('dannenröd', 'forst')
        Open Data                                   ('ope', 'data'), ('open', 'data')
        Cancel culture                              ('cancel', 'culture')
        Fake News                                   ('fake', 'news')
        Fridays for Future                          ('fridays', 'for'), ('for', 'future')
        Anschlag in Hanau                           ('anschlag', 'hanau')
        Soziale Netzwerke                           ('sozial', 'netzwerke')
        Mündliche Anhörung                          ('mündlich', 'anhörung')
        Landesamt für Gesundheit                    ('landesamt', 'gesundheit')
        Landesamt für Verfassungsschutz             ('landesamt', 'verfassungsschutz')
        Freiheitlich demokratische Grundordnung     ('freiheitlichdemokratisch', 'grundordnung')
        Rhönklinikum AG                             ('rhönklinikum', 'ag'), ('rhön', 'ag')
        Robert-Koch Institut                        ('robert', 'kochinstitut')
        Frankfurter Rundschau                       ('frankfurter', 'rundschau')
        Vulnerable Gruppe                           ('vulnerabl', 'gruppe')
        Stephan Ernst                               ('stephan', 'e'), ('stephan', 'ernst')
        Gesetzliche Krankenkasse                    ('gesetzlich', 'krankenkasse')
        Gesetzlicher Mindestlohn                    ('gesetzlich', 'mindestlohn')
        Sozialer Zusammenhalt                       ('sozial', 'zusammenhalt')
        Sozialer Wohnungsbau                        ('sozial', 'wohnungsbau')
        Soziale Marktwirtschaft                     ('sozial', 'marktwirtschaft')
        Soziale Integration                         ('soziale', 'integration')
        Soziale Sicherheit                          ('sozial', 'sicherheit')
        Soziale Ungleichheit                        ('sozial', 'ungleichheit')
        Soziale Spaltung                            ('sozial', 'spaltung')
        Volker Bouffier                             ('volker', 'bouffier')
        Olaf Scholz                                 ('olaf', 'scholz')
        Angela Dorn                                 ('angela', 'dorn')
        Mathias Wagner                              ('mathias', 'wagner')
        Roland Koch                                 ('roland', 'koch')
        Janine Wissler                              ('janine', 'wissler')
        Robert Lambrou                              ('robert', 'lambrou')
        Elisabeth Kula                              ('elisabeth', 'kula')
        Volker Richter                              ('volker', 'richter')
        Tarek Al-Wazir                              ('tarek', 'alwazir')
        Heike Hoffmann                              ('heike', 'hofmann')
        Priska Hinz                                 ('priska', 'hinz')
        Halit Yozgat                                ('halit', 'yozgat')
        Viorel Păun                                 ('viorel', 'păun')
        Michael Reul                                ('michael', 'reul')
        Lisa Gnadl                                  ('lisa', 'gnadl')
        Thorsten Schäfergümbel                      ('thorsten', 'schäfergümbel')
        Willy Brandt                                ('willy', 'brandt')
        Knut John                                   ('knut', 'john')
        Jörg-Uwe Hahn                               ('jörguwe', 'hahn')
        Walter Lübcke                               ('walter', 'lübcke')
        Verkaufsoffene Sonntage                     ('verkaufsoffen', 'sonntage')
        Kassenärtzliche Vereinigung                 ('kassenärztlich', 'vereinigung')
        Polizeiliche Kriminalstatistik              ('polizeiliche', 'kriminalstatistik')
        Freiheit der Wissenschaft                   ('freiheit', 'wissenschaft'), ('freiheit', 'forschung')
        Psychatrische Versorgung                    ('psychiatrisch', 'versorgung')
        Namentliche Abstimmung                      ('namentlich', 'abstimmung')
        Fort - und Weiterbildung                    ('fort', 'weiterbildung')
        Russischer Angriffskrieg gegen die Ukraine  ('russisch', 'angriffskrieg'), ('angriffskrieg', 'russlands'), ('ukraine', 'krieg'), ('krieg', 'ukraine')
        Kommunaler Finanzausgleich                  ('kommunal', 'finanzausgleich'), ('kommunalen', 'finanzausgleich')
        Sexuelle Gewalt                             ('sexuell', 'gewalt'), ('sexualisiert', 'gewalt')
        Häusliche Gewalt                            ('häuslich', 'gewalt'), ('gewalt', 'häuslich')
        Vereinigtes Königreich                      ('vereinigt', 'königreich')
        Frankfurt am Main                           ('frankfurt', 'main')
        Bad Homburg                                 ('bad', 'homburg')
        Bad Hersfeld                                ('bad', 'hersfeld')
        Ehrenamtliches Engagement                   ('ehrenamtlich', 'engagement')
        Digitale Infrastruktur                      ('digital', 'infrastruktur')
        Künstlicher Intelligenz                     ('künstlich', 'intelligenz')
        Landwirtschaftlicher Betrieb                ('landwirtschaftlich', 'betrieb')
        Biologische Vielfalt                        ('biologisch', 'vielfalt')
        Digitales Endgerät                          ('digital', 'endgerät')
        Digitale Transformation                     ('digital', 'transformation'), ('digital', 'wandel')
        Digitale Lehre                              ('digital', 'lehre'), ('digital', 'lehr')
        Digitalstrategie                            ('digital', 'strategie')
        Jüdische Gemeinde                           ('jüdisch', 'gemeinde')
        Psychische Erkrankung                       ('psychisch', 'erkrankung')
        Masterplan Kultur                           ('masterplan', 'kultur')
        Öffentliches Eigentum                       ('öffentlich', 'eigentum')
        Öffentlicher Dienst                         ('öffentlich', 'dienst')
        Öffentlicher Personennahverkehr             ('öffentlich', 'personennahverkehr'), ('öffentlich', 'nahverkehr')
        Öffentliche Verwaltung                      ('öffentlich', 'verwaltung')
        Öffentliche Mittel                          ('öffentlich', 'mittel'), ('öffentlich', 'geld')
        Öffentliche Infrastruktur                   ('öffentlich', 'infrastruktur')
        Europäischer Gerichtshof                    ('europäisch', 'gerichtshof')
        Innere Sicherheit                           ('innerer', 'sicherheit'), ('öffentlich', 'sicherheit')
        Gesellschaftliche Teilhabe                  ('gesellschaftlich', 'teilhabe')
        Rechtliche Rahmenbedinungen                 ('rechtlich', 'rahmenbedingung')
        Mobile Arbeit                               ('mobil', 'arbeit')
        Vereinte Nationen                           ('vereint', 'nation')
        Bündnis 90, die Grünen                      ('90die', 'grünen')
        Alternative für Deutschland                 ('alternative', 'deutschland')
        Deutsche Sprache                            ('deutsch', 'sprache')
        Demografischer Wandel                       ('demografisch', 'wandel'), ('demografisch', 'entwicklung')
        Ländliche Region                            ('ländlich', 'region')
        Energetische Sanierung                      ('energetisch', 'sanierung')
        Dritte Welle                                ('dritter', 'welle')
    '''

    MWE = {
            "Rechte Szene": [('rechter', 'szene')]
    }
    
    with open("data_outputs/MWE.json", "w", encoding="utf-8") as f:
        json.dump(MWE, f, ensure_ascii=False, indent=6)

    '''
    Nachdem die Werte in die JSON-Struktur überführt wurden, werden sie erneut geladen.
    Schlüssel und Werte werden invertiert, damit im Rahmen der LDA-Vorverarbeitung die 2-Gramme auf die entsprechende MWE als 1-Gramm abgebildet
    werden können.
    '''

    with open('data_outputs/MWE.json', 'r', encoding="utf-8") as json_file:
        MWE = json.load(json_file)

    mutliword_expressions = []
    for entry in MWE.values():
        for tuples in entry:
            mutliword_expressions.append(tuples)

    new_dict = {}

    for item in MWE.items():
        for bigram in item[1]:
            new_dict[str(bigram)] = item[0]

    # Der invertierte JSON-Container wird abgespeichert.
    with open('data_outputs/MWE_reversed.json', 'w', encoding="utf-8") as json_file:
        json.dump(new_dict, json_file, ensure_ascii=False, indent=6)
