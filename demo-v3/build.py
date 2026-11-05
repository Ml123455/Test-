#!/usr/bin/env python3
"""Génère les 4 pages de la démo (index, realisations, services, devis) avec en-tête/pied communs.
Lancer : python3 build.py  — icônes : Lucide (ISC), dossier icons/."""
import re, pathlib

ICO = pathlib.Path(__file__).parent / "icons"
TEL = "+33674438216"  # dans la démo, « Appeler » joint Marius ; sur le vrai site du client, ce serait son numéro


def ic(nom, cls="ico"):
    svg = (ICO / f"{nom}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{inner}</svg>'


NAV = [("index.html", "Accueil"), ("realisations.html", "Réalisations"), ("services.html", "Services &amp; prix"), ]


def page(fichier, titre, desc, corps):
    liens = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fichier else ""}>{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titre} — L'Atelier du Bois (démonstration)</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css"><script src="site.js" defer></script></head><body>
<div class="demo-bar"><div class="wrap"><span>Exemple de site pour artisan<span class="long"> : le vôtre aurait votre nom, vos photos, votre numéro.</span></span><a href="tel:{TEL}">Je veux le même site : 06 74 43 82 16</a></div></div>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="index.html"><span class="brand-mark">a.</span><span>L'Atelier du Bois<small>MENUISERIE · AGENCEMENT</small></span></a>
<button class="burger" aria-expanded="false" aria-controls="menu">{ic("menu")} Menu</button>
<nav class="menu" id="menu">{liens}<a class="btn btn-copper" href="devis.html">{ic("pencil-ruler")} Devis gratuit</a></nav>
</div></header>
<main>{corps}</main>
<footer class="site-footer"><div class="wrap"><span>L'Atelier du Bois est un nom de démonstration. Site conçu par <a href="https://lgmartisanat.com" style="text-decoration:underline">Marius Lagrue · LGM Artisanat</a>.</span><span>Icônes Lucide (licence ISC).</span></div></footer>
<div class="mobile-cta"><a class="btn btn-line" href="tel:{TEL}">{ic("phone")} Appeler</a><a class="btn btn-copper" href="devis.html">{ic("pencil-ruler")} Devis gratuit</a></div>
</body></html>"""


def band():
    return f"""<section class="band section"><div class="wrap band-in"><div><p class="eyebrow">Votre projet</p><h2>Parlons-en. <em style="color:#e6c98a">Devis gratuit sous 48 h.</em></h2><p>Dites-nous ce que vous voulez faire. On vous répond vite, avec un prix clair avant de commencer.</p></div>
<div class="cta-row"><a class="btn btn-light" href="devis.html">{ic("pencil-ruler")} Demander un devis</a><a class="btn btn-line" style="color:#fff;border-color:#fff" href="tel:{TEL}">{ic("phone")} Appeler</a></div></div></section>"""


SERVICES = [
    ("sofa", "Meubles sur mesure", "Table, bibliothèque, bureau, dressing : dessinés pour votre pièce, pas pour un catalogue.", "à partir de 350 € (exemple)"),
    ("door-open", "Agencement intérieur", "Escaliers, placards sous pente, cuisines, parquets : chaque mètre carré devient utile.", "à partir de 900 € (exemple)"),
    ("trees", "Bois en extérieur", "Terrasses, portails, pergolas : des essences et des assemblages faits pour durer dehors.", "à partir de 1 200 € (exemple)"),
]

index = f"""
<section class="wrap hero"><div>
<p class="eyebrow">Menuisier à votre service</p>
<h1>Des meubles faits <em>pour chez vous.</em></h1>
<p class="lead">Table, escalier, terrasse : on dessine, on fabrique et on pose. Vous recevez un devis clair sous 48 h, sans engagement.</p>
<div class="cta-row"><a class="btn btn-copper" href="devis.html">{ic("pencil-ruler")} Demander mon devis gratuit</a><a class="btn btn-line" href="tel:{TEL}">{ic("phone")} Appeler maintenant</a></div>
<div class="proofs"><span>{ic("clock")} Devis sous 48 h</span><span>{ic("shield-check")} Prix annoncé avant de commencer</span><span>{ic("map-pin")} Intervention dans votre secteur</span></div>
</div><figure class="hero-photo"><img src="img/atelier-travail.jpg" alt="Finition à la main d'un plateau en bois" fetchpriority="high"><figcaption>{ic("hammer")} Fabriqué à l'atelier, posé chez vous</figcaption></figure></section>

