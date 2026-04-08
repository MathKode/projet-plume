Attribute VB_Name = "MacroPlume"
Sub plume()
    Dim texteOriginal As String
    Dim texteNettoyé As String
    Dim plumeNoir As String
    Dim plumeBase As String
    Dim rng As Word.Range
    Dim aDejaDesPlumes As Boolean
    
    ' Vérifie qu'il y a une sélection
    If Selection.Type = wdNoSelection Then
        MsgBox "Veuillez sélectionner du texte.", vbExclamation
        Exit Sub
    End If
    
    plumeBase = EmojiFromCode("1FAB6")
    plumeNoir = plumeBase & ChrW(&HFE0E)
    
    Set rng = Selection.Range
    
    ' 1. Étendre la sélection pour attraper les plumes existantes autour
    Set rng = EtendreSelectionAvecPlumes(rng, plumeBase, plumeNoir)
    
    ' 2. Nettoyer les espaces
    Set rng = NettoyerEspacesSelection(rng)
    
    ' 3. ANALYSE : On regarde si la sélection contient des plumes AVANT de les effacer
    texteOriginal = rng.Text
    If texteOriginal Like plumeNoir & "*" Or texteOriginal Like plumeBase & "*" Or _
       texteOriginal Like "*" & plumeNoir Or texteOriginal Like "*" & plumeBase Then
        aDejaDesPlumes = True
    Else
        aDejaDesPlumes = False
    End If
    
    ' 4. On prépare le texte propre (sans aucune plume)
    texteNettoyé = SupprimerToutesPlumes(texteOriginal, plumeBase)
    
    ' 5. ACTION
    If aDejaDesPlumes Then
        ' MODE SUPPRESSION : on remet le texte brut
        rng.Text = texteNettoyé
        rng.Font.Bold = False
        ' Optionnel : remettre la couleur automatique
        'rng.Font.ColorIndex = wdAuto
        rng.Font.Name = "Arial"
    Else
        ' MODE AJOUT : on encadre
        rng.Text = plumeNoir & texteNettoyé & plumeNoir
        rng.Font.Bold = True
        rng.Font.Color = RGB(0, 0, 0) ' Noir
        
        ' Forcer la police pour éviter les carrés ou la couleur (voir nos échanges précédents)
        ' On peut appliquer Segoe UI Emoji à toute la zone, le FE0E fera le travail de rendu noir
        ' rng.Font.Name = "Segoe UI Emoji"
    End If
    
    ' On replace la sélection sur le résultat
    rng.Select
End Sub

Function SupprimerToutesPlumes(texte As String, plumeBase As String) As String
    ' Supprime la version noire (FE0E), la version couleur forcée (FE0F) et la version de base
    texte = Replace(texte, plumeBase & ChrW(&HFE0E), "")
    texte = Replace(texte, plumeBase & ChrW(&HFE0F), "")
    texte = Replace(texte, plumeBase, "")
    SupprimerToutesPlumes = texte
End Function

Function EtendreSelectionAvecPlumes(rng As Word.Range, plumeBase As String, plumeNoir As String) As Word.Range
    Dim debut As Long
    Dim fin As Long
    Dim textGauche As String
    Dim textDroite As String
    
    debut = rng.Start
    fin = rng.End
    
    ' Vérifie la présence d'une plume (noire ou normale) à gauche
    If debut >= Len(plumeNoir) Then
        textGauche = ActiveDocument.Range(debut - Len(plumeNoir), debut).Text
        If textGauche = plumeNoir Then
            debut = debut - Len(plumeNoir)
        ElseIf ActiveDocument.Range(debut - Len(plumeBase), debut).Text = plumeBase Then
            debut = debut - Len(plumeBase)
        End If
    End If
    
    ' Vérifie la présence d'une plume (noire ou normale) à droite
    textDroite = ActiveDocument.Range(fin, fin + Len(plumeNoir)).Text
    If textDroite = plumeNoir Then
        fin = fin + Len(plumeNoir)
    ElseIf ActiveDocument.Range(fin, fin + Len(plumeBase)).Text = plumeBase Then
        fin = fin + Len(plumeBase)
    End If
    
    Set EtendreSelectionAvecPlumes = ActiveDocument.Range(debut, fin)
End Function

Function NettoyerEspacesSelection(rng As Word.Range) As Word.Range
    Dim debut As Long
    Dim fin As Long
    
    debut = rng.Start
    fin = rng.End
    
    ' Supprime espaces au début
    Do While debut < fin And Mid(ActiveDocument.Range(debut, debut + 1).Text, 1, 1) = " "
        debut = debut + 1
    Loop
    
    ' Supprime espaces à la fin
    Do While fin > debut And Mid(ActiveDocument.Range(fin - 1, fin).Text, 1, 1) = " "
        fin = fin - 1
    Loop
    
    Set NettoyerEspacesSelection = ActiveDocument.Range(debut, fin)
End Function

Function EmojiFromCode(codeHex As String) As String
    Dim codePoint As Long
    codePoint = CLng("&H" & codeHex)
    
    ' Si dans le BMP (cas simple)
    If codePoint < &H10000 Then
        EmojiFromCode = ChrW(codePoint)
    Else
        ' Conversion en surrogate pair
        codePoint = codePoint - &H10000
        
        Dim highSurrogate As Long
        Dim lowSurrogate As Long
        
        highSurrogate = &HD800 Or (codePoint \ &H400)
        lowSurrogate = &HDC00 Or (codePoint And &H3FF)
        
        EmojiFromCode = ChrW(highSurrogate) & ChrW(lowSurrogate)
    End If
End Function
