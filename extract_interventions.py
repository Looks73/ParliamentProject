#! /usr/bin/env python3
# coding: utf-8

import xml.etree.ElementTree as et
import os
import pandas as pd
import re

# Constitution de la liste des fichiers
liste = os.listdir('data/xml/compteRendus/')
liste.sort()

for file in liste:

    xmlfile = 'data/xml/compteRendus/' + file

    # Parsing du fichier en entrée
    tree = et.parse(xmlfile)
    root = tree.getroot()

    # Initialisation des tableaux de nom et texte des interventions
    nom = []
    texte = []

    # Récupération des interventions, uniquement identifiées
    n_int=0
    for child in root.iter():
        if child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}paragraphe':
            for littlechild in child.iter():
                if littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}nom':
                    nom.append(littlechild.text)
                    n_int += 1
                elif littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}texte' \
                    and child.text is not None and len(texte) == n_int-1:
                    texte.append(littlechild.text)
    
    if len(nom) == len(texte):
        # Intégration dans un DataFrame
        interventions = pd.DataFrame({'nom': nom, 'texte': texte})

        # Regex de nettoyage
        oldRegex = re.compile(r'\w+ +\([\w -]+\)')
        newRegex = re.compile(r'\([\w -]+\)')
        def clean_nom(depute):
            if re.search(oldRegex, depute):
                depute = re.sub(newRegex, '', depute)
            return depute
        
        # Nettoyage du DataFrame
        interventions = interventions[interventions.nom != "Mme la présidente"].reset_index(drop=True)
        interventions = interventions.loc[~interventions.nom.str.contains("député")].reset_index(drop=True)
        interventions.nom = interventions.nom.str.replace('M\.', '')
        interventions.nom = interventions.nom.str.replace('Mme','')
        interventions.nom = interventions.nom.str.replace(u'\xa0', u' ')
        interventions.nom = interventions.nom.map(clean_nom)
        interventions.nom = interventions.nom.str.strip()
        interventions.texte = interventions.texte.str.replace('                            ', ' ')
        interventions.texte = interventions.texte.str.strip()

        # Ajout au fichier CSV des interventions
        if os.path.isfile('data/interventions.csv'):
            interventions.to_csv("data/interventions.csv", mode='a', header=False, index=False)
        else:
            interventions.to_csv("data/interventions.csv", index=False)

        # Accusé de traitement du fichier
        print(f'{file} traité')
    
    else:
        # Accusé de non traitement du fichier
        print(f'{file} non traité : {len(nom)} différent de {len(texte)}')

print('**** Fin de traitement****')
