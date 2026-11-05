# Démo artisan v3 (multi-pages) — 05/11/2026

**Objectif** : site de démonstration montré aux artisans prospectés, pensé pour vendre : faire appeler / demander un devis. Remplace à terme `../demo/` (« L'Atelier », une seule page).

**État** : généré et testé en navigateur sans écran (PC 1440 px, téléphone 390 px : pas de débordement, pas d'erreur JS). **Pas encore en ligne** : en attente de validation de Marius.

**Fichiers** : `build.py` (génère index, realisations, services, devis — modifier le contenu ici puis `python3 build.py`), `site.css`, `site.js`, `img/` (photos copiées de `../demo/img`), `icons/` (icônes Lucide, licence ISC, `LICENSE-lucide.txt`).

**Décisions de Marius**
- Vrai site multi-pages, objectif n°1 = appel / devis.
- Haut de page grand sur PC (hero plein écran).
- Icônes : jeux open source (Lucide), jamais dessinées à la main.
- Aucun faux diplôme ni fausse ancienneté ; avis et prix étiquetés « exemple ».

**Choix à connaître** : dans la démo, « Appeler » et le formulaire affichent les coordonnées de Marius (le prospect qui clique le joint).

**Prochaine étape** : Marius regarde, puis mise en ligne (copier dans le dépôt, commit, push) et lien dans l'e-mail de prospection (`/data/prospection-28/README.md`).
