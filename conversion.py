from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn


def __has_it_image(paragraph):
    #Vérifie si le paragraphe contient une image
    for run in paragraph.runs:
        # Vérifier les éléments graphiques (drawing) dans le run
        if run.element.findall(qn('w:drawing')):
            return True
        # Vérifier les images inline (ancienne méthode)
        if run.element.findall(qn('pic:pic')):
            return True
    return False

def __has_it_equation(paragraph):
    #renvoie une liste [True/False , 'equation']
    element = paragraph._element
    if element.findall(qn('m:oMath')) or element.findall(qn('m:oMathPara')):
        print('EQUATION')
        #print(element.xml)
        #A coder
        


def docx_to_structured_txt(source_path, result_path):
    """
    Convertit un fichier Word en txt en PRÉSERVANT la structure hiérarchique.
    Amélioration : ajoute des marqueurs pour les titres, listes, tableaux.
    """
    doc = Document(source_path)
    output_lines = []
    
    # Parcourir tous les éléments du body dans l'ordre
    for element in doc.element.body:
        # Si c'est un paragraphe
        if element.tag.endswith('p'):
            paragraph = Paragraph(element, doc)
            text = paragraph.text.strip()
            if not text:
                # RECHERCHE IMAGE
                find_image=__has_it_image(paragraph)
                if find_image:
                    print("IMAGE")
                    output_lines.append("[IMAGE]")
                else:
                    print(paragraph)
                #RECHERCHE EQUATION
                __has_it_equation(paragraph)
                
                continue
                
            # Détecte le type de paragraphe
            style_name = paragraph.style.name.lower()
            
            # Titres de niveau 1
            if 'heading 1' in style_name or 'titre 1' in style_name:
                output_lines.append(f"\n{'='*60}")
                output_lines.append(f"# {text}")
                output_lines.append(f"{'='*60}\n")
            
            # Titres de niveau 2
            elif 'heading 2' in style_name or 'titre 2' in style_name:
                output_lines.append(f"\n## {text}")
                output_lines.append(f"{'-'*40}\n")
            
            # Titres de niveau 3
            elif 'heading 3' in style_name or 'titre 3' in style_name:
                output_lines.append(f"\n### {text}\n")
            
            elif 'heading 4' in style_name or 'titre 4' in style_name:
                output_lines.append(f"\n#### {text}\n")
            
            # Listes à puces
            elif paragraph.style.name.startswith('List'):
                output_lines.append(f"  • {text}")
            
            # Paragraphe normal
            else:
                output_lines.append(text)
        
        # Si c'est un tableau
        elif element.tag.endswith('tbl'):
            table = Table(element, doc)
            output_lines.append("\n[TABLEAU]")
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    cell_text = []
                    for paragraph in cell.paragraphs:
                        txt = paragraph.text.strip()
                        if txt != "":
                            cell_text.append(txt)
                        else:
                            if __has_it_image(paragraph):
                                print("IMG dans le tableau")
                                cell_text.append('[IMAGE]')
                    if len(cell_text) != 0:
                        row_data.append(" [NEXT LINE] ".join(cell_text))
                if row_data:
                    output_lines.append(" | ".join(row_data))
            output_lines.append("[/TABLEAU]\n")
    
    # Écrire le fichier
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return result_path

   


def pdf_to_structured_txt(source_path, result_path, mode):
    """
    Convertit un PDF en txt en essayant de détecter la structure.
    mode :
     1 = classique, on garde tous les contenus
     2 = Enoncées uniquement
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

            if mode == 1:
                output_lines.append(line)
            elif mode == 2:
                # Critère page de correction :
                # Si il y a écrit "correction :" alors on ajoute la ligne
                if len(text.split('Correction :')) == 0:
                    output_lines.append(line)

    # Écrire le fichier
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return result_path

#docx_to_structured_txt("./ressources/UE6-C8-L1-Oussalah.docx","./v3/test_structured.txt")
#pdf_to_structured_txt("./ressources/annales_2.pdf","./v3/pdf_test.txt")