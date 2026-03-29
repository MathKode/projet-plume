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

#Nouveau prompt

PROMPT_UNIQUE_OKIII = """Tu es un expert pédagogique médical/scientifique/mathématique spécialisé dans l'analyse de correspondance annales-cours.

FICHIERS FOURNIS :
- annales.txt : questions d'examen avec leurs corrections
- cours.txt : ronéo de cours

TA MISSION EN 3 PHASES :

═══ PHASE 1 : COMPRÉHENSION DES ANNALES ═══
Analyse chaque question et identifie :
- Pour chaque item, pour chaque proposition A/B/C/D/E le concept principal testé
- Les connaissances implicites nécessaires
- Les pièges possibles (ex: une question sur un symptôme qui nécessite de connaître la physiopathologie)

═══ PHASE 2 : CARTOGRAPHIE DES CONCEPTS ═══
Pour chaque connaissance identifiée, cherche dans cours.txt :
- Les définitions exactes
- Les explications détaillées  
- Les exemples cliniques
- Les mécanismes physiopathologiques
- Les classifications/listes
- Il faut pour chaque notion abordé dans les annales que tu trouves 1 correspondance minimum dans la ronéo/cours

ATTENTION : 
- Un même concept peut être expliqué à PLUSIEURS endroits → trouve-les TOUS
- Cherche les SYNONYMES (ex: "insuffisance cardiaque" = "défaillance cardiaque")
- Ne te limite PAS aux mots exacts des annales

═══ PHASE 3 : EXTRACTION PRÉCISE ═══
Pour chaque passage trouvé, extrais la phrase/notion clé sous ce format :
mot_avant [AN]passage_exact[/AN] mot_après

RÈGLES D'EXTRACTION :
✓ Passage entre 2 et 10 mots (ni trop court, ni trop long)
✓ Doit être auto-suffisant (compréhensible hors contexte, PAS DE chiffre sans contexte/Pas de section de phrase incompréhensible)
✓ Copié-collé EXACT de cours.txt (respecte majuscules, accents, ponctuation)
✓ Si un paragraphe contient plusieurs notions importantes, fais plusieurs extraits et cible la principale

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


# PROMPT OPTIMISÉ - VERSION ANTI-BRUIT

PROMPT_V2_ANTI_BRUIT = """Tu es un expert pédagogique médical spécialisé dans l'analyse de correspondance annales-cours.

FICHIERS FOURNIS :
- annales.txt : questions d'examen avec leurs corrections
- cours.txt : ronéo de cours

═══════════════════════════════════════════════════════════
PHASE 1 : IDENTIFICATION DES CONCEPTS CLÉS
═══════════════════════════════════════════════════════════

Pour chaque question des annales, identifie :
- Les concepts **généraux** nécessaires pour répondre (pas les exemples spécifiques)
- Les définitions théoriques indispensables
- Les mécanismes fondamentaux

⚠️ EXCLUSIONS STRICTES :
- Ne retiens PAS les exemples illustratifs ("c'est la représentation de X")
- Ne retiens PAS les calculs numériques spécifiques ("pI = 6,1")
- Ne retiens PAS les cas particuliers ("l'acide glutamique a un pI = 3,25")

═══════════════════════════════════════════════════════════
PHASE 2 : RECHERCHE DANS LE COURS
═══════════════════════════════════════════════════════════

Pour chaque concept identifié, trouve dans cours.txt :
✓ Les DÉFINITIONS générales
✓ Les RÈGLES fondamentales
✓ Les MÉCANISMES explicatifs
✓ Les CLASSIFICATIONS importantes

✗ IGNORE :
✗ Les exemples chiffrés isolés
✗ Les références à des figures/schémas
✗ Les anecdotes ("quand on se mouille les cheveux...")

═══════════════════════════════════════════════════════════
PHASE 3 : EXTRACTION INTELLIGENTE
═══════════════════════════════════════════════════════════

