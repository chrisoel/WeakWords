# -----------------------------------------------------------------------------
# Weak-Words Analysis Tool - Modul zur Erstellung von Zusammenfassungen
# -----------------------------------------------------------------------------
# Beschreibung:
# Dieses Modul erstellt eine übersichtliche PDF-Zusammenfassung der Analyse
# von Weak-Words. Die Zusammenfassung enthält eine Auflistung aller gefundenen
# Weak-Words sowie deren Häufigkeit und Beschreibung.
#
# Hauptfunktionen:
# - Generiert ein PDF mit den Ergebnissen der Weak-Words-Analyse
# - Gruppiert die Ergebnisse nach Kategorien
# - Fügt Beschreibungen und Häufigkeiten hinzu
#
# Benötigte Pakete:
# - pymupdf (PyMuPDF) für die Erstellung von PDF-Dokumenten
#
# -----------------------------------------------------------------------------
# Änderungshistorie:
# -----------------------------------------------------------------------------
# Version  Datum         Autor                    Änderungen
# -----------------------------------------------------------------------------
# 1.0      13.01.2025    CHOE                     Initiale Erstellung
# -----------------------------------------------------------------------------
# Hinweise:
# - Die Platzierung der Inhalte erfolgt dynamisch, um die Seiten optimal zu
#   nutzen.
# - Die Zusammenfassungs-PDF wird im `data/output`-Ordner gespeichert.
# - Die PDF-Datei enthält eine detaillierte Auflistung der gefundenen Weak-Words,
#   einschließlich Häufigkeit und Beschreibung.
# -----------------------------------------------------------------------------

import os
import fitz
from modules.config import logger

def save_summary_as_pdf(input_file, weak_words_with_comments, category_counts, weak_word_counts, output_file, summary_type="findings"):
    """
    Speichert die Zusammenfassung der Weak-Words-Analyse in einer PDF.
    """
    logger.debug(f"Erstelle Zusammenfassung für: {input_file}")
    
    try:
        # PDF-Dokument öffnen und neue Seite erstellen
        pdf_document = fitz.open()
        summary_page = pdf_document.new_page()
    except Exception as e:
        logger.error(f"Fehler beim Öffnen oder Erstellen des PDF-Dokuments: {e}")
        raise
    
    y_offset = 50

    try:
        # Titel der Zusammenfassung einfügen
        summary_page.insert_text(
            (50, y_offset),
            f"Zusammenfassung der Weak-Words Analyse für {os.path.basename(input_file)}",
            fontsize=12, fontname="Helvetica-Bold"
        )
        y_offset += 30
    except Exception as e:
        logger.error(f"Fehler beim Einfügen des Titels in das PDF: {e}")
        raise

    try:
        # Iteriere durch Kategorien und füge Text hinzu
        for category, words in weak_words_with_comments.items():
            category_total = category_counts.get(category, 0)
            if category_total > 0:
                summary_page.insert_text((50, y_offset), f"Kategorie: {category} - {category_total} Vorkommen", fontsize=9)
                y_offset += 20
                for word, comment in words.items():
                    word_count = weak_word_counts.get(word, 0)
                    if word_count > 0:
                        summary_page.insert_text((60, y_offset), f"{word}: {word_count}", fontsize=8)
                        summary_page.insert_text((70, y_offset + 10), f"Beschreibung: {comment}", fontsize=7)
                        y_offset += 30
                    if y_offset > 750:
                        summary_page = pdf_document.new_page()
                        y_offset = 50
    except Exception as e:
        logger.error(f"Fehler beim Einfügen der Weak-Words-Daten in das PDF: {e}")
        raise

    try:
        # PDF speichern
        pdf_document.save(output_file)
        pdf_document.close()
        logger.info(f"Zusammenfassung gespeichert: {output_file}")
    except Exception as e:
        logger.error(f"Fehler beim Speichern des PDF-Dokuments: {e}")
        raise