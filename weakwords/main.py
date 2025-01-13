# -----------------------------------------------------------------------------
# Weak-Words Analysis Tool
# -----------------------------------------------------------------------------
# Beschreibung:
# Dieses Python-Skript dient zur Analyse von Weak-Words in PDF-Dokumenten.
# Schwache Begriffe (Weak-Words) werden basierend auf einer YAML-Datei markiert
# und optional mit Kommentaren versehen, um unklare oder vage Formulierungen
# hervorzuheben.
#
# Hauptfunktionen:
# - Unterstützung für mehrsprachige Weak-Words-Listen (Deutsch/Englisch)
# - Automatisches Hervorheben und Kommentieren von Weak-Words in PDF-Dokumenten
# - Einfache Erweiterbarkeit durch Anpassung der YAML-Datei
#
# Benötigte Pakete:
# - pymupdf (PyMuPDF) für die PDF-Verarbeitung
# - pyyaml für das Laden der Weak-Words aus einer YAML-Datei
#
# -----------------------------------------------------------------------------
# Änderungshistorie:
# -----------------------------------------------------------------------------
# Version  Datum         Autor                    Änderungen
# -----------------------------------------------------------------------------
# 1.0      13.01.2025    CHOE                     Initiale Erstellung
# -----------------------------------------------------------------------------
# Hinweise:
# - Zum Installieren der Abhängigkeiten: pip install -r requirements.txt
# - Zum Erweitern der Weak-Words-Liste muss die YAML-Datei bearbeitet werden.
# - Die generierte Datei mit markierten Weak-Words wird als neue PDF gespeichert.
# - Alle zu prüfenden Dateien müssen in den **Input-Ordner** abgelegt werden (`data/input`).
# - Alle Ausgabedateien (markierte PDFs und Zusammenfassungen) werden im **Output-Ordner** gespeichert (`data/output`).
# - Die Schwächen (Weak-Words) können durch Bearbeiten der YAML-Datei **weakwords/weak_words.yaml** angepasst werden.
# -----------------------------------------------------------------------------

import os
from modules.config import WEAK_WORDS_FILE, logger
from modules.weak_words_loader import load_weak_words
from modules.pdf_processor import highlight_weak_words_in_pdf
from modules.summary_generator import save_summary_as_pdf

def process_all_files(input_folder, languages):
    """
    Verarbeitet alle Dateien im Input-Ordner und führt die Analyse durch.
    """
    logger.info("Starte die Verarbeitung der PDF-Dateien.")
    
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('.pdf'):
            logger.info(f"Verarbeite Datei: {file_name}")
            
            try:
                # Die Weak-Words für die gewählten Sprachen laden
                weak_words_with_comments = load_weak_words(WEAK_WORDS_FILE, languages)
                
                # Die Analyse durchführen
                category_counts, weak_word_counts = highlight_weak_words_in_pdf(
                    file_path, weak_words_with_comments, apply_marking=True
                )
                
                # Ausgabe-Dateipfad anpassen
                base_name = os.path.splitext(file_name)[0]
                output_pdf = f"data/output/{base_name}_weak_words_marked_{'_'.join(languages)}.pdf"
                summary_pdf = f"data/output/{base_name}_weak_words_findings_{'_'.join(languages)}.pdf"
                
                # Ergebnisse als PDF speichern
                save_summary_as_pdf(file_path, weak_words_with_comments, category_counts, weak_word_counts, summary_pdf, summary_type="findings")
                logger.info(f"Ergebnisse gespeichert: {summary_pdf}")
                
            except Exception as e:
                logger.error(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

def main():
    input_folder = "data/input"
    languages = ["english", "deutsch"]
    process_all_files(input_folder, languages)

if __name__ == "__main__":
    main()