# HesseParlPy

Dieses Repository enthält den Code und die Datensätze, die im Rahmen meiner Masterarbeit entstehen. Ich habe auf der Grundlage der semi-strukturierten Rohdokumente
ein XML-TEI-Korpus der Plenarprotokolle der 20. Legislaturperiode des hessischen Landtags generiert.

Auf Grundlage dieses Korpus wird ein Topic Model berechnet. 

## Ordnerstruktur

Die folgende Struktur zeigt die Organisation der Projektordner und -dateien:

```plaintext
PolMinePyHesse/
│ 
├── data/
│   ├── xml/
│   ├── xml-tei/
│   ├── processed_corpus/
│   └── CLARIN PUB end-user license +BY +NC +SA v2.1 -- Die Korpuslizenz. 
├── data_outputs/
│   ├── topicmodels/
│   ├── stoppwords.txt -- Ein eigens - mithilfe von tf-idf - generierte Stoppwortliste für das Korpus.
│   ├── tf-idf_results.txt -- Die mittleren tf-idf-Werte.
│   ├── MWE.json -- Statistisch bedeutsame MWE und NE im Korpus.
│   └── MWE_reversed.json -- Abbildung der Bigramme auf die MWE und NE.
├── docs/
│   └── Die HTML-Dokumente der Github-Page.
├── lda_visualisations/
│   └── Die mit pyLDAvis erzeugten Visualisierungen für Themenmodelle.
├── XSD
│   └── hesseparl_tei.xsd -- Ein XSD-Dokument, um die formale Struktur der Dokumente zu validieren.
├── data_analyzer.py -- Die Analyse der rohen und schemalosen XML-Dokumente.
├── xml_parser.py -- Der Parser.
├── parser_script.py -- Die Parsing-Prozedur
├── patterns.py -- Reguläre Ausdrücke für den Parser.
├── xml_validator.py -- Funktionen für die Validierung der Wohlgeformtheit und der Validität nach einem XSD.
├── corpus_manager.py -- Enthält die Klasse CorpusManager, um das hesseparl-tei-Korpus einzulesen und zu verwalten.
├── cooccurrence_miner.py -- Das Skript enthält eine Prozedur, um Kookkurrenzen bzw. Kollokationen zu berechnen, um daraus bededeutsame MWE und NE abzuleiten.
├── text_miner.py -- Enthält Funktionen für das Text-Mining.
└── topic_miner.py -- Berechnet die Korrelationen zwischen den Themenpaaren und visualisiert die Verteilung als Boxplot.
