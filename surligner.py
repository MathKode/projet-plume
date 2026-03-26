from docx import Document
from copy import deepcopy
from docx.enum.text import WD_COLOR_INDEX

def __analyser_paragraph(paragraph, mot_ls):
    if True: #le if true c'est parceque j'ai copier coller le code en dehors de la boucle et j'avais la flemme d'enlever la tabulation
        #Phase de détection du mot dans tout le paragraphe
        txt = paragraph.text
        position_cible = [] # [ [début, fin] ]
        for mot in mot_ls:
            spliter = paragraph.text.lower().split(mot.lower())
            if len(spliter) > 1:
                spliter.pop()
                counter = 0
                for d in spliter:
                    position_cible.append([counter+len(d),counter+len(d)+len(mot)])
                    counter = counter + len(d) + len(mot)
        print(position_cible)
        #print(paragraph.text[position_cible[0][0]:position_cible[0][1]])
        for cible in position_cible:
            print(cible)
            i=0
            counter=0
            yellow = False
            result_run = []
            for run in paragraph.runs:
                txt = run.text
                print(f"RUN n° {i} {run.text}")

                #Extraction des lettres
                before = ""
                inside = ""
                after = ""
                for lettre in txt:
                    if counter < cible[0]:
                        before += lettre
                    elif counter >= cible[1]:
                        after += lettre
                    else:
                        inside += lettre
                    counter+=1
                #print(before)
                #print(inside)
                #print(after)
                
                if before != "":
                    new_run = deepcopy(run)
                    new_run.text = before
                    #new_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    result_run.append(new_run)
                if inside != "":
                    new_run = deepcopy(run)
                    new_run.text = inside
                    new_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    result_run.append(new_run)
                if after != "":
                    new_run = deepcopy(run)
                    new_run.text = after
                    #new_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    result_run.append(new_run)
                if before=="" and inside=="" and after=="":
                    print("Maybe une image")
                    result_run.append(deepcopy(run))
                i+=1

            # SUPPRIMER les anciens runs
            for run in paragraph.runs:
                paragraph._element.remove(run._element)

            # AJOUTER les nouveaux runs
            for new_run in result_run:
                paragraph._element.append(new_run._element)

def surligner_mots(doc, mot_ls):
    fichier = Document(doc)
    for paragraph in fichier.paragraphs:
        __analyser_paragraph(paragraph, mot_ls)

    for table in fichier.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    __analyser_paragraph(paragraph, mot_ls)

    fichier.save('./v3/result_test.docx')


#surligner_mots("./v3/test.docx",["surligner", "un test"])
#surligner_mots("./ressources/UE6-C8-L1-Oussalah.docx",["2/3 du volume", "lobe gauche", "division chirurgicale", "bilirubine"])