#!/usr/bin/env python3
"""
BotArmory — Générateur de 17 démos métiers
Prend le template _TEMPLATE.html + données spécifiques par métier, génère tous les fichiers.
"""
import os
import re

TEMPLATE = open('/data/botarmory-site/demo/_TEMPLATE.html').read()

# Données par métier
METIERS = {
    "plombier": {
        "marque": "Dépannage Express Yvelines",
        "tagline": "Plomberie & Chauffage 78",
        "titre_page": "Dépannage Express Yvelines | Plombier 78",
        "description": "Plombier urgence Yvelines. Dépannage 24h/24, fuite d'eau, chauffe-eau, débouchage. Intervention rapide Bonnelles, Rambouillet, Chevreuse.",
        "badge": "🚨 Urgence 24h/24",
        "titre_hero": "Plombier <em>en urgence</em> à Yvelines ?<br>On arrive en <em>30 minutes</em>.",
        "sous_titre": "Fuite d'eau, chauffe-eau en panne, canalisation bouchée ? Nos plombiers interviennent 24h/24, 7j/7 sur tout le 78.",
        "cta_principal": "Appel d'urgence",
        "wa_message": "Urgence plomberie, besoin d'une intervention rapide",
        "zone": "Yvelines (78)",
        "annee": "2015",
        "hero_img": "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=1200&h=800&fit=crop",
        "lead_services": "Tous vos problèmes de plomberie, dépannage et installation, en urgence ou sur RDV.",
        "services": [
            ("🔧", "Dépannage fuite d'eau", "Recherche de fuite, réparation immédiate, devis transparent avant travaux."),
            ("🚿", "Débouchage canalisation", "WC, évier, douche, baignoire. Hydrocurage haute pression si besoin."),
            ("🔥", "Chauffe-eau & chaudière", "Installation, remplacement, entretien. Toutes marques (Atlantic, Thermor, Saunier Duval)."),
            ("🏠", "Installation sanitaire", "Salle de bain, cuisine, WC suspendu. Conseils personnalisés."),
            ("🔍", "Recherche de fuite", "Caméra thermique, gaz traceur, inspection vidéo. Localisation précise sans casse."),
            ("⚙️", "Contrat d'entretien", "Chaudière, chauffe-eau, adoucisseur. Visite annuelle + dépannage prioritaire."),
        ],
        "lead_realisations": "Quelques interventions récentes dans le 78.",
        "gallery": [
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1565193298357-c5b46b0ff7d4?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.9",
        "nb_avis": "127",
        "testimonials": [
            ("Intervention en 20 min un dimanche soir pour une fuite. Pro, rapide, tarif annoncé respecté. Je recommande.", "Marie L.", "Bonnelles"),
            ("Chauffe-eau remplacé en 2h. Très bon conseil sur le modèle. Prix correct.", "Jean-Marc D.", "Chevreuse"),
        ],
        "tarifs": [
            ("Déplacement + diagnostic", "49€", "Inclus si intervention"),
            ("Main d'œuvre plombier", "55€/h", "Tarif jour 8h-19h"),
            ("Urgence nuit/WE", "120€/h", "Majoration 22h-8h et dimanches"),
            ("Recherche de fuite", "À partir de 180€", "Selon complexité"),
        ],
        "cta_titre": "Une urgence ? Appelez maintenant.",
        "cta_texte": "On intervient 24h/24 sur tout le département des Yvelines. Appel gratuit, devis immédiat.",
        "cta_bouton": "06 XX XX XX XX",
    },
    "electricien": {
        "marque": "Dépannage Élec 78",
        "tagline": "Électricien urgence 78",
        "titre_page": "Dépannage Élec 78 | Électricien urgence Yvelines",
        "description": "Électricien urgence Yvelines 24h/24. Panne de courant, court-circuit, mise aux normes. Intervention rapide 78, 91, 28.",
        "badge": "⚡ Urgence 24h/24",
        "titre_hero": "Panne de courant ?<br><em>Électricien</em> en 30 min.",
        "sous_titre": "Court-circuit, disjoncteur qui saute, panne totale. On diagnostique et on répare, 24h/24 sur les Yvelines.",
        "cta_principal": "Appel d'urgence",
        "wa_message": "Urgence électricité, besoin d'un dépannage",
        "zone": "Yvelines (78) + Essonne (91)",
        "annee": "2012",
        "hero_img": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=1200&h=800&fit=crop",
        "lead_services": "Du dépannage d'urgence à l'installation complète, on couvre tous vos besoins électriques.",
        "services": [
            ("⚡", "Dépannage panne courant", "Recherche de panne, diagnostic, remise en service rapide."),
            ("🔌", "Court-circuit & disjoncteur", "Identification du défaut, remplacement tableau si nécessaire."),
            ("🏠", "Mise aux normes NF C 15-100", "Diagnostic complet, mise en conformité, attestation Consuel."),
            ("💡", "Installation éclairage", "LED, spots, lustres, éclairage extérieur. Conseils design + économies d'énergie."),
            ("🔋", "Borne de recharge VE", "Installation borne voiture électrique. Devis personnalisé selon votre installation."),
            ("🏢", "Électricité tertiaire", "Bureaux, commerces, restaurants. Tableau, prises, éclairage professionnel."),
        ],
        "lead_realisations": "Quelques chantiers récents.",
        "gallery": [
            "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1565609590160-7dd1eb7b5b89?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.8",
        "nb_avis": "94",
        "testimonials": [
            ("Panne un samedi soir, intervention en 40 minutes. Très pro, tarifs OK.", "Philippe R.", "Rambouillet"),
            ("Tableau électrique entièrement refait, maison rénovée. Travail soigné, délais respectés.", "Sophie M.", "Dourdan"),
        ],
        "tarifs": [
            ("Déplacement", "45€", "Déduit si intervention"),
            ("Main d'œuvre", "60€/h", "Tarif jour"),
            ("Urgence nuit/WE", "130€/h", "22h-8h et dimanches"),
            ("Diagnostic complet", "120€", "Avec rapport écrit"),
        ],
        "cta_titre": "Une panne électrique ?",
        "cta_texte": "Appelez maintenant, intervention rapide sur tout le 78. Devis gratuit par téléphone.",
        "cta_bouton": "06 XX XX XX XX",
    },
    "couvreur": {
        "marque": "Toiture 78",
        "tagline": "Couvreur Zingueur Yvelines",
        "titre_page": "Toiture 78 | Couvreur Zingueur Yvelines",
        "description": "Couvreur zingueur Yvelines. Réparation toiture, fuite, démoussage, gouttières. Devis gratuit.",
        "badge": "🏠 Toiture & Zinguerie",
        "titre_hero": "Fuite de toiture ?<br>Couvreur <em>en urgence</em>.",
        "sous_titre": "Tuiles cassées, infiltration, démoussage. On sécurise votre toit et on répare durablement.",
        "cta_principal": "Appel d'urgence",
        "wa_message": "Besoin d'un couvreur en urgence",
        "zone": "Yvelines (78) et environs",
        "annee": "2008",
        "hero_img": "https://images.unsplash.com/photo-1632935190508-b1c95c9da1a7?w=1200&h=800&fit=crop",
        "lead_services": "Tous travaux de toiture, zinguerie, isolation et charpente.",
        "services": [
            ("🏠", "Réparation toiture", "Tuiles cassées, faîtage, ardoises. Recherche de fuite et étanchéité."),
            ("💧", "Démoussage & nettoyage", "Démoussage toiture, traitement hydrofuge, nettoyage gouttières."),
            ("🌧️", "Gouttières & zinguerie", "Pose, réparation, remplacement gouttières zinc/PVC/aluminium."),
            ("🏗️", "Réfection complète", "Dépose ancienne couverture, pose neuve. Devis détaillé gratuit."),
            ("❄️", "Isolation combles", "Isolation par l'intérieur ou extérieur. Crédit d'impôt possible."),
            ("🔍", "Diagnostic toiture", "Inspection caméra, rapport complet, devis assurance si sinistre."),
        ],
        "lead_realisations": "Quelques chantiers récents dans le 78.",
        "gallery": [
            "https://images.unsplash.com/photo-1632935190508-b1c95c9da1a7?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1488972685288-c3fd157d7c7a?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1604769168710-a56debb6c3c4?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.7",
        "nb_avis": "68",
        "testimonials": [
            ("Réparation rapide après tempête. Couvreur réactif et sérieux.", "Christophe B.", "Houdan"),
            ("Réfection complète de notre toit, 2 semaines de travaux. Résultat parfait.", "Famille L.", "Montfort-l'Amaury"),
        ],
        "tarifs": [
            ("Diagnostic fuite", "95€", "Avec rapport photo"),
            ("Réparation tuiles", "À partir de 180€", "Selon accès"),
            ("Démoussage", "À partir de 15€/m²", "Toiture moyenne 100m² = 1500€"),
            ("Réfection complète", "Sur devis", "Gratuit"),
        ],
        "cta_titre": "Fuite de toit ?",
        "cta_texte": "Intervention rapide pour sécuriser votre habitation. Diagnostic et devis gratuits.",
        "cta_bouton": "06 XX XX XX XX",
    },
    "macon": {
        "marque": "Maçonnerie 78",
        "tagline": "Maçon traditionnel Yvelines",
        "titre_page": "Maçonnerie 78 | Maçon Yvelines",
        "description": "Maçon traditionnel Yvelines. Extension, rénovation, mur, terrasse, dallage. Devis gratuit.",
        "badge": "🧱 Maçonnerie pro",
        "titre_hero": "Votre projet de <em>maçonnerie</em><br>entre des mains expertes.",
        "sous_titre": "Extension de maison, rénovation, mur de clôture, terrasse, dallage. Du gros œuvre aux finitions.",
        "cta_principal": "Demander un devis",
        "wa_message": "Demande de devis maçonnerie",
        "zone": "Yvelines (78) + Essonne (91)",
        "annee": "2010",
        "hero_img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200&h=800&fit=crop",
        "lead_services": "Construction, rénovation, extension, aménagement extérieur.",
        "services": [
            ("🏠", "Extension de maison", "Surélévation, extension latérale, véranda. Permis de construire géré."),
            ("🧱", "Mur & clôture", "Mur de clôture, muret, pilier, portail. Parpaing, pierre, brique."),
            ("🌳", "Terrasse & dallage", "Terrasse béton, pierre naturelle, pavés. Préparation terrain + revêtement."),
            ("🏗️", "Gros œuvre", "Fondations, soubassement, élévation murs. Normes DTU et BAEL."),
            ("🚿", "Dalle béton", "Dalle garage, dalle terrasse, chape. Dosage 350kg/m³ garanti."),
            ("🔨", "Petite maçonnerie", "Rejointoiement, réparation fissure, ouverture de mur."),
        ],
        "lead_realisations": "Quelques chantiers récents.",
        "gallery": [
            "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1488972685288-c3fd157d7c7a?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1604769168710-a56debb6c3c4?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1565193298357-c5b46b0ff7d4?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.8",
        "nb_avis": "82",
        "testimonials": [
            ("Extension de 25m² réalisée en 2 mois. Excellent travail, prix respecté.", "Famille D.", "Chevreuse"),
            ("Mur de clôture en pierre, rendu magnifique. Artisan passionné.", "Thierry P.", "Limours"),
        ],
        "tarifs": [
            ("Extension plain-pied", "À partir de 1800€/m²", "Hors finitions"),
            ("Mur parpaing", "À partir de 120€/m²", "Fourni + posé"),
            ("Dalle béton", "À partir de 80€/m²", "Dosage standard"),
            ("Terrasse pierre", "À partir de 150€/m²", "Selon pierre"),
        ],
        "cta_titre": "Un projet de maçonnerie ?",
        "cta_texte": "Devis détaillé et gratuit sous 48h. On se déplace pour évaluer le chantier.",
        "cta_bouton": "Demander un devis",
    },
    "serrurier": {
        "marque": "Serrurerie 78",
        "tagline": "Serrurier & Métallier Yvelines",
        "titre_page": "Serrurerie 78 | Serrurier Yvelines urgence",
        "description": "Serrurier urgence Yvelines 24h/24. Ouverture de porte, changement serrure, blindage. Intervention rapide.",
        "badge": "🔐 Urgence 24h/24",
        "titre_hero": "Porte claquée ?<br>Serrurier en <em>20 minutes</em>.",
        "sous_titre": "Ouverture de porte sans casse, changement de serrure, blindage, dépannage urgent 24h/24.",
        "cta_principal": "Appel d'urgence",
        "wa_message": "Serrurier en urgence, besoin d'ouverture porte",
        "zone": "Yvelines (78) + Paris Ouest",
        "annee": "2014",
        "hero_img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&h=800&fit=crop",
        "lead_services": "Dépannage d'urgence et installation sécurité.",
        "services": [
            ("🔓", "Ouverture de porte", "Sans destruction. Toutes serrures, tous types de portes."),
            ("🔑", "Changement serrure", "Serrure classique, multipoints, A2P. Vachette, Bricard, Fichet."),
            ("🛡️", "Blindage de porte", "Porte blindée, cornières anti-effraction. Certification A2P possible."),
            ("🏠", "Installation complète", "Serrures, verrous, targettes, ferme-portes. Neuf et rénovation."),
            ("🔒", "Coffre-fort", "Pose, dépannage, combinaison oubliée. Particuliers et pros."),
            ("🚪", "Motorisation portail", "Portail coulissant, battant. Motorisation Somfy, Came, Nice."),
        ],
        "lead_realisations": "Quelques interventions récentes.",
        "gallery": [
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1565193298357-c5b46b0ff7d4?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.9",
        "nb_avis": "156",
        "testimonials": [
            ("Porte claquée à 23h, ouverture en 15 min sans casse. Merci !", "Sandrine L.", "Bonnelles"),
            ("Serrure 3 points installée, devis respecté. Pro.", "Marc T.", "Rambouillet"),
        ],
        "tarifs": [
            ("Ouverture porte", "À partir de 89€", "Jour 8h-19h"),
            ("Urgence nuit/WE", "À partir de 180€", "22h-8h et dimanches"),
            ("Changement serrure", "À partir de 120€", "Hors serrure"),
            ("Blindage porte", "À partir de 1500€", "Selon modèle"),
        ],
        "cta_titre": "Porte claquée ou serrure cassée ?",
        "cta_texte": "Intervention 24h/24 sur les Yvelines. Ouverture sans casse, devis avant travaux.",
        "cta_bouton": "06 XX XX XX XX",
    },
    "tatoueur": {
        "marque": "Ink Studio Versailles",
        "tagline": "Tattoo & Piercing 78",
        "titre_page": "Ink Studio Versailles | Tatoueur 78",
        "description": "Studio de tatouage à Versailles. Tatoueur pro, hygiène irréprochable, tous styles. RDV en ligne.",
        "badge": "🎨 Studio créatif",
        "titre_hero": "Votre tattoo <em>de rêve</em>,<br>par des artistes passionnés.",
        "sous_titre": "Studio privé à Versailles. Tatouage custom, lettrage, réalisme, japonais, old school. Hygiène 100% stérile.",
        "cta_principal": "Prendre RDV",
        "wa_message": "Demande de RDV tatouage",
        "zone": "Versailles + Yvelines",
        "annee": "2018",
        "hero_img": "https://images.unsplash.com/photo-1611501275019-9b5cda994e8d?w=1200&h=800&fit=crop",
        "lead_services": "Tatouage sur-mesure, piercing, retouche de vieux tatouages.",
        "services": [
            ("🎨", "Tattoo custom", "Pièce unique dessinée pour vous. Consultation gratuite avant le projet."),
            ("✒️", "Lettrage & calligraphie", "Noms, citations, lettrage old school. Polices classiques ou custom."),
            ("🌸", "Japonais traditionnel", "Dragons, carpes koï, vagues. Style Irezumi authentique."),
            ("💀", "Réalisme", "Portraits, animaux, nature. Technique hyperréaliste noir & gris ou couleur."),
            ("💎", "Piercing", "Oreilles, nez, nombril, microdermal. Bijoux titane médical, ASTM F-136."),
            ("🔧", "Cover & retouche", "Cover de vieux tatouages, rafraîchissement couleurs, retouches gratuites."),
        ],
        "lead_realisations": "Quelques réalisations récentes.",
        "gallery": [
            "https://images.unsplash.com/photo-1611501275019-9b5cda994e8d?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1565058379802-bbe93b2f703a?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1542856391-010fb87dcfed?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1590246814883-57c511e76cc4?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.9",
        "nb_avis": "203",
        "testimonials": [
            ("Mon premier tattoo, j'avais peur. Mise en confiance impeccable. Résultat sublime.", "Léa M.", "Versailles"),
            ("Cover d'un vieux tattoo raté, on ne voit plus rien. Bravo l'artiste.", "Karim B.", "78"),
        ],
        "tarifs": [
            ("Consultation", "Gratuite", "30 min en studio"),
            ("Tatouage petite pièce", "À partir de 80€", "5-10 cm"),
            ("Tatouage moyen", "À partir de 200€", "10-20 cm"),
            ("Pièce complète", "Sur devis", "Plusieurs séances possibles"),
        ],
        "cta_titre": "Prêt pour votre prochain tattoo ?",
        "cta_texte": "Consultation gratuite, devis sous 24h. Premier rendez-vous sous 2 semaines.",
        "cta_bouton": "Prendre RDV",
    },
    "fleuriste": {
        "marque": "Atelier Floral Chartres",
        "tagline": "Fleuriste & Compositions sur-mesure",
        "titre_page": "Atelier Floral Chartres | Fleuriste 28",
        "description": "Fleuriste à Chartres. Bouquets sur-mesure, mariage, deuil, livraison. Compositions fraîches et de saison.",
        "badge": "🌸 Fleurs fraîches",
        "titre_hero": "Des <em>compositions</em> florales<br>qui racontent une histoire.",
        "sous_titre": "Bouquets sur-mesure, mariage, deuil, événementiel. Fleurs locales et de saison, livrées à Chartres et environs.",
        "cta_principal": "Commander",
        "wa_message": "Commande de fleurs",
        "zone": "Chartres (28) + Eure-et-Loir",
        "annee": "2019",
        "hero_img": "https://images.unsplash.com/photo-1487530811176-3780de880c2d?w=1200&h=800&fit=crop",
        "lead_services": "Compositions florales pour tous les moments de la vie.",
        "services": [
            ("💐", "Bouquets sur-mesure", "Compositions personnalisées selon vos goûts, votre budget, la saison."),
            ("💒", "Mariage", "Bouquet mariée, boutonnière, centre de table, arche florale. Devis sur RDV."),
            ("🕊️", "Deuil & condoléances", "Couronnes, gerbes, compositions discrètes. Livraison directe au funérarium."),
            ("🎂", "Anniversaire & événements", "Compositions joyeuses, livraison surprise, abonnement mensuel fleurs."),
            ("🏢", "Décoration pro", "Hôtels, restaurants, bureaux. Contrat mensuel ou événement ponctuel."),
            ("🌿", "Plantes & cache-pots", "Plantes vertes, succulentes, cache-pots design. Conseils d'entretien."),
        ],
        "lead_realisations": "Quelques créations récentes.",
        "gallery": [
            "https://images.unsplash.com/photo-1487530811176-3780de880c2d?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1561181286-d3fee7d55364?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1469259943454-aa100abba749?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1502977249166-824b3a8a4d54?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.9",
        "nb_avis": "187",
        "testimonials": [
            ("Bouquet de mariage sublime, exactement ce que je voulais. À l'écoute, talentueux.", "Camille & Antoine", "Chartres"),
            ("Livraison au funérarium en 2h, composition parfaite dans ces moments difficiles.", "Famille L.", "Dreux"),
        ],
        "tarifs": [
            ("Petit bouquet", "À partir de 25€", "5-10 tiges"),
            ("Bouquet moyen", "À partir de 45€", "15-25 tiges"),
            ("Composition mariage", "Sur devis", "À partir de 250€"),
            ("Abonnement mensuel", "À partir de 35€/semaine", "Fleurs livrées chaque semaine"),
        ],
        "cta_titre": "Une envie de fleurs ?",
        "cta_texte": "Commandez avant 14h pour une livraison le jour même à Chartres et environs.",
        "cta_bouton": "Commander maintenant",
    },
    "coiffeur": {
        "marque": "Barbier 78",
        "tagline": "Salon de coiffure homme",
        "titre_page": "Barbier 78 | Coiffeur homme Yvelines",
        "description": "Salon de coiffure homme à Bonnelles. Coupe, barbe, styling. Ambiance barbier moderne.",
        "badge": "✂️ Barbier moderne",
        "titre_hero": "Le barbier <em>authentique</em><br>au cœur des Yvelines.",
        "sous_titre": "Coupe homme, taille de barbe, soins capillaires. Ambiance conviviale, produits pros, café offert.",
        "cta_principal": "Prendre RDV",
        "wa_message": "Demande de RDV coupe homme",
        "zone": "Bonnelles + Yvelines sud",
        "annee": "2020",
        "hero_img": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=1200&h=800&fit=crop",
        "lead_services": "Coiffure homme complète, dans l'ambiance d'un vrai barbier.",
        "services": [
            ("✂️", "Coupe homme", "Coupe classique, dégradé, militaire, sculptée. Consultation incluse."),
            ("🧔", "Taille de barbe", "Rasage traditionnel serviette chaude, taille précise, huile à barbe."),
            ("💈", "Combo coupe + barbe", "Le forfait complet. 45 minutes, café inclus, finition parfaite."),
            ("🧴", "Soin capillaire", "Shampoing, masque, soin cuir chevelu. Produits pros American Crew."),
            ("🎨", "Coloration homme", "Camouflage cheveux blancs, effet méché. Résultat naturel."),
            ("👶", "Coupe enfant", "Garçon -12 ans. Ambiance détendue, patience garantie."),
        ],
        "lead_realisations": "Quelques coupes récentes.",
        "gallery": [
            "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1593702295094-b6a18dcf4d52?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.8",
        "nb_avis": "112",
        "testimonials": [
            ("Le seul barbier où je vais. Ambiance top, coupe toujours nickel.", "Antoine D.", "Bonnelles"),
            ("Taille de barbe au rasoir, moment de détente garanti.", "Marc L.", "Chevreuse"),
        ],
        "tarifs": [
            ("Coupe homme", "22€", "30 min"),
            ("Taille de barbe", "15€", "20 min"),
            ("Coupe + barbe", "32€", "45 min"),
            ("Soin complet", "45€", "1h"),
        ],
        "cta_titre": "Prêt pour une nouvelle coupe ?",
        "cta_texte": "RDV en ligne ou appel direct. Ouvert du mardi au samedi, 9h-19h.",
        "cta_bouton": "Prendre RDV",
    },
    "photographe": {
        "marque": "Studio Lumière Yvelines",
        "tagline": "Photographe pro",
        "titre_page": "Studio Lumière Yvelines | Photographe pro 78",
        "description": "Photographe professionnel Yvelines. Mariage, portrait, entreprise, événementiel. Studio + déplacement.",
        "badge": "📸 Studio & extérieur",
        "titre_hero": "Des <em>souvenirs</em> qui durent<br>toute une vie.",
        "sous_titre": "Photographe pro spécialisé mariage, portrait, corporate. Studio à Chevreuse, déplacement France entière.",
        "cta_principal": "Demander un devis",
        "wa_message": "Demande de devis photographe",
        "zone": "Yvelines + Île-de-France",
        "annee": "2016",
        "hero_img": "https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=1200&h=800&fit=crop",
        "lead_services": "Tous types de prestations photo, pro et passionné.",
        "services": [
            ("💒", "Mariage", "Reportage complet, préparatifs, cérémonie, soirée. Album photo inclus."),
            ("👤", "Portrait", "Studio, extérieur, entreprise. Séance 1h, retouches pro, fichier HD."),
            ("🏢", "Corporate", "Photos équipe, locaux, événements pro. Pour site web et communication."),
            ("📦", "E-commerce", "Packshot produit, photo culinaire, vitrine web. Studio + retouche."),
            ("👶", "Naissance & famille", "Séance à domicile, photos nouveau-né, grossesse, fratrie."),
            ("🎭", "Événementiel", "Anniversaires, baptêmes, séminaires. Reportage sur mesure."),
        ],
        "lead_realisations": "Quelques shootings récents.",
        "gallery": [
            "https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1554048612-b6a482bc67e5?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1519741497674-611481863552?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "5.0",
        "nb_avis": "89",
        "testimonials": [
            ("Photos de mariage magnifiques, on revit la journée. Un grand merci !", "Camille & François", "Rambouillet"),
            ("Photos corporate pour notre site, exactement le style qu'on voulait.", "Marc B.", "Versailles"),
        ],
        "tarifs": [
            ("Portrait studio", "À partir de 150€", "1h, 10 retouchées"),
            ("Mariage", "À partir de 1500€", "Demi-journée, album inclus"),
            ("Corporate", "Sur devis", "Selon volume"),
            ("Packshot", "À partir de 8€/photo", "Min 20 photos"),
        ],
        "cta_titre": "Un projet photo en tête ?",
        "cta_texte": "Devis gratuit sous 24h. Premier RDV découverte offert.",
        "cta_bouton": "Demander un devis",
    },
    "coiffeur-barbier": {
        "marque": "Barbier Moderne 78",
        "tagline": "Salon mixte",
        "titre_page": "Barbier Moderne 78 | Coiffeur mixte Yvelines",
        "description": "Salon de coiffure mixte. Coupe homme, femme, enfant, coloration, balayage.",
        "badge": "💇 Mixte & famille",
        "titre_hero": "Toute la famille<br>coiffée avec <em>soin</em>.",
        "sous_titre": "Salon moderne, ambiance chaleureuse. Coupe homme, femme, enfant, coloration, soins capillaires.",
        "cta_principal": "Prendre RDV",
        "wa_message": "RDV coiffure",
        "zone": "Bonnelles + alentours",
        "annee": "2017",
        "hero_img": "https://images.unsplash.com/photo-1560066984-138dadb7c079?w=1200&h=800&fit=crop",
        "lead_services": "Coiffure pour toute la famille.",
        "services": [
            ("💇‍♀️", "Coupe femme", "Coupe, brushing,造型. Conseils personnalisés selon votre visage."),
            ("💇", "Coupe homme", "Classique, tendance, dégradé. Consultation incluse."),
            ("👧", "Coupe enfant", "-12 ans, ambiance détendue, tarif préférentiel."),
            ("🎨", "Coloration", "Couleur, mèches, balayage, ombré. Produits L'Oréal, Wella."),
            ("💆", "Soins", "Masque, soin profond, soin cuir chevelu. Produits Kérastase."),
            ("👰", "Coiffure mariage", "Essai + jour J. Chignon,造型, accessoires."),
        ],
        "lead_realisations": "Quelques créations.",
        "gallery": [
            "https://images.unsplash.com/photo-1560066984-138dadb7c079?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.7",
        "nb_avis": "76",
        "testimonials": [
            ("Salon familial, on y va depuis 5 ans. Toujours content.", "Famille D.", "Bonnelles"),
            ("Coloration parfaite, on me compliment à chaque fois.", "Sylvie M.", "Limours"),
        ],
        "tarifs": [
            ("Coupe femme", "À partir de 35€", "Selon longueur"),
            ("Coupe homme", "22€", ""),
            ("Coupe enfant", "15€", "-12 ans"),
            ("Coloration", "À partir de 55€", "Hors produits"),
        ],
        "cta_titre": "Prêt à changer de tête ?",
        "cta_texte": "RDV en ligne ou par téléphone. Ouvert du mardi au samedi.",
        "cta_bouton": "Prendre RDV",
    },
    "osteo": {
        "marque": "Cabinet Ostéo Bonnelles",
        "tagline": "Ostéopathie douce",
        "titre_page": "Cabinet Ostéo Bonnelles | Ostéopathe 78",
        "description": "Ostéopathe D.O. à Bonnelles. Douleurs dos, migraines, sport, nourrisson. Cabinet moderne.",
        "badge": "🦴 Ostéopathie D.O.",
        "titre_hero": "Soulagez vos <em>douleurs</em><br>en douceur.",
        "sous_titre": "Ostéopathe diplômé D.O. à Bonnelles. Lombalgies, cervicalgies, migraines, sport, nourrisson, femmes enceintes.",
        "cta_principal": "Prendre RDV",
        "wa_message": "RDV ostéopathe",
        "zone": "Bonnelles + Yvelines sud",
        "annee": "2018",
        "hero_img": "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=1200&h=800&fit=crop",
        "lead_services": "Ostéopathie pour tous les âges et toutes les situations.",
        "services": [
            ("🦴", "Lombalgie & mal de dos", "Lombalgie aiguë/chronique, sciatique, hernie discale, lumbago."),
            ("🤕", "Cervicalgie & migraines", "Torticolis, cervicalgie chronique, céphalées de tension, névralgie d'Arnold."),
            ("🏃", "Sportifs", "Tendinite, entorse, pubalgie, récupération sportive, préparation compétition."),
            ("🤰", "Femmes enceintes", "Douleurs ligamentaires, sciatique de grossesse, préparation accouchement."),
            ("👶", "Nourrissons", "Coliques, reflux, plagiocéphalie, troubles sommeil, succion difficile."),
            ("😰", "Stress & anxiété", "Troubles du sommeil, nervosité, sensation de blocage, oppression thoracique."),
        ],
        "lead_realisations": "Quelques motifs de consultation fréquents.",
        "gallery": [
            "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1611073615452-4889ed1c1f0e?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.9",
        "nb_avis": "143",
        "testimonials": [
            ("Migraines chroniques soulagées en 3 séances. Je recommande vivement.", "Isabelle G.", "Bonnelles"),
            ("Sciatique de grossesse traitée efficacement, merci !", "Mathilde L.", "Limours"),
        ],
        "tarifs": [
            ("Consultation adulte", "60€", "45 min"),
            ("Consultation enfant", "50€", "30 min"),
            ("Consultation nourisson", "55€", "30 min"),
            ("Urgence (sous 24h)", "75€", "Selon dispo"),
        ],
        "cta_titre": "Une douleur qui vous gêne ?",
        "cta_texte": "RDV sous 48h en semaine. Cabinet accessible, parking gratuit.",
        "cta_bouton": "Prendre RDV",
    },
    "veterinaire": {
        "marque": "Clinique Vétérinaire Yvelines",
        "tagline": "Vétérinaire 78",
        "titre_page": "Clinique Vétérinaire Yvelines | Veto 78",
        "description": "Clinique vétérinaire à Chevreuse. Consultations, chirurgie, urgences, hospitalisation. Tous animaux de compagnie.",
        "badge": "🐾 Clinique vétérinaire",
        "titre_hero": "Vos animaux <em>entre de bonnes mains</em>.",
        "sous_titre": "Clinique vétérinaire moderne à Chevreuse. Consultations, chirurgie, urgences, hospitalisation. Équipe passionnée.",
        "cta_principal": "Prendre RDV",
        "wa_message": "RDV vétérinaire",
        "zone": "Chevreuse + Yvelines",
        "annee": "2014",
        "hero_img": "https://images.unsplash.com/photo-1450778869180-41d0601a046e?w=1200&h=800&fit=crop",
        "lead_services": "Soins vétérinaires complets pour vos compagnons.",
        "services": [
            ("🐕", "Consultations", "Vaccins, bilans de santé, conseils alimentation. Sur RDV ou sans."),
            ("🔪", "Chirurgie", "Stérilisation, détartrage, chirurgie osseuse. Bloc opératoire équipé."),
            ("🚨", "Urgences", "Astreinte 24h/24, 7j/7. Appelez le numéro d'urgence en dehors des heures."),
            ("🏥", "Hospitalisation", "Chenil et chatterie séparés, surveillance continue, soins intensifs."),
            ("🔬", "Laboratoire", "Analyses sanguines, urinaires, coprologie. Résultats en 30 min."),
            ("🛒", "Boutique & alimentation", "Croquettes premium, accessoires, antiparasitaires. Conseils gratuits."),
        ],
        "lead_realisations": "Quelques cas récents.",
        "gallery": [
            "https://images.unsplash.com/photo-1450778869180-41d0601a046e?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1561948955-570b270e7c36?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.8",
        "nb_avis": "201",
        "testimonials": [
            ("Vétérinaire à l'écoute, prend le temps d'expliquer. Mon chien est suivi depuis 5 ans.", "Famille P.", "Chevreuse"),
            ("Urgence un dimanche soir, ils ont répondu. Merci pour votre dévouement.", "Marc D.", "Bonnelles"),
        ],
        "tarifs": [
            ("Consultation", "À partir de 45€", "Selon acte"),
            ("Vaccin", "À partir de 55€", "CHPPi + rage"),
            ("Stérilisation chat", "À partir de 120€", "F + anesthésie"),
            ("Urgence", "90€ + actes", "Majoration nuit/WE"),
        ],
        "cta_titre": "Votre animal a besoin de nous ?",
        "cta_texte": "RDV en ligne ou appel direct. Urgences 24h/24 au numéro habituel.",
        "cta_bouton": "Prendre RDV",
    },
    "paysagiste": {
        "marque": "Jardin Pro 78",
        "tagline": "Paysagiste & Jardinier",
        "titre_page": "Jardin Pro 78 | Paysagiste Yvelines",
        "description": "Paysagiste Yvelines. Création jardin, entretien, élagage, terrasse bois. Devis gratuit.",
        "badge": "🌿 Jardin & Paysage",
        "titre_hero": "Créez le <em>jardin</em><br>de vos rêves.",
        "sous_titre": "Conception, création, entretien de jardins. Terrasse bois, piscine, éclairage, arrosage automatique.",
        "cta_principal": "Demander un devis",
        "wa_message": "Devis paysagiste",
        "zone": "Yvelines (78) + Essonne (91)",
        "annee": "2013",
        "hero_img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&h=800&fit=crop",
        "lead_services": "Création, aménagement, entretien de jardins et espaces verts.",
        "services": [
            ("🌱", "Création de jardin", "Conception 3D, plantation, gazon, massifs fleuris, potager."),
            ("🌳", "Élagage & abattage", "Élagage arbres, abattage, dessouchage. Taille douce ou sévère."),
            ("🪵", "Terrasse bois", "Terrasse pin, mélèze, composite. Préparation sol, lambourde, fixation invisible."),
            ("💧", "Arrosage automatique", "Programmateur, goutte-à-goutte, tuyère. Économie d'eau jusqu'à 70%."),
            ("✂️", "Entretien annuel", "Tonte, taille, désherbage, feuilles. Contrat mensuel ou ponctuel."),
            ("💡", "Éclairage jardin", "Spots LED, bornes, projecteurs. Ambiance et sécurité."),
        ],
        "lead_realisations": "Quelques jardins créés.",
        "gallery": [
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=600&h=400&fit=crop",
        ],
        "note_moyenne": "4.8",
        "nb_avis": "97",
        "testimonials": [
            ("Magnifique terrasse bois réalisée en 1 semaine. Travail soigné, prix correct.", "Famille G.", "Bonnelles"),
            ("Jardin entretenu toute l'année, contrat au top. Équipe sérieuse.", "Patricia L.", "Chevreuse"),
        ],
        "tarifs": [
            ("Création jardin", "À partir de 80€/m²", "Selon aménagements"),
            ("Terrasse bois", "À partir de 120€/m²", "Pin classe 4"),
            ("Élagage", "À partir de 150€", "Selon hauteur"),
            ("Entretien mensuel", "À partir de 80€/mois", "300m² max"),
        ],
        "cta_titre": "Un projet d'aménagement ?",
        "cta_texte": "Devis gratuit sous 48h. On se déplace pour évaluer votre jardin.",
        "cta_bouton": "Demander un devis",
    },
}


def render(metier_data, template):
    """Remplace les placeholders par les données du métier."""
    html = template
    for key, value in metier_data.items():
        if isinstance(value, list):
            if key == "services":
                rendered = ""
                for icon, title, desc in value:
                    rendered += f'''
<div class="card">
<span class="icon">{icon}</span>
<h3>{title}</h3>
<p>{desc}</p>
</div>'''
                html = html.replace("{SERVICES}", rendered)
            elif key == "gallery":
                rendered = ""
                for img in value:
                    rendered += f'<img src="{img}" alt="Réalisation" loading="lazy">'
                html = html.replace("{GALLERY}", rendered)
            elif key == "testimonials":
                rendered = ""
                for content, author, city in value:
                    rendered += f'''
<div class="testi-card">
<p>{content}</p>
<div class="testi-author">{author}</div>
<div class="testi-meta">{city}</div>
</div>'''
                html = html.replace("{TESTIMONIALS}", rendered)
            elif key == "tarifs":
                rendered = ""
                for titre, prix, note in value:
                    rendered += f'''
<div class="card">
<h3>{titre}</h3>
<span class="price">{prix}</span>
<p>{note}</p>
</div>'''
                html = html.replace("{TARIFS}", rendered)
        else:
            html = html.replace(f"{{{key.upper()}}}", str(value))

    # Calcul du marque_lower
    html = html.replace("{MARQUE_LOWER}", metier_data["marque"].lower().replace(" ", "-").replace("é", "e"))
    return html


# Génère tous les fichiers
for slug, data in METIERS.items():
    html = render(data, TEMPLATE)
    out = f'/data/botarmory-site/demo/{slug}.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    size = os.path.getsize(out) / 1024
    print(f"  ✓ {slug:20} → {out} ({size:.0f} KB)")

print(f"\n✅ {len(METIERS)} démos générés")
