# Password Reality Check

Site de sensibilisation à la sécurité des mots de passe.

## Accès
[raniabdya.github.io/password-reality-check](https://raniabdya.github.io/password-reality-check)

## Fonctionnalités
- Estimation du temps de cassage par force brute (hypothèse : mot de passe tiré au hasard, 10 milliards d'essais par seconde)
- Vérification dans les bases de mots de passe volés (API Have I Been Pwned)
- Repérage de mauvaises habitudes : mots de passe courants, substitutions de caractères (@ pour a, 0 pour o...), caractères répétés, schéma « mot + chiffres », mot de passe trop court
- Générateur de mot de passe par tirage de 6 mots (démonstration de la méthode)
- Section pédagogique sur le lien avec l'article 32 du RGPD

## Confidentialité
Le mot de passe saisi reste dans le navigateur. Pour la vérification des fuites, seuls les 5 premiers caractères de son empreinte SHA-1 sont envoyés à l'API Have I Been Pwned (principe du k-anonymat), ce qui ne permet pas de retrouver le mot de passe. Ce site ne stocke aucune donnée.

## Limites
- Outil pédagogique : il ne remplace pas un gestionnaire de mots de passe. 
- L'estimation du temps de cassage ne tient pas compte des attaques par dictionnaire.
- Le générateur utilise une liste de 200 mots (environ 46 bits de sécurité), ce qui illustre la méthode mais reste insuffisant pour un usage réel. Une version utilisable demanderait une liste de plusieurs milliers de mots.

## Stack
HTML · CSS · JavaScript · API Have I Been Pwned
