# -----------------------------------------------------------------------------
# Weak-Words Analysis Tool - PDF-Verarbeitungsmodul
# -----------------------------------------------------------------------------
# Beschreibung:
# Dieses Modul verarbeitet PDF-Dokumente, sucht nach Weak-Words und markiert
# diese optional. Es zählt Vorkommen und bereitet die Ergebnisse für die
# Zusammenfassung vor.
#
# Hauptfunktionen:
# - Durchsucht PDF-Dokumente nach Weak-Words
# - Markiert Weak-Words (optional)
# - Zählt Vorkommen und kategorisiert Ergebnisse
#
# Benötigte Pakete:
# - pymupdf (PyMuPDF) für die Verarbeitung von PDF-Dokumenten
# - re für die Erstellung regulärer Ausdrücke
#
# -----------------------------------------------------------------------------
# Änderungshistorie:
# -----------------------------------------------------------------------------
# Version  Datum         Autor                    Änderungen
# -----------------------------------------------------------------------------
# 1.0      13.01.2025    CHOE                     Initiale Erstellung
# -----------------------------------------------------------------------------
# Hinweise:
# - Die Markierungen im PDF können über die globale Variable `apply_marking`
#   gesteuert werden. Wenn `apply_marking` auf `True` gesetzt ist, werden
#   die Weak-Words im PDF hervorgehoben.
# - Das Modul verarbeitet eine Seite nach der anderen, um große PDFs effizient
#   zu handhaben.
# - Alle zu prüfenden Dateien müssen im `data/input`-Ordner abgelegt werden.
# - Die markierten PDFs werden im `data/output`-Ordner gespeichert.
# -----------------------------------------------------------------------------

import fitz
import re
from collections import defaultdict
from modules.config import logger  # Logger importieren

def highlight_weak_words_in_pdf(input_file, weak_words_with_comments, apply_marking=True):
    """
    Markiert Weak-Words in einem PDF und zählt die Vorkommen.
    """
    logger.debug(f"Verarbeite PDF: {input_file}")
    
    try:
        # PDF-Dokument öffnen
        pdf_document = fitz.open(input_file)
    except Exception as e:
        logger.error(f"Fehler beim Öffnen der PDF-Datei '{input_file}': {e}")
        raise  # Fehler beim Öffnen der Datei weitergeben
    
    weak_word_counts = defaultdict(int)
    category_counts = defaultdict(int)

    try:
        # Durch jede Seite des PDF-Dokuments iterieren
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            text = page.get_text("text")

            for chapter, chapter_data in weak_words_with_comments.items():
                for weak_word, comment in chapter_data.items():
                    regex = re.compile(r'\b{}\b'.format(re.escape(weak_word)), re.IGNORECASE)
                    matches = list(regex.finditer(text))

                    for match in matches:
                        start_idx, end_idx = match.span()
                        if (start_idx == 0 or not text[start_idx - 1].isalnum()) and \
                           (end_idx == len(text) or not text[end_idx].isalnum()):
                            weak_word_counts[weak_word] += 1
                            category_counts[chapter] += 1
                            if apply_marking:
                                search_result = page.search_for(match.group(0))
                                for inst in search_result:
                                    try:
                                        highlight = page.add_highlight_annot(inst)
                                        highlight.update()
                                    except Exception as e:
                                        logger.error(f"Fehler beim Markieren von Weak-Word '{weak_word}' in Seite {page_number + 1}: {e}")
                                        continue  # Fehler beim Markieren nicht stoppen

    except Exception as e:
        logger.error(f"Fehler beim Verarbeiten des PDFs '{input_file}': {e}")
        pdf_document.close()
        raise  # Fehler beim Verarbeiten des Dokuments weitergeben

    # Ausgabedatei entsprechend dem Dateinamen und Modus speichern
    if apply_marking:
        try:
            output_file = input_file.replace("data/input", "data/output").replace(".pdf", "_weak_words_marked.pdf")
            pdf_document.save(output_file)
            logger.info(f"Weak-Words wurden markiert: {output_file}")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der markierten PDF '{output_file}': {e}")
            pdf_document.close()
            raise  # Fehler beim Speichern weitergeben

    pdf_document.close()
    return category_counts, weak_word_counts