<section class="section"><div class="wrap"><div class="head"><div><p class="eyebrow">Ce qu'on fait</p><h2>Trois façons de <em>vous aider.</em></h2></div><p>Un besoin précis ou une simple idée : on commence par vous écouter, puis on vous propose une solution et un prix.</p></div>
<div class="cards">{"".join(f'<article class="card"><div class="ico-big">{ic(i)}</div><h3>{t}</h3><p>{d}</p><div class="price">{p}</div></article>' for i, t, d, p in SERVICES)}</div></div></section>

<section class="section" style="padding-top:0"><div class="wrap"><div class="head"><div><p class="eyebrow">Réalisations</p><h2>Du travail <em>qui se voit.</em></h2></div><a class="btn btn-line" href="realisations.html">Voir toutes les réalisations {ic("arrow-right")}</a></div>
<div class="gallery"><figure><img src="img/table-design.jpg" alt="Table en bois et acier" loading="lazy"><figcaption><b>La table qui rassemble</b>Mobilier</figcaption></figure>
<figure><img src="img/renovation-interieure.jpg" alt="Parquet posé contre un mur de pierre" loading="lazy"><figcaption><b>Le bois rejoint la pierre</b>Intérieur</figcaption></figure>
<figure><img src="img/portail-domaine.jpg" alt="Portail en bois" loading="lazy"><figcaption><b>Une entrée à sa mesure</b>Extérieur</figcaption></figure></div></div></section>

<section class="section" style="background:#ece6d8"><div class="wrap"><div class="head"><div><p class="eyebrow">Comment ça se passe</p><h2>Simple, <em>de A à Z.</em></h2></div><p>Vous savez toujours où on en est, et ce que ça coûte avant que le travail commence.</p></div>
<ol class="steps"><li>{ic("message-circle")}<h3>1. Vous nous écrivez</h3><p>Quelques lignes et une photo suffisent.</p></li><li>{ic("ruler")}<h3>2. On prend les mesures</h3><p>Sur place ou par photos, selon le projet.</p></li><li>{ic("pencil-ruler")}<h3>3. Devis détaillé</h3><p>Dessin, bois, finition, prix et délai, sous 48 h.</p></li><li>{ic("hammer")}<h3>4. Fabrication et pose</h3><p>On fabrique, on pose, on nettoie. Vous profitez.</p></li></ol></div></section>

<section class="section"><div class="wrap"><div class="head"><div><p class="eyebrow">Ils nous font confiance</p><h2>Ce que disent <em>les clients.</em></h2></div></div>
<div class="avis">{"".join(f'<blockquote><div class="stars">{ic("star")*5}</div>{t}<footer>{n}</footer></blockquote>' for t, n in [("« Devis reçu le lendemain, travail propre, posé à la date prévue. »", "Exemple d'avis · Claire, Chartres"), ("« Il a compris ce qu'on voulait dès la première photo. La table est parfaite. »", "Exemple d'avis · Thomas, Rambouillet"), ("« Le prix annoncé était le prix payé. Pas de mauvaise surprise. »", "Exemple d'avis · Sophie, Maintenon")])}</div>
<p class="note">Exemples de mise en page : sur votre vrai site, on affiche les vrais avis de vos clients.</p></div></section>
{band()}"""

REAL = [("table-design", "La table qui rassemble", "Mobilier"), ("renovation-interieure", "Le bois rejoint la pierre", "Intérieur"), ("portail-domaine", "Une entrée à sa mesure", "Extérieur"),
        ("atelier-travail", "Jusqu'à la dernière passe", "En atelier"), ("terrasse-bois", "Une pièce de plus, dehors", "Extérieur"), ("portail-artisanal", "Un passage qui a du caractère", "Extérieur")]
realisations = f"""
<section class="wrap page-title"><p class="eyebrow">Réalisations</p><h1>Le travail, <em>de près.</em></h1><p>Quelques projets pour vous donner des idées. Le vôtre sera dessiné pour votre espace.</p></section>
<section class="section"><div class="wrap"><div class="gallery">{"".join(f'<figure><img src="img/{f}.jpg" alt="{t}" loading="lazy"><figcaption><b>{t}</b>{k}</figcaption></figure>' for f, t, k in REAL)}</div>
<p class="note">Photos d'illustration pour cette démonstration.</p></div></section>{band()}"""