RÈGLES D'OR POUR L'EXTRACTION :

1️⃣ LONGUEUR : 3 à 10 mots minimum
   → Assez long pour être compréhensible seul

2️⃣ AUTO-SUFFISANCE : Le passage doit pouvoir être lu HORS CONTEXTE
   ✓ Bon : "Les liaisons hydrogènes sont établies entre les résidus i et i+4"
   ✗ Mauvais : "entre les résidus i et i+4" (incomplet)
   ✗ Mauvais : "il a charge -1" (pronom sans antécédent)

3️⃣ COMPLÉTUDE GRAMMATICALE :
   ✓ Sujet + Verbe + Complément complet
   ✗ Pas de fragments de phrases
   ✗ Pas de pronoms isolés (il, elle, ce, cela...)

4️⃣ VALEUR PÉDAGOGIQUE :
   ✓ Définitions, règles, mécanismes
   ✗ Exemples numériques isolés
   ✗ Phrases de transition ("voyons maintenant...")

5️⃣ CONTEXTUALISATION :
   Si le passage contient un pronom (il, elle, cela...), inclus le nom auquel il se réfère.
   Exemple : 
   ✗ "il déstabilise l'hélice alpha" 
   ✓ "L'acide aspartique déstabilise l'hélice alpha"

═══════════════════════════════════════════════════════════
TESTS DE VALIDATION AVANT EXTRACTION
═══════════════════════════════════════════════════════════

Avant d'extraire un passage, vérifie TOUTES ces conditions :

□ Le passage fait au moins 3 mots ?
□ Il contient un verbe conjugué ?
□ Il est compréhensible SANS lire ce qui précède/suit ?
□ Il n'y a PAS de pronoms sans référent explicite ?
□ Ce n'est PAS un exemple chiffré isolé ?
□ Ce n'est PAS une référence à une figure/image ?
□ Cela exprime une RÈGLE ou DÉFINITION générale ?

Si l'une de ces conditions échoue → NE PAS EXTRAIRE

═══════════════════════════════════════════════════════════
FORMAT DE SORTIE
═══════════════════════════════════════════════════════════

Retourne UNIQUEMENT les passages validés au format :
mot_avant [AN]passage_exact[/AN] mot_après

EXEMPLES DE BONNES EXTRACTIONS :
-----------------------------------
cohésive grâce à [AN]des liaisons hydrogènes qui doivent être fournies par les atomes qui constituent la liaison peptidique[/AN] ce sont les

ramifié sur le [AN]carbone beta comme la valine et l'isoleucine ainsi que les acides aminés impliqués dans des liaisons hydrogène déstabilisent les hélices alpha[/AN] La valine

antiparallèles sont [AN]les plus stables car les atomes impliqués dans la formation des liaisons hydrogènes sont alignés[/AN] ce qui confère

EXEMPLES DE MAUVAISES EXTRACTIONS (À ÉVITER) :
----------------------------------------------
✗ représentation de [AN]la myoglobine[/AN] elle est
   → Référence à un exemple visuel, pas une connaissance

✗ pH = 5, [AN]il a charge -1[/AN] donc
   → Pronom "il" sans référent, incompréhensible seul

✗ extrémité [AN]C-terminale[/AN] de la protéine
   → Fragment trop court, sans contexte

✗ l'acide glutamique [AN]a un pI = 3,25[/AN] tandis que
   → Valeur numérique spécifique, pas une règle générale

═══════════════════════════════════════════════════════════
MAINTENANT, ANALYSE LES FICHIERS
═══════════════════════════════════════════════════════════

Applique rigoureusement ces règles et retourne UNIQUEMENT les passages validés.
"""


# PROMPT AVEC ÉTAPE DE RAISONNEMENT (pour forcer la réflexion)

PROMPT_V2_AVEC_RAISONNEMENT = """Tu es un expert pédagogique médical spécialisé dans l'analyse de correspondance annales-cours.

