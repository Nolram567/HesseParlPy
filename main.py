import os
import xml_validator
from xml_parser import xmlParser
from datetime import datetime


if __name__ == '__main__':

    #Wir iterieren über alle Rohdokumente.
    for filename in os.listdir("data/xml/20"):

        #Wir formatieren den realtiven Dateipfad mit der Ordnerstruktur und dem Dateinamen.
        xml_file_path = os.path.join("data/xml/20/", filename)

        '''
        Die Methode xmlParser.extract_data_from_raw_document() gibt ein 3-Tupel zurück, das - in dieser Reihenfolge - die
        Legislaturperiode, die Sitzungsnummer, das Datum und die extrahierten Textbeiträge enthält.
        '''
        legislative_term, session, date, extracted_data = xmlParser.extract_data_from_raw_document(xml_file_path)

        if not extracted_data:
            continue

        # Instanziierung eines datetime-Objekts, um das Datum später besser formatieren zu können.
        date = datetime.strptime(date, "%d.%m.%Y")

        '''
        Die Bereinigung der Daten mithilfe von List Comprehensions: Multiple Leerzeichen oder multiple Zeilenumbrüche
        jeweils mit einem Leerzeichen bzw. Zeilenumbruch ersetzt. Daraufhin wird das Inhaltsverzeichnis entfernt, das
        immer der erste Eintrag in extracted_data ist.
        '''

        extracted_data = [xmlParser.remove_multiple_spaces(e) for e in extracted_data]
        extracted_data = [xmlParser.remove_line_break(e) for e in extracted_data]
        extracted_data = [xmlParser.substitute_metacharacter(e) for e in extracted_data]
        extracted_data = extracted_data[1:]

        # Instanziierung einiger Laufvariablen.
        agenda_item_count = 1
        temp = ""
        temp2 = ""

        # Generation des XML-Deskriptors und des Headers des XML-Dokuments nach dem Hesseparl-TEI-Schema.
        temp += xmlParser.create_header(legislative_term, session, date.strftime('%d-%m-%Y'))

        #Iteration über alle extrahierten Redebeiträge im Rohdokument.
        for item in extracted_data:
            formated_text, intro = xmlParser.extract_speaker_and_text(item)

            if not formated_text:
                temp2 += item
                continue
            if temp2:
                temp2 = xmlParser.extract_introduction(temp2 + intro)
                formated_text = temp2 + formated_text
                temp2 = ""
            else:
                intro = xmlParser.extract_introduction(intro)
                formated_text = intro + formated_text

            temp += xmlParser.generate_div(item, agenda_item_count)
            temp += formated_text
            temp += "\t\t\t\t</div>\n"
            agenda_item_count += 1

        # Wir fangen den letzten Beitrag ab, der nicht mehr formatiert wird, da die Iteration terminiert.
        if temp2:
            temp += xmlParser.generate_div(temp2, agenda_item_count, False)
            temp += xmlParser.extract_introduction(temp2)
            temp += "\t\t\t\t</div>\n"


        # Wir schließen die Elemente body, text und TEI
        temp += xmlParser.create_footer()

        # Wir entfernen multiple Zeilenumbrüche.
        temp = xmlParser.remove_line_break(temp, True)

        # Wir prüfen die Wohlgeformtheit unseres XML-Strings.
        if not xml_validator.validate_syntax(temp):
            print(f"Das Dokument {xml_file_path} ist nicht wohlgeformt.")

        # Wir prüfen die Gültigkeit nach dem Schema HesseParl-TEI
        if not xml_validator.validate_schema(temp, "XSD/tei_hesseparl.xsd"):
            print(f"Das Dokument {xml_file_path} ist nicht gültig.")

        # Wir serialisieren die Datei und halten Metadaten über die Legislaturperiode, die Sitzung und das Datum im Dateinamen fest.
        filename = f"data/xml-tei_reworked/tei_{legislative_term}_{session}_{date.strftime('%d_%m_%Y')}"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(temp)

        #Wir wiederholen den Prozess für das nächste Rohdokument im Verzeichnis.
