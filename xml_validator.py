from lxml import etree
import xmlschema

def validate_syntax(xml_string: str) -> bool:
    """
    Diese Funktion überprüft die Wohlgeformtheit eines XML-Strings.

    Args:
        xml_string: Der zu überprüfende XML-String.
    Returns:
        True, wenn der String wohlgeformt ist, anderenfalls False.
    """

    try:
        # Wenn der String erfolgreich eingelesen wird, ist er wohlgeformt.
        root = etree.fromstring(xml_string)
        return True
    except etree.XMLSyntaxError as e:
        print(f"XML-Syntaxfehler: {e}")
        return False

def validate_schema(xml_string: str, xsd_file: str) -> bool:
    """
    Diese Funktion validiert einen XML-String nach einem Schema.

    Args:
        xml_string: Der zu validierende XML-String.
        xsd_file: Der relative Dateipfad zu der XSD-Datei.
    Returns:
        True, wenn der String dem Schema entspricht, anderenfalls False.
    """
    try:
        schema = xmlschema.XMLSchema(xsd_file)
        schema.validate(xml_string)
        return True
    except xmlschema.XMLSchemaValidationError as e:
        print(f"Validierungsfehler: {e}")
        return False
    except xmlschema.XMLSchemaParseError as e:
        print(f"Schema-Fehler: {e}")
        return False
    except Exception as e:
        print(f"Ein unbekannter Fehler ist aufgetreten: {e}")
        return False


