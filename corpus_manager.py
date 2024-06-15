import os
import xml.etree.ElementTree as ET
import string
import spacy
from nltk.corpus import stopwords
import nltk

class CorpusManager:
    """
    Objekte dieser Klasse initialisieren und verwalten das Korpus.

    Attributes:
        corpus (dict): Dieses Dictionary enthält alle Protokolle der 20. Legislaturperiode nach dem Muster:
        "Dateiname": ElementTree des Dokuments
    """

    def __init__(self, name):
        """
        Dieser Konstruktor deserialisiert das Korpus.
        """
        self.corpus = {}
        self.name = name
        self.processed = []
        for filename in os.listdir("data/xml-tei"):
            # Wir formatieren den relativen Dateipfad mit der Ordnerstruktur und dem Dateinamen.
            xml_file_path = os.path.join("data/xml-tei/", filename)
            self.corpus[filename] = ET.parse(xml_file_path)

    def get_speaches_from_politican(self, p: str, id: str = "who") -> list:
        """
        Mit dieser Objektmethode kann man alle Reden einer spezifizierten Person aus einem Korpus extrahieren.

        Args:
             p: Der Name der Person.
             id: Das Attribut des sp-Elements, in dem nach dem Namen (Parameter p) gesucht werden soll. Das Standardattribut ist "who".
        Return:
            Eine Liste mit allen Einzeläußerungen der spezifizierten Person ohne Metadaten.
        """
        speaches = []
        for e in self.corpus.keys():
            root = self.corpus[e]
            for sp_tag in root.findall(f".//sp[@{id}='{p}']"):
                for a in sp_tag.findall((".//p")):
                    speaches.append(a.text)
        return speaches

    def get_speaches_from_party(self, party: str) -> list:
        """
        Mit dieser Funktion kann man alle Reden einer spezifizierten Partei aus einem Korpus extrahieren. Das Korpus sollte
        zuvor mit der Funktion create_partition() erstellt wurden sein oder konform zur Struktur des Rückgabe-Dictionaries sein.

        Args:
            party: Der Name der Partei.
        Return:
            Eine Liste mit allen Einzeläußerungen von Mitglieder der spezifizierten Partei ohne Metadaten.
        """
        speaches = []
        for e in self.corpus.keys():
            root = self.corpus[e]
            for sp_tag in root.findall(f".//sp[@parliamentary_group='{party}']"):
                for a in sp_tag.findall((".//p")):
                    speaches.append(a.text)
        return speaches

    @staticmethod
    def clean_corpus(l: list[str]) -> list[str]:
        """
        Befreit eine Liste mit Strings von Interpunktionszeichen und nicht alphabetischen Zeichenfolgen.

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
            Die nach Kleinschreibung normalisierten Strings in corpus.
        """
        return [e.lower() for e in l]

    @staticmethod
    def clean_with_custom_stoppwords(path: str, l: list[str]) -> list[str]:
        """
        Diese statische Methode bereinigt ein Korpus mithilfe einer Stoppwortliste.

        Args:
            path: Der Dateipfad.
            l: Das zu bereinigende Korpus.
        Return:
            Das bereinigte Korpus.
        """
        with open(path, 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()
        return [token for token in l if token not in stopwords]

    @staticmethod
    def lemmatize_corpus(l: list[str]) -> list[str]:
        """
        Diese Methode lemmatisiert eine Liste von Strings und entfernt Stoppwörter.

        Args:
            l: Die Liste mit den zu lemmatisierenden Strings.
        Return:
            Der tokenisierte, lemmatisierte String als Liste.
        """
        german_model = spacy.load('de_core_news_sm', disable=['parser', 'ner'])
        german_model.max_length = 10000000

        # Lade die deutschen Stoppwörter
        nltk.download('stopwords')
        german_stop_words = set(stopwords.words('german'))

        doc = german_model(" ".join(l))
        lemmas = [token.lemma_ for token in doc if token.text.lower() not in german_stop_words and not token.is_punct and not token.is_digit]
        return lemmas
