---
title: 'TP Threat Intel – Conception d’un outil de détection d’hameçonnage ciblé'
author:
  - \url{georges.bossert@sekoia.fr}
header-includes:
  - \usepackage[top=1in, bottom=1.25in, left=1.25in, right=1.25in]{geometry}
  - \usepackage[utf8]{inputenc}
  - \usepackage[T1]{fontenc}
  - \usepackage[francais]{babel}
  - \usepackage{datetime}
---

<!-- pandoc -f markdown -o README.pdf README.md -M date="`date "+%d %B %Y"`" -->

# Objectifs de réalisation
Un flux d’information au format STIXv2 de sites d’hammeçonnages ciblés.

# Format du TP
Travail en groupe (entre 2 et 4 personnes par groupe)

# Consignes
Imaginer, concevoir puis implémenter une solution chargée de détecter automatiquement des sites web utilisés dans le cadre de campagne d’hammeçonnages ciblés. La solution retenue devra reposer à minima sur deux sources d’informations parmis les sources suivantes :

* [CertStream Cali Dog Security](https://certstream.calidog.io/);
* [Alexa Top 1 Million Sites](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip);
* [Umbrella Popularity List](http://s3-us-west-1.amazonaws.com/umbrella-static/index.html);
* [VirusTotal : URL Abuse](https://www.virustotal.com/en/documentation/public-api/#scanning-urls);
* [BGP Ranking / CIRCL](https://www.circl.lu/projects/bgpranking/).

Développé dans le langage de votre choix, votre solution stockera la liste des alertes de détection de sites web d’hammeçonnage dans un fichier. L'alerte exprimée au format STIXv2 (type Indicator [^0]) comportera à minima les informations suivantes:

* l'url du site web détecté;
* l'heure exacte de la collecte de l'url.

Un dossier de conception sera rédigé et comportera les points suivants :

* les objectifs de votre outil (rappeler ce qu'est une attaque par hammeçonnage ciblé);
	* répérer les sites de phishing souhaitant usurper les sites gouvernementaux.
* la liste des sources et services utilisés pas votre solution et leurs descriptions succintes;
    * .csv comportant une liste des sites gouvernementaux référencés dans le monde : (url source);
    * une liste de mots clés en plusieurs langue, à élargir en fonction du nombre de matchs possibles
      (assemblé, ambassade, ministère, impôt, président, taxe, passeport ...);
    * geoAPI + circl;
    * virustotal.
* le fonctionnement général de votre solution.

# Livrables
Les livrables suivants devront être envoyés par email à l’adresse  :

* un dossier de conception envoyé par email avant la fin de séance de TP;
* le compte rendu final du TP comportant le dossier de conception, les résultat d’exécutions et les sources de l’outil. Il devra être envoyé au maximum 14 jours après la séance de TP (\formatdate{07}{02}{2018}).

# Evaluation
En plus du respect des consignes, la créativité de la solution sera évaluée.


[^0]: \url{https://oasis-open.github.io/cti-documentation/examples/indicator-for-malicious-url}
