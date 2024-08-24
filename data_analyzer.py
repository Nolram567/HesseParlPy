import re
from re import Pattern
import os

class dataAnalyzer:

    @staticmethod
    def find_expression(doc: str, pattern: Pattern[str], p: bool = True) -> list[str] or None:
        """
        Diese Methode sucht und sammelt alle Vorkommen von aus Ausdrücken in einem String, die zu einem
        regulären Ausdruck passen. Die gesammelten Ausdrücke werden entweder gedruckt oder als Liste zurückgegeben,
        je nachdem, ob der Paramter p wahr oder falsch ist.

        Args:
            doc: Das als String deserialisierte Dokument.
            pattern: Der reguläre Ausdruck, der gematcht werden soll.
            p: Ein Schalter, der standardmäßig wahr ist und die gefundenen Strings druckt; anderenfalls werden die
            gefundenen Ausdrücke gesammelt und als Liste zurückgegeben.
        Returns:
            None oder eine Liste mit gematchten Ausdrücken.
        """
        pattern = re.compile(pattern)
        matches = re.finditer(pattern, doc)
        if not p:
            return_list = []
            for match in matches:
                return_list.append(match.group())
            return return_list
        else:
            for match in matches:
                print(match.group())

    @staticmethod
    def find_unique_tags(directory_path: str, regex: str) -> None:
        """
        Diese statische Methode findet alle Ausdrücke innerhalb einer Sammlung von Dokumenten, die zu einem regulären
        Ausdruck passen und druckt sie in der Konsole.

        Args:
            directory_path: Der Dateipfad als String, der relativ zum Arbeitsverzeichnis den Ordner referenziert,
            der die Dokumente enthält, die durchsucht werden sollen.
            regex: Das Pattern, nach dem gesucht werden soll.
        """
        unique_tags = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".xml"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, "r", encoding='utf-8') as file:
                    content = file.read()
                    tags = dataAnalyzer.find_expression(content, regex, p=False)
                    if tags:
                        unique_tags.extend(tags)

        print("Einzigartige Field-Tags gefunden:", list(set(unique_tags)))


if __name__ == "__main__":

    # Ein regulärer Ausdruck, der alle <Field>-Tags in XML matcht.
    regexI = r'<Field[^>]*>'

    # Ein regulärer Ausdruck der alle XML-Tags matcht.
    regexII = r'<[^>]*>'

    dataAnalyzer.find_unique_tags("data/xml/20", regexI)
    #dataAnalyzer.find_unique_tags("data/xml/20", regexII)
    '''
    Einzigartige Field-Tags gefunden: ['<Field Clear="True" InputFieldName="DNRB"/>',
    '<Field Clear="True" InputFieldName="DATER">', '<Field Clear="True" InputFieldName="SEITV">',
    '<Field Clear="True" InputFieldName="ZUGA">', '<Field Long="True" Clear="True" InputFieldName="TOP">',
    '<Field Long="True" Clear="True" InputFieldName="AVT1">', '<Field Clear="True" InputFieldName="BDOK">',
    '<Field Clear="True" InputFieldName="SEITB">', '<Field Clear="True" InputFieldName="ASEIV">',
    '<Field Clear="True" InputFieldName="TOPSP">', '<Field Clear="True" InputFieldName="ASEIV"/>',
    '<Field Clear="True" InputFieldName="DATNA">', '<Field Clear="True" InputFieldName="ANR"/>',
    '<Field Clear="True" InputFieldName="ANR">', '<Field Clear="True" InputFieldName="DATFO">',
    '<Field Clear="True" InputFieldName="RNRD">', '<Field Clear="True" InputFieldName="SEIT">',
    '<Field Long="True" Clear="True" InputFieldName="AVT1"/>', '<Field Clear="True" InputFieldName="DATGE">',
    '<Field Clear="True" InputFieldName="QUELL">', '<Field Clear="True" InputFieldName="DAT">',
    '<Field Clear="True" InputFieldName="SEITB"/>', '<Field Clear="True" InputFieldName="ASEIB">',
    '<Field Clear="True" InputFieldName="AKAT">', '<Field Clear="True" InputFieldName="ASEIB"/>',
    '<Field Clear="True" InputFieldName="DNRB">', '<Field Clear="True" InputFieldName="WP">',
    '<Field Clear="True" InputFieldName="RED">', '<Field Clear="True" InputFieldName="ASEI">',
    '<Field Clear="True" InputFieldName="DATGR">', '<Field Clear="True" InputFieldName="DNR">',
    '<Field Clear="True" InputFieldName="DART">']
    '''

