# Das Pattern für die Abgeordneten.
delegate_pattern = r"(.*?)((?<=[\)\.\?])\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33})\[(.{0,25})\]:(.*?)(?=((?:\)|\.|\?)\s[a-zA-Z\-\–][^.,:\(\)\?]{0,33}\[.{1,25}\]:)|$)"

# Das Pattern für die Einleitung.
introduction_pattern = r"^(.*?) – Drucks\. \d+/\d+(.*?)[a-zA-Z\-\–][^.,:\(\)\?]{0,33}\[(.{1,25})\]:"

# Das Pattern für die Zwischenrufe.
interjection_pattern = r"\(((?!.*\b(SPD|CDU|Freie Demokraten|DIE LINKE|BÜNDNIS 90/DIE GRÜNEN|AfD|fraktionslos)\b$).{10,150})\)(?=[^)]{0,30})"

# Das Pattern für die Minister.
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

# Das Pattern für das Präsidium.
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