#! /usr/bin/env python3
# coding: utf-8

import xml.etree.ElementTree as et
import os
import pandas as pd

# Constitution de la liste des fichiers
liste = os.listdir('data/xml/votes/')
liste.sort()

# Initialisation des dictionnaires
df_dico = {}
df_dico['date'] = []
df_dico['objet'] = []
df_dico['nonVotants'] = []
df_dico['pours'] = []
df_dico['contres'] = []
df_dico['abstentions'] = []

# Construction des votes
for file in liste:

    xmlfile = 'data/xml/votes/' + file

    # Parsing du fichier en entrée
    tree = et.parse(xmlfile)
    root = tree.getroot()

    # Initialisation des tableaux de résultats des votes
    nonVotants = ""
    pours = ""
    contres = ""
    abstentions = ""

    # Récupération des votes
    for child in root.iter():
        if child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}dateScrutin':
            date = child.text
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}titre':
            objet = child.text
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}nonVotants':
            for littlechild in child.iter():
                if littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}acteurRef':
                    nonVotants += littlechild.text + " "
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}pours':
            for littlechild in child.iter():
                if littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}acteurRef':
                    pours += littlechild.text + " "
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}contres':
            for littlechild in child.iter():
                if littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}acteurRef':
                    contres += littlechild.text + " "
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}abstentions':
            for littlechild in child.iter():
                if littlechild.tag == '{http://schemas.assemblee-nationale.fr/referentiel}acteurRef':
                    abstentions += littlechild.text + " "
        elif child.tag == '{http://schemas.assemblee-nationale.fr/referentiel}miseAuPoint':
            break

    df_dico['date'].append(date)
    df_dico['objet'].append(objet)
    df_dico['nonVotants'].append(nonVotants)
    df_dico['pours'].append(pours)
    df_dico['contres'].append(contres)
    df_dico['abstentions'].append(abstentions)

    # Accusé de traitement du fichier
    print(f'{file} traité')

votes = pd.DataFrame(df_dico)
votes.to_csv('data/votes.csv', index=False)
print(f'Nombre de votes : {len(votes)}')

print('**** Fin de traitement****')
