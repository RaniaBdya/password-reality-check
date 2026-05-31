# Password Reality Check

Site de sensibilisation à la sécurité des mots de passe.

## Accès

[raniabdya.github.io/password-reality-check](https://raniabdya.github.io/password-reality-check)

## Fonctionnalités

- Estimation du temps de cassage par force brute
- Vérification dans les bases de données de mots de passe volés (API Have I Been Pwned)
- Analyse des mauvaises habitudes (schémas courants, substitutions, répétitions)
- Générateur de mot de passe sécurisé (méthode des 4 mots)
- Section pédagogique sur le lien avec l'article 32 du RGPD

## Confidentialité

Le mot de passe ne quitte jamais le navigateur. Aucune donnée n'est collectée ni stockée.
Seuls les 5 premiers caractères du hash SHA-1 sont envoyés à l'API HIBP (k-anonymat).

## Stack

HTML · CSS · JavaScript · API Have I Been Pwned
