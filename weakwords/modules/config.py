# -----------------------------------------------------------------------------
# Weak-Words Analysis Tool - Konfigurationsmodul
# -----------------------------------------------------------------------------
# Beschreibung:
# Dieses Modul enthält alle zentralen Konfigurationen und globalen Einstellungen
# für das Weak-Words Analysis Tool. Dazu gehören Datei- und Pfadangaben,
# Logging-Einstellungen sowie Optionen zur Steuerung der Markierungen.
#
# Hauptfunktionen:
# - Definiert globale Pfade und Konstanten für die Eingabe- und Ausgabedateien
# - Konfiguriert das Logging-System
# - Ermöglicht einfache Anpassung durch zentrale Verwaltung der Parameter
#
# Benötigte Pakete:
# - logging für die Protokollierung von Prozessen und Fehlern
#
# -----------------------------------------------------------------------------
# Änderungshistorie:
# -----------------------------------------------------------------------------
# Version  Datum         Autor                    Änderungen
# -----------------------------------------------------------------------------
# 1.0      13.01.2025    CHOE                     Initiale Erstellung
# -----------------------------------------------------------------------------

import logging
import os

# Globale Einstellungen
INPUT_FILE_PATH = r"data/input/testdatei.pdf"
WEAK_WORDS_FILE = "weakwords/weak_words.yaml"
OUTPUT_FILE_PATH = r"data/output/testdatei_weak_words_marked.pdf"
SUMMARY_FILE_PATH = r"data/output/weak_words_findings.pdf"

apply_marking = True

# Logging konfigurieren
try:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.FileHandler("weak_words.log"),
        logging.StreamHandler()
    ])
    # Logger für das gesamte Projekt bereitstellen
    logger = logging.getLogger(__name__)
except Exception as e:
    print(f"Fehler beim Konfigurieren des Loggers: {e}")
    raise

# Überprüfen, ob die Verzeichnisse existieren und gegebenenfalls erstellen
try:
    # Überprüfen, ob der Input-Ordner existiert, wenn nicht, dann erstellen
    if not os.path.exists("data/input"):
        logger.warning("Input-Ordner 'data/input' existiert nicht. Er wird jetzt erstellt.")
        os.makedirs("data/input")

    # Überprüfen, ob der Output-Ordner existiert, wenn nicht, dann erstellen
    if not os.path.exists("data/output"):
        logger.warning("Output-Ordner 'data/output' existiert nicht. Er wird jetzt erstellt.")
        os.makedirs("data/output")

    # Überprüfen, ob der Pfad zur Weak-Words-Datei existiert
    if not os.path.isfile(WEAK_WORDS_FILE):
        logger.error(f"Die Weak-Words-Datei '{WEAK_WORDS_FILE}' wurde nicht gefunden.")
        raise FileNotFoundError(f"Die Datei {WEAK_WORDS_FILE} konnte nicht gefunden werden.")
    
except FileNotFoundError as e:
    logger.error(f"Fehler beim Überprüfen der Verzeichnisse oder Dateien: {e}")
    raise
except Exception as e:
    logger.error(f"Unbekannter Fehler bei der Verzeichnisprüfung oder Dateianordnung: {e}")
    raise