FAQ = [("Faut-il un plan précis pour demander un devis ?", "Non. Une idée et deux ou trois photos de la pièce suffisent. Le dessin vient ensuite."),
       ("Qu'est-ce qui fait varier le prix ?", "Le bois choisi, les dimensions, les assemblages, la finition et la pose. Le devis détaille tout pour que vous puissiez ajuster."),
       ("Combien de temps pour un meuble ?", "Comptez quelques semaines selon le projet. Le délai est écrit sur le devis avant que vous vous engagiez."),
       ("Intervenez-vous chez moi ?", "Oui, dans le secteur de l'atelier. Indiquez votre ville dans le formulaire et on vous confirme.")]
services = f"""
<section class="wrap page-title"><p class="eyebrow">Services &amp; prix</p><h1>Ce qu'on fait, <em>et ce que ça coûte.</em></h1><p>Des prix de départ pour vous repérer. Le prix exact est sur le devis, gratuit et sans engagement.</p></section>
<section class="section"><div class="wrap"><div class="cards">{"".join(f'<article class="card"><div class="ico-big">{ic(i)}</div><h3>{t}</h3><p>{d}</p><div class="price">{p}</div></article>' for i, t, d, p in SERVICES)}</div>
<p class="note">Prix d'exemple pour cette démonstration.</p></div></section>
<section class="section" style="padding-top:0"><div class="wrap split"><div><p class="eyebrow">Questions fréquentes</p><h2>Avant de <em>se lancer.</em></h2></div><div>{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div></div></section>{band()}"""

devis = f"""
<section class="wrap page-title"><p class="eyebrow">Devis gratuit</p><h1>Racontez-nous <em>votre projet.</em></h1><p>Trois lignes suffisent. Réponse sous 48 h, sans engagement.</p></section>
<section class="section"><div class="wrap split"><div>
<div class="contact-lines"><a href="tel:{TEL}">{ic("phone")} 06 74 43 82 16</a><a href="mailto:mariuslagrue@lgmartisanat.com">{ic("mail")} mariuslagrue@lgmartisanat.com</a><a href="https://wa.me/33674438216">{ic("message-circle")} WhatsApp</a><div>{ic("clock")} Réponse sous 48 h</div></div>
<p class="note" style="margin-top:28px">Dans cette démonstration, ces coordonnées sont celles de Marius, qui a conçu le site. Sur votre site, ce seraient les vôtres.</p></div>
<form id="devis" novalidate><label>Votre nom<input name="nom" autocomplete="name" required></label>
<label>Votre téléphone<input name="tel" type="tel" autocomplete="tel" required></label>
<label>Votre projet<select name="projet"><option>Un meuble</option><option>Un aménagement intérieur</option><option>Un extérieur en bois</option><option>Autre chose</option></select></label>
<label>Quelques mots (facultatif)<textarea name="msg" rows="4" placeholder="Dimensions, pièce, idée…"></textarea></label>
<button class="btn btn-copper" type="submit">{ic("pencil-ruler")} Recevoir mon devis</button>
<p class="note" style="margin:0">Démonstration : le formulaire ne s'envoie pas.</p><div id="merci" class="thanks" hidden>Merci ! Sur un vrai site, votre demande serait arrivée à l'artisan. Ici rien n'est envoyé.</div></form></div></section>"""

for f, t, d, c in [("index.html", "Menuisier sur mesure", "Meubles, agencements et extérieurs en bois sur mesure. Devis gratuit sous 48 h.", index),
                   ("realisations.html", "Réalisations", "Quelques réalisations de menuiserie sur mesure.", realisations),
                   ("services.html", "Services et prix", "Meubles, agencement, extérieur : services et prix de départ.", services),
                   ("devis.html", "Devis gratuit", "Demandez un devis gratuit, réponse sous 48 h.", devis)]:
    (pathlib.Path(__file__).parent / f).write_text(page(f, t, d, c))
print("4 pages générées")
