import json
import os
import xml.etree.ElementTree as ET
import string
import spacy
from nltk.corpus import stopwords
import nltk


class CorpusManager:
    """
    Objekte dieser Klasse initialisieren und verwalten ein Korpus.

    Attributes:
        corpus (dict): Dieses Dictionary enthält alle Protokolle der 20. Legislaturperiode nach dem Muster:
        "Dateiname": ElementTree des Dokuments
        name (str): Der Name des Korpus.
        processed (list): Eine verarbeitete Version des Korpus als Liste.

    """

    def __init__(self, name, load_processed: bool = False):
        """
        Dieser Konstruktor deserialisiert das Korpus.

        Args:
            name: Der Name des Korpus.
            load_processed: Falls ja, wird ein Korpus mit dem übergebenen Namen aus dem Ordner data/processed_corpus
            geladen und als Objektattribut processed abgespeichert.
        """
        if not load_processed:
            self.corpus = {}
            self.name = name
            self.processed = []
            for filename in os.listdir("data/xml-tei"):
                # Wir formatieren den relativen Dateipfad mit der Ordnerstruktur und dem Dateinamen.
                xml_file_path = os.path.join("data/xml-tei/", filename)
                self.corpus[filename] = ET.parse(xml_file_path)
        else:
            self.corpus = {}
            self.name = name
            with open(f'data/processed_corpus/{name}', 'r', encoding='utf-8') as json_file:
                self.processed = json.load(json_file).values()

    def get_all_speaches(self) -> list:
        """
        Mit dieser Methode werden alle Reden aus einem Korpus extrahiert. Dabei die Reden der Präsidenten oder
        Vizepräsidenten des Landtags ignoriert.

        Return:
            Eine Liste mit allen Einzeläußerungen von Mitglieder des Landtags die nicht Präsident oder Vizepräsident
            des Landtags sind ohne Metadaten.
        """
        speaches = []
        for e in self.corpus.keys():
            root = self.corpus[e]
            for sp_tag in root.findall(".//sp"):
                role = sp_tag.get("role")
                if role not in ["Vizepräsident", "Vizepräsidentin", "Präsident", "Präsidentin"]:
                    for a in sp_tag.findall(".//p"):
                        speaches.append(a.text)
        return speaches

    def serialize_corpus(self, custom_name: str = None) -> None:
        """
        Diese Funktion serialisiert ein verarbeitetes Korpus unter data/processed_corpus.

        Args:
            custom_name: Ein eigens definierter Name.
        """

        with open(f"data/processed_corpus/{self.name if not custom_name else custom_name}", "w",
                  encoding="utf-8") as f:
            json_container = {}
            for i, doc in enumerate(self.processed):
                json_container[i] = doc
            json.dump(json_container, f, ensure_ascii=False, indent=2)

    @staticmethod
    def clean_corpus(l: list[str]) -> list[str]:
        """
        Diese Methode befreit eine Liste mit Strings von Interpunktionszeichen.

        Args:
            l: Die zu bereinigende Liste.
        Returns:
            Die von Interpunktionszeichen befreite Liste.
        """
        lc = []
        for entry in l:
            lc = lc + entry.split(" ")
        lc = [entry for entry in l if not all(char in string.punctuation for char in entry)]
        translator = str.maketrans('', '', string.punctuation)
        for i, entry in enumerate(lc):
            if any(char in string.punctuation for char in entry):
                lc[i] = entry.translate(translator)
        return lc

    @staticmethod
    def normalize_case(l: list[str]) -> list[str]:
        """
        Mit dieser Funktion kann man alle Strings einer Liste zu Kleinschreibung normalisieren.

        Args:
            l: Die Liste mit strings.
        Return:
            Die nach Kleinschreibung normalisierten Strings der Liste.
        """
        return [e.lower() for e in l]

    @staticmethod
    def clean_with_custom_stopwords(path: str, l: list[str]) -> list[str]:
        """
        Diese Methode bereinigt ein Korpus mithilfe einer Stoppwortliste.

        Args:
            path: Der Dateipfad zu der Stoppwortliste.
            l: Das zu bereinigende Korpus.
        Return:
            Das bereinigte Korpus.
        """
        with open(path, 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()
        return [token for token in l if token not in stopwords]

    @staticmethod
    def lemmatize_corpus(l: list[str]) -> list[list[str]]:
        """
        Diese Methode lemmatisiert eine Liste von Strings. Außerdem werden Stoppwörter mit nltk entfernt und numerische
        Zeichen entfernt.

        Args:
            l: Die Liste mit den Dokumenten aus ggf. flektierten Termen.
        Return:
            Die tokenisierten, lemmatisierten Dokumente als Liste.
        """

        german_model = spacy.load('de_core_news_sm', disable=['parser', 'ner'])  # Lade das kleine Sprachmodell für die Lemmatisierung
        german_model.max_length = 10000000  # Vermeide Overflow-Error

        # Lade die deutschen Stoppwörter
        nltk.download('stopwords')
        german_stop_words = set(stopwords.words('german'))  # Reduziere die Stoppwortliste auf dn deutschen Teil.

        # doc = german_model(" ".join(l))
        lemmatised_corpus = []

        '''
        Wir fügen einen Token genau dann unserem lemmatisierten Korpus an, wenn er
        1) nicht auf der Stoppwortliste steht, 
        2) kein Interpunktionszeichen ist,
        3) keine Zahl ist.
        '''

        for speach in l:
            doc = german_model(speach)
            lemmatised_speach = [token.lemma_ for token in doc if
                                 token.text.lower() not in german_stop_words and not token.is_punct and not token.is_digit]
            lemmatised_corpus.append(lemmatised_speach)

        return lemmatised_corpus

    @staticmethod
    def union_multiword_expression(docs: list[list[str]]) -> list[list[str]]:
        """
        Diese Methode konkateniert alle Bigramme eines Korpus, wenn sie einem mehrteiligen Ausdruck oder einer
        Named Entity entsprechen, die ein Element der Liste data_outputs/MWE.json ist.
        Args:
            docs: Das Korpus aus Einzeldokumenten.
        Return:
            Das übergebene Korpus, indem alle mehrteiligen Ausdrücke nach data_outputs/MWE.json zu einem Token konkateniert sind.
        """

        with open('data_outputs/MWE.json', 'r', encoding='utf-8') as json_file:
            MWE = json.load(json_file)
        with open('data_outputs/MWE_reversed.json', 'r', encoding='utf-8') as json_file:
            MWE_reversed = json.load(json_file)

        mutliword_expressions = []
        for entry in MWE.values():
            for tuples in entry:
                mutliword_expressions.append(tuples)

        new_docs = []
        for doc in docs:
            new_doc = []
            skipped = False
            for i, token in enumerate(doc):
                if skipped:
                    skipped = False
                    continue
                if i < len(doc) - 1:
                    #bigram = token + " " + doc[i + 1]
                    bigram = [token, doc[i + 1]]
                    #print(bigram)
                    if bigram in mutliword_expressions:
                        new_doc.append(MWE_reversed[str(bigram)])
                        skipped = True
                    else:
                        new_doc.append(token)
                else:
                    new_doc.append(token)
            new_docs.append(new_doc)
        return new_docs
