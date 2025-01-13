# -----------------------------------------------------------------------------
# Weak-Words Analysis Tool - Modul zum Laden von Weak-Words
# -----------------------------------------------------------------------------
# Beschreibung:
# Dieses Modul kümmert sich um das Laden und Verarbeiten von Weak-Words aus
# einer YAML-Datei. Es unterstützt mehrsprachige Listen und bereitet die
# Weak-Words für die Analyse vor.
#
# Hauptfunktionen:
# - Lädt Weak-Words aus einer YAML-Datei
# - Unterstützt Mehrsprachigkeit (Deutsch, Englisch)
# - Gibt die Weak-Words in einem leicht verarbeitbaren Format zurück
#
# Benötigte Pakete:
# - pyyaml für das Parsen der YAML-Datei
#
# -----------------------------------------------------------------------------
# Änderungshistorie:
# -----------------------------------------------------------------------------
# Version  Datum         Autor                    Änderungen
# -----------------------------------------------------------------------------
# 1.0      13.01.2025    CHOE                     Initiale Erstellung
# -----------------------------------------------------------------------------
# Hinweise:
# - Die YAML-Datei muss im richtigen Format vorliegen, um korrekt geladen zu
#   werden. Sie befindet sich im Ordner `weakwords/weak_words.yaml`.
# - Mehrere Sprachen können kombiniert werden, indem die entsprechenden
#   Sprachparameter (z. B. `english`, `german`) übergeben werden.
# -----------------------------------------------------------------------------

import yaml
from modules.config import logger

def load_weak_words(file_path, languages):
    """
    Lädt die Weak-Words aus der YAML-Datei für die angegebenen Sprachen.
    """
    logger.debug(f"Lade Weak-Words aus: {file_path} für Sprachen: {languages}")
    
    try:
        # Überprüfen, ob die Datei existiert
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Die Datei '{file_path}' wurde nicht gefunden.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Fehler beim Parsen der YAML-Datei '{file_path}': {e}")
        raise
    except Exception as e:
        logger.error(f"Unbekannter Fehler beim Laden der YAML-Datei '{file_path}': {e}")
        raise

    weak_words_combined = {}
    
    # Überprüfen, ob alle angegebenen Sprachen in den geladenen Daten vorhanden sind
    missing_languages = [language for language in languages if language not in data]
    if missing_languages:
        logger.error(f"Die folgenden Sprachen wurden nicht in der YAML-Datei gefunden: {', '.join(missing_languages)}")
        raise ValueError(f"Sprache(n) {', '.join(missing_languages)} nicht in der YAML-Datei gefunden.")
    
    # Schwache Begriffe für die angegebenen Sprachen extrahieren
    for language in languages:
        weak_words_combined.update(data[language])
    
    logger.info(f"Erfolgreich {len(weak_words_combined)} Weak-Words für die Sprachen {', '.join(languages)} geladen.")
    return weak_words_combined