FICHIERS FOURNIS :
- annales.txt : questions d'examen avec leurs corrections
- cours.txt : ronéo de cours

═══════════════════════════════════════════════════════════
MÉTHODOLOGIE EN 2 ÉTAPES
═══════════════════════════════════════════════════════════

ÉTAPE 1 : ANALYSE ET RAISONNEMENT (visible dans ta réponse)
------------------------------------------------------------

Pour chaque question des annales, rédige une analyse structurée :

**Question N°X : [résumé]**

Concepts généraux requis :
- [Concept 1] : [pourquoi c'est une règle générale et non un exemple]
- [Concept 2] : [pourquoi c'est essentiel pour comprendre]

Passages trouvés dans le cours :
1. "[extrait candidat 1]"
   ✓ Validation : Auto-suffisant ? Oui/Non
   ✓ Contient une règle générale ? Oui/Non
   ✓ Longueur > 8 mots ? Oui/Non
   → DÉCISION : RETENU / REJETÉ

2. "[extrait candidat 2]"
   ✓ Validation : Auto-suffisant ? Oui/Non
   ...
   → DÉCISION : RETENU / REJETÉ

---

ÉTAPE 2 : SORTIE FINALE (après toutes les analyses)
----------------------------------------------------

Une fois toutes les questions analysées, retourne UNIQUEMENT les passages RETENUS :

[AN]passage_1[/AN]
[AN]passage_2[/AN]
[AN]passage_3[/AN]
...

═══════════════════════════════════════════════════════════
CRITÈRES DE VALIDATION (rappel)
═══════════════════════════════════════════════════════════

Un passage est RETENU si et seulement si :
✓ 3-10 mots
✓ Phrase complète (sujet + verbe + complément)
✓ Compréhensible HORS CONTEXTE
✓ Exprime une RÈGLE/DÉFINITION générale
✓ Pas de pronoms sans référent (il, elle, cela...)
✓ Pas d'exemple chiffré isolé
✓ Pas de référence à figure/schéma

Maintenant, analyse les fichiers.
"""



PROMPT_ORTHO_V1="""Tu es un expert de la langue française, ta mission est de relever les fautes d'orthographe et de sens dans le texte ci-joint et de m'indiquer où elles sont situées afin que je puisse les modifer. 

FICHIER SOURCE :
- ronéo_txt.txt : document texte à analyser pour la recherche de faute d'orthographe

MISSION :
Détecter les fautes d'orthographe/de sens et proposer une correction adaptée

RESULTAT :
Pour chaque fautes, je veux que les résultats soient présenté sous cette forme : [AN][B0]Phrase de base[/B0][B1]Extrait de la phrase avec correction[/B1][/AN]
Plus précisément, nous avons 3 balises
[AN][/AN] : permet d'indiquer une correction orthographique
[B0][/B0] : présente la phrase d'origine avec la faute
[B1][/B1] : présente la phrase corrigée

REGLES :
- Se fier EXACTEMENT au text de ronéo_txt.txt 
- Proposer une correction avec le passage normal puis celui corrigé
- Il faut que la correction et la phrase proposé soit les mêmes (sauf pour le mots corrigé)
- Phrase assez longue pour qu'on comprenne le contexte (au moins les accords entre les mots)
- Phrase assez longue mais pas trop non plus.
- Respecter les retours à la ligne, les séparations du tableaux (si il y a un séparateur = traiter les fautes comme 2 fautes distinctes)
- Pas de phrase d'introduction

EXEMPLE:
"J'aimes les pommes" -> [AN][B0]J'aimes les pommes[/B0][B1]J'aime les pommes[/B1][/AN]
"Le glycogène est une molécule très intéressante a étudié en physiologie" -> [AN][B0]une molécule très intéressante a étudié en physiologie[/B0][B1]une molécule très intéressante à étudier en physiologie[/B1][/AN]
"""