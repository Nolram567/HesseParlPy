
delegate_pattern = r"(.*?)((?<=[\)\.\?])\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33})\[(.{0,25})\]:(.*?)(?=((?:\)|\.|\?)\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33}\[.{1,25}\]:)|$)"

introduction_pattern = r"^(.*?) – Drucks\. \d+/\d+(.*?)[a-zA-Z\-\–][^.,:\(\)\?]{0,33}\[(.{1,25})\]:"

interjection_pattern = r"\(((?!.*\b(SPD|CDU|Freie Demokraten|DIE LINKE|BÜNDNIS 90/DIE GRÜNEN|AfD|fraktionslos)\b$).{10,150})\)(?=[^)]{0,30})"

minister_pattern = r"(.*?)" \
               r"(Prof\. Dr\. Michael Ronellenfitsch, Hessischer Beauftragter für Datenschutz und Informationsfreiheit:" \
                   r"|Prof\. Dr\. R\. Alexander Lorz, Kultusminister:" \
                   r"|Tarek Al-Wazir, Minister für Wirtschaft, Energie, Verkehr und Wohnen:" \
                   r"|Prof\. Dr\. Kristina Sinemus, Ministerin für Digitale Strategie und Entwicklung:" \
                   r"|Axel Wintermeyer, Minister und Chef der Staatskanzlei:" \
                   r"|Priska Hinz, Ministerin für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz:" \
                   r"|Peter Beuth, Minister des Innern und für Sport:" \
                   r"|Michael Boddenberg, Minister der Finanzen:" \
                   r"|Angela Dorn, Ministerin für Wissenschaft und Kunst:" \
                   r"|Kai Klose, Minister für Soziales und Integration:" \
                   r"|Lucia Puttrich, Ministerin für Bundes- und Europaangelegenheiten und Bevollmächtigte des Landes Hessen beim Bund:" \
                   r"|Ministerpräsident Boris Rhein:" \
                   r"|Ministerpräsident Volker Bouffier:" \
                   r"|Alterspräsident Rolf Kahnt:)" \
               r"(.*?)" \
               r"(?=(Vizepräsident|Präsident|Vizepräsidentin|Präsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):|$" \
               r"|(Prof\. Dr\. Michael Ronellenfitsch, Hessischer Beauftragter für Datenschutz und Informationsfreiheit:" \
                   r"|Prof\. Dr\. R\. Alexander Lorz, Kultusminister:|Tarek Al-Wazir, Minister für Wirtschaft, Energie, Verkehr und Wohnen:" \
                   r"|Prof\. Dr\. Kristina Sinemus, Ministerin für Digitale Strategie und Entwicklung:" \
                   r"|Axel Wintermeyer, Minister und Chef der Staatskanzlei:" \
                   r"|Priska Hinz, Ministerin für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz:" \
                   r"|Peter Beuth, Minister des Innern und für Sport:" \
                   r"|Michael Boddenberg, Minister der Finanzen:" \
                   r"|Angela Dorn, Ministerin für Wissenschaft und Kunst:" \
                   r"|Kai Klose, Minister für Soziales und Integration:" \
                   r"|Lucia Puttrich, Ministerin für Bundes- und Europaangelegenheiten und Bevollmächtigte des Landes Hessen beim Bund:" \
                   r"|Ministerpräsident Boris Rhein:" \
                   r"|Ministerpräsident Volker Bouffier:" \
                   r"|Alterspräsident Rolf Kahnt:))" \
               r"(.*)" \

functional_speaker_pattern = r"(.*?)" \
               r"(Vizepräsident|Präsident|Vizepräsidentin|Präsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):" \
               r"(.*?)" \
               r"(?=(Vizepräsident|Präsident|Vizepräsidentin|Präsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):|$" \
               r"|(Prof\. Dr\. Michael Ronellenfitsch, Hessischer Beauftragter für Datenschutz und Informationsfreiheit:" \
                             r"|Prof\. Dr\. R\. Alexander Lorz, Kultusminister:" \
                             r"|Tarek Al-Wazir, Minister für Wirtschaft, Energie, Verkehr und Wohnen:" \
                             r"|Prof\. Dr\. Kristina Sinemus, Ministerin für Digitale Strategie und Entwicklung:" \
                             r"|Axel Wintermeyer, Minister und Chef der Staatskanzlei:" \
                             r"|Priska Hinz, Ministerin für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz:" \
                             r"|Peter Beuth, Minister des Innern und für Sport:" \
                             r"|Michael Boddenberg, Minister der Finanzen:" \
                             r"|Angela Dorn, Ministerin für Wissenschaft und Kunst:" \
                             r"|Kai Klose, Minister für Soziales und Integration:" \
                             r"|Lucia Puttrich, Ministerin für Bundes- und Europaangelegenheiten und Bevollmächtigte des Landes Hessen beim Bund:" \
                             r"|Ministerpräsident Boris Rhein:" \
                             r"|Alterspräsident Rolf Kahnt:" \
                             r"|Ministerpräsident Volker Bouffier:))" \
               r"(.*)"

"""minister_pattern_old = r'''(.*)\s*(Prof\. Dr\. R\. Alexander Lorz, Kultusminister:|Tarek Al-Wazir, Minister für Wirtschaft, Energie, Verkehr und Wohnen:|Prof\. Dr\. Kristina Sinemus, Ministerin für Digitale Strategie und Entwicklung:
|Axel Wintermeyer, Minister und Chef der Staatskanzlei:
|Priska Hinz, Ministerin für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz:
|Peter Beuth, Minister des Innern und für Sport:
|Michael Boddenberg, Minister der Finanzen:
|Angela Dorn, Ministerin für Wissenschaft und Kunst:
|Kai Klose, Minister für Soziales und Integration:
|Lucia Puttrich, Ministerin für Bundes- und Europaangelegenheiten und Bevollmächtigte des Landes Hessen beim Bund:)(.*?)
(?=(Vizepräsident|Präsident|Vizepräsidentin|Präsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):|$)
'''

functional_speaker_pattern_old = r"(.*)\s*(Präsident|Präsidentin|Vizepräsident|Vizepräsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):" \
                             r"(.*?)" \
                             r"(?=(\s(Präsident|Präsidentin|Vizepräsident|Vizepräsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):)" \
                             r"|$)" \
                             r"(Prof\. Dr\. R\. Alexander Lorz, Kultusminister:|Tarek Al-Wazir, Minister für Wirtschaft, Energie, Verkehr und Wohnen:|Prof\. Dr\. Kristina Sinemus, Ministerin für Digitale Strategie und Entwicklung:|Axel Wintermeyer, Minister und Chef der Staatskanzlei:|Priska Hinz, Ministerin für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz:|Peter Beuth, Minister des Innern und für Sport:|Michael Boddenberg, Minister der Finanzen:|Angela Dorn, Ministerin für Wissenschaft und Kunst:|Kai Klose, Minister für Soziales und Integration:|Lucia Puttrich, Ministerin für Bundes- und Europaangelegenheiten und Bevollmächtigte des Landes Hessen beim Bund:))"

delegate_pattern = r"((?<=[\)\.\?])\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33})\[(.{0,25})\]:(.*?)(?=((?:\)|\.|\?)\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33}\[.{1,25}\]:)|$)"
functional_speaker_pattern_II = r"^(Vizepräsident|Präsident|Vizepräsidentin|Präsidentin)\s(Karin Müller|Heike Hofmann|Frank Lortz|Astrid Wallmann|Dr. Ulrich Wilken|Dr. h.c. Jörg-Uwe Hahn|Boris Rhein):"
"""