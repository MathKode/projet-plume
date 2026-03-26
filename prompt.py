# ÉTAPE 1 : Analyser les annales et extraire les concepts requis
PROMPT_ETAPE_1 = """Tu es un expert pédagogique médical. Ton rôle est d'analyser des annales d'examen.

FICHIER FOURNI :
- annales.txt : contient les questions d'examen ET leurs corrections

TA MISSION :
Analyse chaque question des annales et identifie TOUS les concepts/connaissances médicales nécessaires pour y répondre correctement.

IMPORTANT :
- Ne te limite PAS aux mots exacts de la question
- Identifie les concepts IMPLICITES (ex: une question sur "l'ictère" nécessite de connaître le métabolisme de la bilirubine)
- Pour chaque concept, réfléchis : "Quelle connaissance du cours un étudiant DOIT maîtriser pour répondre ?"

FORMAT DE SORTIE :
Pour chaque question des annales, liste les concepts sous cette forme :

QUESTION N°[numéro] : [résumé court de la question]
Concepts requis :
- [Concept 1] : [pourquoi c'est nécessaire]
- [Concept 2] : [pourquoi c'est nécessaire]
- [Concept 3] : [pourquoi c'est nécessaire]

[ligne vide]

EXEMPLE :
QUESTION N°1 : Quelle est la cause principale de l'ictère néonatal ?
Concepts requis :
- Métabolisme de la bilirubine : comprendre le cycle bilirubine-albumine
- Immaturité hépatique du nouveau-né : expliquer pourquoi l'ictère est fréquent
- Bilirubine conjuguée vs non-conjuguée : différencier les types d'ictère
- Traitement par photothérapie : connaître la prise en charge

Analyse maintenant le fichier annales.txt.
"""


# ÉTAPE 2 : Localiser ces concepts dans le cours
PROMPT_ETAPE_2 = """Tu es un expert pédagogique. Tu vas maintenant localiser des concepts précis dans un cours.

FICHIERS FOURNIS :
- cours.txt : le ronéo/cours
- concepts.txt : liste des concepts à trouver (générée à l'étape précédente)

TA MISSION :
Pour CHAQUE concept listé dans concepts.txt, trouve dans cours.txt les passages EXACTS qui l'expliquent.

RÈGLES IMPORTANTES :
1. Un concept peut apparaître à PLUSIEURS endroits du cours → trouve-les TOUS
2. Cherche les SYNONYMES et REFORMULATIONS (ex: "lobe gauche" = "segment hépatique gauche")
3. Cherche les DÉFINITIONS, EXPLICATIONS et EXEMPLES du concept
4. Un passage peut couvrir PLUSIEURS concepts → note-le pour chacun
5. Si un concept n'est PAS dans le cours, écris "CONCEPT ABSENT"

FORMAT DE SORTIE :
Pour chaque concept, retourne les passages exacts du cours sous cette forme :

[CONCEPT] Métabolisme de la bilirubine
mot_avant [AN]passage exact du cours à surligner[/AN] mot_après
mot_avant [AN]autre passage du cours[/AN] mot_après

[CONCEPT] Bilirubine conjuguée vs non-conjuguée  
mot_avant [AN]passage exact[/AN] mot_après

[CONCEPT] Photothérapie
CONCEPT ABSENT

CONSIGNES TECHNIQUES :
- Les passages entre [AN] et [/AN] doivent être EXACTS (copiés-collés du cours.txt)
- Longueur idéale : 5 à 20 mots (une phrase clé ou une définition courte)
- Inclus toujours 1-2 mots avant et après pour le contexte
- Si un passage est trop long (>30 mots), découpe-le en plusieurs extraits plus courts

Analyse maintenant cours.txt avec la liste de concepts fournie.
"""


# VERSION ALTERNATIVE : PROMPT UNIQUE AMÉLIORÉ (si tu veux garder 1 seule étape)
PROMPT_UNIQUE_AMELIORE = """Tu es un expert pédagogique médical/scientifique/mathématique spécialisé dans l'analyse de correspondance cours-annales.

FICHIERS FOURNIS :
- annales.txt : questions d'examen avec leurs corrections
- cours.txt : ronéo de cours

TA MISSION EN 3 PHASES :

═══ PHASE 1 : COMPRÉHENSION DES ANNALES ═══
Analyse chaque question et identifie :
- Le concept principal testé
- Les connaissances implicites nécessaires
- Les pièges possibles (ex: une question sur un symptôme qui nécessite de connaître la physiopathologie)

═══ PHASE 2 : CARTOGRAPHIE DES CONCEPTS ═══
Pour chaque connaissance identifiée, cherche dans cours.txt :
- Les définitions exactes
- Les explications détaillées  
- Les exemples cliniques
- Les mécanismes physiopathologiques
- Les classifications/listes

ATTENTION : 
- Un même concept peut être expliqué à PLUSIEURS endroits → trouve-les TOUS
- Cherche les SYNONYMES (ex: "insuffisance cardiaque" = "défaillance cardiaque")
- Ne te limite PAS aux mots exacts des annales

═══ PHASE 3 : EXTRACTION PRÉCISE ═══
Pour chaque passage trouvé, extrais la phrase/notion clé sous ce format :
mot_avant [AN]passage_exact[/AN] mot_après

RÈGLES D'EXTRACTION :
✓ Passage entre 5 et 20 mots (ni trop court, ni trop long)
✓ Doit être auto-suffisant (compréhensible hors contexte)
✓ Copié-collé EXACT de cours.txt (respecte majuscules, accents, ponctuation)
✓ Si un paragraphe contient plusieurs notions importantes, fais plusieurs extraits

EXEMPLE DE SORTIE :

Question annale : "Citez 2 causes d'ictère à bilirubine non conjuguée"
→ Concept requis : Causes ictère bilirubine non conjuguée

Passages trouvés dans cours.txt :
hémolyse [AN]la destruction excessive des globules rouges libère de la bilirubine non conjuguée[/AN] que le foie
syndrome de [AN]Gilbert : déficit en UDP-glucuronosyltransférase[/AN] entraînant une

───────────────────────────────────────

Maintenant, analyse les fichiers et retourne UNIQUEMENT la liste finale des passages au format :
mot_avant [AN]passage[/AN] mot_après

(Un passage par ligne, sans numérotation, sans explication supplémentaire)
"""