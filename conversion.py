from docx import Document
from docx.enum.style import WD_STYLE_TYPE

def docx_to_structured_txt(source_path, result_path):
    """
    Convertit un fichier Word en txt en PRÉSERVANT la structure hiérarchique.
    Amélioration : ajoute des marqueurs pour les titres, listes, tableaux.
    """
    doc = Document(source_path)
    output_lines = []
    
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
            
        # Détecte le type de paragraphe
        style_name = paragraph.style.name.lower()
        
        # Titres de niveau 1 (ex: "I. Introduction")
        if 'heading 1' in style_name or 'titre 1' in style_name:
            output_lines.append(f"\n{'='*60}")
            output_lines.append(f"# {text}")
            output_lines.append(f"{'='*60}\n")
        
        # Titres de niveau 2 (ex: "A. Anatomie")
        elif 'heading 2' in style_name or 'titre 2' in style_name:
            output_lines.append(f"\n## {text}")
            output_lines.append(f"{'-'*40}\n")
        
        # Titres de niveau 3
        elif 'heading 3' in style_name or 'titre 3' in style_name:
            output_lines.append(f"\n### {text}\n")
        
        # Listes à puces
        elif paragraph.style.name.startswith('List'):
            output_lines.append(f"  • {text}")
        
        # Paragraphe normal
        else:
            output_lines.append(text)
    
    # Traiter les tableaux
    for table in doc.tables:
        output_lines.append("\n[TABLEAU]")
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text:
                    row_data.append(cell_text)
            if row_data:
                output_lines.append(" | ".join(row_data))
        output_lines.append("[/TABLEAU]\n")
    
    # Écrire le fichier
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return result_path


def pdf_to_structured_txt(source_path, result_path):
    """
    Convertit un PDF en txt en essayant de détecter la structure.
    """
    import pymupdf
    
    doc = pymupdf.open(source_path)
    output_lines = []
    
    for page_num, page in enumerate(doc, start=1):
        # Ajouter un marqueur de page
        output_lines.append(f"\n{'─'*60}")
        output_lines.append(f"PAGE {page_num}")
        output_lines.append(f"{'─'*60}\n")
        
        # Extraire le texte
        text = page.get_text()
        
        # Détecter les questions (souvent commencent par Q, Question, numéro, etc.)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Détecter les questions
            if any(line.startswith(prefix) for prefix in ['Q', 'Question', '1.', '2.', 'QCM']):
                output_lines.append(f"\n[QUESTION] {line}")
            # Détecter les réponses/corrections
            elif any(marker in line.lower() for marker in ['réponse', 'correction', 'bonne réponse']):
                output_lines.append(f"[RÉPONSE] {line}")
            # Texte normal
            else:
                output_lines.append(line)
    
    # Écrire le fichier
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return result_path