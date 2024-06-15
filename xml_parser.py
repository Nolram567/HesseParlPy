import xml.etree.ElementTree as ET
import re
import patterns


class xmlParser:
    """
    Diese Klasse enthält Methoden, um die rohen XML-Dateien in XML-Datei mit dem Schema "TEI" zu überführen. Zudem
    enthält dieser Klasse verschiedene Methoden, um die Rohdaten zu bereinigen.
    """

    @staticmethod
    def extract_data_from_raw_document(file_path: str) -> list[str]:
        """
        Mit dieser Methode werden die Redebeiträge und die Tagesordnungspunkte aus den Rohdokumenten extrahiert.

        Args:
            Der relative Dateipfad zu den rohen XML-Dateien.
        Returns:
            Eine Liste an Strings
            der Wahlperiode,
            der Sitzungsnummer
            und den extrahierten Redebeiträgen.
        """

        # XML-Datei einlesen
        try:
            tree = ET.parse(file_path)
        except ET.ParseError:
            print(f"{file_path} fehlerhaft")
            return ["","","",""]

        root = tree.getroot()

        # Alle <UpdateRecord>-Tags mit LockId und Clear="False" finden
        update_records = root.findall(".//UpdateRecord[@Clear='False']")

        #Extrahiere die Wahlperiode, Sitzungsnummer und das Datum.
        lp = update_records[0].find(".//Field[@Clear='True'][@InputFieldName='WP']").text
        session = update_records[0].find(".//Field[@Clear='True'][@InputFieldName='DNR']").text
        date = update_records[0].find(".//Field[@Clear='True'][@InputFieldName='DAT']").text

        text_data = []

        # Durch die gefundenen <UpdateRecord>-Tags iterieren
        for record in update_records:
            # Innerhalb jedes <UpdateRecord>, finde alle <Field>-Tags mit den spezifischen Attributen
            fields = record.findall(".//Field[@Long='True'][@Clear='True'][@InputFieldName='AVT1']")
            for field in fields:
                # Den Text aus jedem gefundenen <Field>-Tag extrahieren
                if field.text:  # Nur Text hinzufügen, wenn es nicht None ist
                    text_data.append(field.text.strip())

        return [lp, session, date, text_data]

    @staticmethod
    def create_header(lp: str, session: str) -> str:
        """
        In dieser Methode wird die XML-Deklaration und der Header eines XML-TEI-Dokuments formatiert und als String
        zurückgegeben. Außerdem werden die Tags <text> und <body> geöffnet.

        Args:
            lp: Die Legislaturperiode.
            session: Die Sitzungsnummer.
        Returns:
            Der formatierte Header als String.
        """
        return f'<?xml version="1.0" standalone="no"?>\n' \
               f'\t<TEI>\n' \
               f'\t\t<teiHeader>\n' \
               f'\t\t\t<fileDesc>\n' \
               f'\t\t\t\t<titleStmt>\n' \
               f'\t\t\t\t\t<title>Plenarprotokoll</title>\n' \
               f'\t\t\t\t\t<legislativePeriod>{lp}</legislativePeriod>\n' \
               f'\t\t\t\t\t<sessionNo>{session}</sessionNo>\n' \
               f'\t\t\t\t</titleStmt>\n' \
               f'\t\t\t\t<editionStmt>\n' \
               f'\t\t\t\t\t<edition>\n' \
               f'\t\t\t\t\t\t<package>PolMinePyHesse</package>\n' \
               f'\t\t\t\t\t\t<version/>\n' \
               f'\t\t\t\t\t\t<birthday/>\n' \
               f'\t\t\t\t\t</edition>\n' \
               f'\t\t\t\t</editionStmt>\n' \
               f'\t\t\t\t<publicationStmt>\n' \
               f'\t\t\t\t\t<publisher>Hessischer Landtag</publisher>\n' \
               f'\t\t\t\t\t<date/>\n' \
               f'\t\t\t\t\t<page/>\n' \
               f'\t\t\t\t</publicationStmt>\n' \
               f'\t\t\t\t<sourceDesc>\n' \
               f'\t\t\t\t\t<filetype>xml</filetype>\n' \
               f'\t\t\t\t\t<url/>\n' \
               f'\t\t\t\t\t<date/>\n' \
               f'\t\t\t\t</sourceDesc>\n' \
               f'\t\t\t</fileDesc>\n' \
               f'\t\t\t<encodingDesc><projectDesc>PolMinePyHesse</projectDesc>\n' \
               f'\t\t\t\t<samplingDecl/>\n' \
               f'\t\t\t\t<editorialDecl/>\n' \
               f'\t\t\t</encodingDesc>\n' \
               f'\t\t\t<profileDesc/>\n' \
               f'\t\t\t<revisionDesc/>\n' \
               f'\t\t</teiHeader>\n' \
               f'\t\t<text>\n' \
               f'\t\t\t<body>\n'


    @staticmethod
    def create_footer() -> str:
        """
        In dieser Methode werden die schließenden Tags </body>, </text> und </TEI> eines XML-TEI-Dokuments als String
        zurückgegeben.

        Returns:
            Die schließenden Tags als String.
        """
        return f"\t\t\t</body>\n\t\t</text>\n\t</TEI>"

    @staticmethod
    def remove_multiple_spaces(text: str) -> str:
        """
        Diese Methode ersetzt beim übergebenen String mittels eines regulären Ausdrucks multiple Whitespaces mit genau
        einem Whitespace.

        Args:
            text: Der String, der von multiplen Whitespaces befreit werden soll.
        Returns:
            Der von multiplen Whitespaces befreite String.
        """
        return re.sub(r'\s+', ' ', text)

    @staticmethod
    def remove_line_break(text: str, m: bool = False) -> str:
        """
        Diese Methode ersetzt beim übergebenen String Zeilenumbrüche mit einem leeren String.

        Args:
            text: Der String, der von Zeilenumbrüchen befreit werden soll.
            m: Dieser Parameter spezifiziert, ob nur multiple Zeilenumbrüche entfernt werden sollen oder alle.
        Returns:
            Der von Zeilenumbrüchen befreite String.
        """
        return re.sub(r'\n{2}', '\n', text) if m else re.sub(r'\n', '', text)

    @staticmethod
    def substitute_metacharacter(text: str) -> str:
        """
        Diese Methode bereinigt und substituiert XML-Metazeichen, die in wohlgeformten XML-Dokumenten nicht auftauchen dürfen.

        Args:
            text: Der zu bereinigende Text.
        Returns:
            Der bereinigte Text.
        """
        text = text.replace("&", "and")
        text = re.sub(r"[<>]", "", text)
        return text

    @staticmethod
    def generate_div(text: str, c: int, regular: bool = True) -> str:
        """
        Diese Methode erzeugt einen <div>-Tag mit den Attributen 'type', 'n' und 'desc'. Der 'type' ist hier immer ein
        'agenda_item', d. h. ein Tagesordnungspunkt innerhalb einer Sitzung wie ein Antrag einer Fraktion oder eine
        Fragestunde. Das Attribut 'n' nummeriert die <div>-Tags einer Sitzung und das Attribut 'desc' beinhaltet den
        Titel des Tagesordnungspunkt, sofern ein Titel gefunden wird.

        Args:
            text: Der unformatierte Tagesordnungspunkt.
            c: Der Zähler der agenda_items.
            regular: False, wenn es sich um einen Spezialfall handelt.
        Returns:
            Der formatierte <div>-Tag für den Tagesordnungspunkt.

        """
        if not regular and "Amtliche Mitteilungen" in text:
            return f'\t\t\t\t<div type="agenda_item" n="{c}" what="" desc="Amtliche Mitteilungen">\n'
        if not regular:
            return f'\t\t\t\t<div type="agenda_item" n="{c}" what="" desc="">\n'

        match = re.search(r"^(.*?) – Drucks\. \d+/\d+", text)
        if match:
            return f'\t\t\t\t<div type="agenda_item" n="{c}" what="" desc="{match.group(1)}">\n'
        else:
            return f'\t\t\t\t<div type="agenda_item" n="{c}" what="" desc="">\n'

    @staticmethod
    def extract_speaker_and_text(text: str) -> tuple[str, str]:
        """
        Diese zentrale Methode des Parsers partitioniert die Redebeiträge einer Sitzung zunächst nach Redebeiträge von
        Abgeordneten. Diese Partitionen enthalten zumeist weitere Redebeiträge von (Vize)Präsidenten des Landtags oder
        Ministern. Mittels einer Fallunterscheidung werden das weitere Vorgehen festgelegt. Die Fallunterscheidung wird
        danach iterativ so lange angewandt, bis der nächste Redebeitrag eines Abgeordneten beginnt. Die Partitionen
        werden jeweils nach dem gewünschten Schema mit der Methode format_paragraphs_and_interjections() formatiert. Der
        String Builder fungiert in dieser Prozedur als 'Stack', auf dem sukzessive fertig formatierte Redebeiträge
        abgelegt werden.

        Args:
            text: Der String, der partitioniert, ausgezeichnet und annotiert werden soll.
        Returns:
            Die partitionierten, ausgezeichneten und annotierten Redebeiträge als String.
        """
        # Das Pattern, das den/die Präsident*in nicht berücksichtigt.
        pattern = re.compile(patterns.delegate_pattern)
        matches = re.finditer(pattern, text)
        builder = ""
        intro = ""

        for i, match in enumerate(matches):
            
            content = match.group(4)

            if i == 0:
                intro = match.group(1)
                """print(intro)
                builder += f'\t\t\t\t\t<sp who="" parliamentary_group="" ' \
                           f'role="" position="" who_original="" party="" name="">\n' \
                           f'{xmlParser.format_paragraphs_and_interjections(intro)}' \
                           f'</sp>\n'
                """

            functional_speaker = xmlParser.extract_functional_speaker(match.group(4))

            minister_speaker = xmlParser.extract_minister_speaker(match.group(4))

            current_speaker = f'\t\t\t\t\t<sp who="{match.group(2).strip()}" parliamentary_group="{match.group(3).strip()}" ' \
                              f'role="" position="" who_original="" party="{match.group(3)}" name="">'

            if functional_speaker and minister_speaker:

                if functional_speaker[8] < minister_speaker[7]:
                    builder += f'{current_speaker}\n'\
                    f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[0])}\n'\
                    f'\t\t\t\t\t</sp>\n'
                    f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n'\
                    f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}\n'\
                    f'\t\t\t\t\t</sp>\n'

                    if functional_speaker[7]:
                        builder = xmlParser.handle_loop(functional_speaker[7], builder)

                else:
                    builder += f'{current_speaker}\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[0])}\n'\
                          f'\t\t\t\t\t</sp>\n'
                    name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                    builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}\n'\
                          f'\t\t\t\t\t</sp>\n'
                    if minister_speaker[6]:
                        builder = xmlParser.handle_loop(minister_speaker[6], builder)

            elif functional_speaker:
                builder += f'{current_speaker}\n'\
                      f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[0])}\n'\
                      f'\t\t\t\t\t</sp>\n'\
                      f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n'\
                      f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}\n'\
                      f'\t\t\t\t\t</sp>\n'
                if functional_speaker[7]:
                    builder = xmlParser.handle_loop(functional_speaker[7], builder)

            elif minister_speaker:
                builder += f'{current_speaker}\n'\
                      f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[0])}\n'\
                      f'\t\t\t\t\t</sp>\n'
                name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n'\
                      f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}\n'\
                      f'\t\t\t\t\t</sp>\n'
                if minister_speaker[6]:
                    builder = xmlParser.handle_loop(minister_speaker[6], builder)
            else:
                builder += f'{current_speaker}\n'\
                           f'{xmlParser.format_paragraphs_and_interjections(content)}\n'\
                           f'\t\t\t\t\t</sp>\n'

        return builder, intro

    @staticmethod
    def handle_loop(remainder: str, builder: str) -> str:
        """
        Die Methode fungiert als Helfermethode für extract_speaker_and_text() und wendet die darin enthaltene Logik der
        Fallunterscheidung iterativ an, bis der Redebeitrag endet.

        Args:
            remainder: Der restliche Text, der nach der Applikation der ersten Fallunterscheidung übrig geblieben ist.
            builder: Der 'Stack' der Hauptmethode, auf dem die fertig formatierten Redebeiträge abgelegt werden.
        Returns:
            Der fertig formatierte Partition, die als remainder übergeben wurde.
        """

        while remainder:

            functional_speaker = xmlParser.extract_functional_speaker(remainder)

            minister_speaker = xmlParser.extract_minister_speaker(remainder)

            if not functional_speaker and not minister_speaker:
                return builder

            if functional_speaker and minister_speaker:

                if functional_speaker[8] < minister_speaker[7]:
                    builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}'\
                          f'\t\t\t\t\t</sp>\n'
                    name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                    builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}'\
                          f'\t\t\t\t\t</sp>\n'
                    remainder = minister_speaker[6]
                    continue
                else:
                    name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                    builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}'\
                          f'\t\t\t\t\t</sp>\n'
                    builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n'\
                          f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}'\
                          f'\t\t\t\t\t</sp>\n'
                    remainder = functional_speaker[7]
                    continue
            elif functional_speaker:
                builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n'\
                        f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}'\
                        f'\t\t\t\t\t</sp>\n'
                remainder = functional_speaker[7]
                continue
            elif minister_speaker:
                name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n'\
                           f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}'\
                           f'\t\t\t\t\t</sp>\n'
                remainder = minister_speaker[6]
                continue

        return builder

    @staticmethod
    def extract_introduction(text: str) -> str:
        """
        Die Methode fungiert als Helfermethode für extract_speaker_and_text() und extrahiert Beiträge

        Args:
            text: Der restliche Text, der nach der Applikation der ersten Fallunterscheidung übrig geblieben ist.
            builder: Der 'Stack' der Hauptmethode, auf dem die fertig formatierten Redebeiträge abgelegt werden.
        Returns:
            Der fertig formatierte Partition, die als remainder übergeben wurde.
        """

        builder = ""

        while text:

            functional_speaker = xmlParser.extract_functional_speaker(text)

            minister_speaker = xmlParser.extract_minister_speaker(text)

            if not functional_speaker and not minister_speaker:
                builder += f'\t\t\t\t\t<sp who="" parliamentary_group="" role="" position="" who_original="" party="" name="">\n' \
                           f'{xmlParser.format_paragraphs_and_interjections(text)}' \
                           f'\t\t\t\t\t</sp>\n'
                return builder

            if functional_speaker and minister_speaker:

                if functional_speaker[8] < minister_speaker[7]:
                    builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n' \
                               f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}' \
                               f'\t\t\t\t\t</sp>\n'
                    name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                    builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n' \
                               f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}' \
                               f'\t\t\t\t\t</sp>\n'
                    text = minister_speaker[6]
                    continue
                else:
                    name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                    builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n' \
                               f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}' \
                               f'\t\t\t\t\t</sp>'
                    builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n' \
                               f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}' \
                               f'\t\t\t\t\t</sp>'
                    text = functional_speaker[7]
                    continue
            elif functional_speaker:
                builder += f'\t\t\t\t\t<sp who="{functional_speaker[2]}" parliamentary_group="" role="{functional_speaker[1]}" position="" who_original="" party="" name="">\n' \
                           f'{xmlParser.format_paragraphs_and_interjections(functional_speaker[3])}' \
                           f'\t\t\t\t\t</sp>'
                text = functional_speaker[7]
                continue
            elif minister_speaker:
                name, function = xmlParser.divide_name_and_function(minister_speaker[1])
                builder += f'\t\t\t\t\t<sp who="{name}" parliamentary_group="" role="{function}" position="" who_original="" party="" name="">\n' \
                           f'{xmlParser.format_paragraphs_and_interjections(minister_speaker[2])}' \
                           f'\t\t\t\t\t</sp>'
                text = minister_speaker[6]
                continue

        return builder

    @staticmethod
    def divide_name_and_function(text: str) -> tuple[str, str]:
        """
        Diese Method trennt den Namen und die Funktion eines Ministers oder des Ministerpräsidenten und gibt ihn als Tupel
        zurück.

        Args:
             Der/die Minister*in als String.
        Returns:
            Ein Tupel mit dem Ressort und dem Namen in dieser Reihenfolge.
        """
        name_and_function = text.split(', ', 1)
        if len(name_and_function) == 1:
            temp = name_and_function[0].split(" ", 1)
            return temp[1], temp[0]
        if len(name_and_function) == 2:
            return name_and_function[0], name_and_function[1].replace(":", "")
        if len(name_and_function) > 2:
            return name_and_function[0], "".join(name_and_function[0:]).replace(":", "")

    @staticmethod
    def extract_functional_speaker(text: str) -> list[str]:
        """
        Diese Methode partitioniert den als Argument übergebenen String in 9 capture groups und gibt diese als Liste zurück.
        Wenn kein match gefunden wird, wird der Liste das Element "None" hinzugefügt.

        Die erste Gruppe enthält den Text, bevor ein Redebeitrag des/der (Vize)präsident*in beginnt.
        Die zweite Gruppe enhält die genaue Funktion des/der sprechenden (Vize)präsident*in.
        Die dritte Gruppe enhält den Namen des/der sprechenden (Vize)präsident*in.
        Die vierte Gruppe enthält den Redbeitrag des/der (Vize)präsident*in.
        Die fünfte Gruppe enthält die Funktion des nachfolgenden Sprechers, sofern der/die Vizepräsident*in spricht.
        Die sechste Gruppe enthält den Namen des nachfolgenden Sprechers, sofern der/die Vizepräsident*in spricht.
        Die siebte Gruppe enthält den Namen und das Ressort des nachfolgenden Sprechers, sofern ein Minister spricht.
        Die siebte Gruppe enthält den restlichen Text.
        Das achte Listenelement enthält den Startindex des ersten Sprechers.

        Args:
            text: Der String, der partitioniert werden soll.
        Returns:
            Eine Liste mit den capture groups und dem Startindex des ersten Sprechers.
        """

        speaker_pattern = patterns.functional_speaker_pattern
        matches = re.finditer(speaker_pattern, text)


        for match in matches:
            # Inhalte_before, function, speaker, inhalte_after, if_functional: function, if_functional: Name, if_minister: Name+function, remainder, start_index; len 9
            return [match.group(1) if match.group(1) else None,
                    match.group(2) if match.group(2) else None,
                    match.group(3) if match.group(3) else None,
                    match.group(4) if match.group(4) else None,
                    match.group(5) if match.group(5) else None,
                    match.group(6) if match.group(6) else None,
                    match.group(7) if match.group(7) else None,
                    match.group(8) if match.group(8) else None,
                    match.start(2) if match.group(2) else None
                    ]

    @staticmethod
    def extract_minister_speaker(text: str) -> list[str]:
        """
        Diese Methode partitioniert den als Argument übergebenen String in 8 capture groups und gibt diese als String zurück.
        Wenn kein match gefunden wird, wird der Liste das Element "None" hinzugefügt.

        Die erste Gruppe enthält den Text, bevor (der erste) Redebeitrag eines Ministers beginnt.
        Die zweite Gruppe enhält den Namen und das Ressort des sprechenden Ministers.
        Die dritte Gruppe enthält den Redebeitrag des Ministers.
        Die vierte Gruppe enthält die Funktion des nachfolgenden Sprechers, sofern der/die Vizepräsident*in spricht.
        Die fünfte Gruppe enthält den Namen des nachfolgenden Sprechers, sofern der/die Vizepräsident*in spricht.
        Die sechste Gruppe enthält den Namen und das Ressort des nachfolgenden Sprechers, sofern ein Minister spricht.
        Die siebte Gruppe enthält den restlichen Text.
        Das achte Listenelement enthält den Startindex des ersten Sprechers.

        Args:
            text: Der String, der partitioniert werden soll.
        Returns:
            Eine Liste mit den capture groups und dem Startindex des ersten Sprechers.
        """

        speaker_pattern = patterns.minister_pattern

        matches = re.finditer(speaker_pattern, text)

        for match in matches:
            # Inhalte_before, minister, inhalte_after, if_functional: function, if_functional: Name, if_minister: Name+function, remainder, start_index; len:8
            return [match.group(1) if match.group(1) else None,
                    match.group(2) if match.group(2) else None,
                    match.group(3) if match.group(3) else None,
                    match.group(4) if match.group(4) else None,
                    match.group(5) if match.group(5) else None,
                    match.group(6) if match.group(6) else None,
                    match.group(7) if match.group(7) else None,
                    match.start(2) if match.group(2) else None
                    ]

    @staticmethod
    def format_paragraphs_and_interjections(text: str) -> str:
        """
        Diese Methode separiert den Redebeitrag von den Zwischenrufen. Die einzelnen Absätze werden mit einem <p>-Tag
        ausgezeichnet und die Zwischenrufe mit einem <stage>-Tag.

        Args:
            text: Der auszuzeichnende String.
        Returns:
            Der ausgezeichnete String.
        """

        regex = re.compile(patterns.interjection_pattern)

        last_match_end = 0
        formatted_text = ""

        # Durchsuche den Text nach dem gegebenen Pattern
        for match in regex.finditer(text):
            # Extrahiere die Textteile vor und während des Matches
            before_interjection = text[last_match_end:match.start()]
            interjection = match.group()

            # Wir fangen noch nicht erfasste Redebeiträge der (Vize)Präsident*innen ab.
            if before_interjection.strip():

                formatted_text += f"\t\t\t\t\t\t<p>{before_interjection.strip()}</p>\n"
            # Füge die Interjektion hinzu
            formatted_text += f'\t\t\t\t\t\t<stage type="interjection">{interjection}</stage>\n'

            # Aktualisiere den letzten Match-Endindex
            last_match_end = match.end()

        # Überprüfe, ob nach dem letzten Match noch Text übrig ist
        remaining_text = text[last_match_end:]
        if remaining_text.strip():
            formatted_text += f"\t\t\t\t\t\t<p>{remaining_text.strip()}</p>\n"

        return formatted_text