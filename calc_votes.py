#! /usr/bin/env python3
# coding: utf-8

import argparse
import logging as lg
import pandas as pd
import matplotlib.pyplot as plt

# Fonction de récupération du nom
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--name",help="""Nom du MP dont on recherche
                        les votes""")
    parser.add_argument("-s","--statistiques", action='store_true',
                        help="""Statistiques des votes du MP""")
    parser.add_argument("-d","--detail", action='store_true',
                        help="""Détail des votes du MP""")
    return parser.parse_args()

# Fonction de préparation du dataframe des votes du député
def prep_votes(mp_code):

    # Chargement et classement du fichier des votes
    votes = pd.read_csv('data/votes.csv')
    votes.sort_values(by="date", inplace=True)
    votes.reset_index(inplace=True, drop=True)

    # Transformation des strings de mps en listes
    def trait_chaine(chaine):
        return chaine.strip().split()

    # Nettoyage des listes de mp vides
    def nettoyage(liste):
        if liste == ['nan']:
            liste = []
        return liste

    # Fonction d'identification du mp dans les votes
    def identify_mp(liste):
        vote = 0
        if mp_code in liste:
            vote = 1
        return vote

    # Mise en listes des colonnes de votes
    columns = ['nonVotants', 'pours', 'contres', 'abstentions']
    for column in columns:
        votes[column] = votes[column].map(str)
        votes[column] = votes[column].map(trait_chaine)
    votes = votes.applymap(nettoyage)
    votes_mp = votes.copy()

    # Recherche des votes du mp
    for column in columns:
        votes_mp[column] = votes_mp[column].map(identify_mp)
    votes_mp['controle'] = votes_mp['nonVotants'] + votes_mp['pours'] + \
        votes_mp['contres'] + votes_mp['abstentions']
    votes_mp = votes_mp[votes_mp['controle'] == 1].drop(columns='controle')

    return [votes_mp.pours.sum(), votes_mp.contres.sum(),
            votes_mp.abstentions.sum(), votes_mp.nonVotants.sum(), len(votes)]

# Fonction de chargement et de choix de la liste des députés
def chose_mp(name):
    mps = pd.read_csv('data/current_mps.csv', sep=';')
    choices = mps[mps['nom'].str.contains(name.capitalize())][['nom', 'id_an']]
    if len(choices) == 0:
        return None, None
    elif len(choices) == 1:
        return 'PA' + str(choices.loc[choices.index[0], 'id_an']), \
            choices.loc[choices.index[0], 'nom']
    else:
        print(choices[['nom']])
        Id = input('Quelle ligne ? ')
        return 'PA' + str(choices.loc[int(Id), 'id_an']), choices.loc[int(Id), 'nom']

# Fonction d'impression des statistiques du député
def plot_stat(name, pours, contres, abstentions, nonVotants, scrutins):

    # Préparation des variables
    participation = pours + contres + abstentions + nonVotants
    absence = scrutins - participation

    # Préparation du graphique
    _, (ax1, ax2) = plt.subplots(1,2, figsize=(13,3))

    # Graphique de présence
    ax1labels = ['Présent', 'Absent']
    ax1sizes = [participation, absence]
    ax1colors = ['blue', 'pink']
    ax1explode = (0.1, 0)
    ax1.pie(ax1sizes, labels=ax1labels, explode=ax1explode,
            colors=ax1colors, autopct='%1.1f%%', shadow=True,
            startangle=180)
    ax1.axis('equal')
    ax1.set_title(f"Présence de {name}")

    # Graphique de votes
    ax2labels = ['Pour', 'Contre', 'Abstention', 'Non votant']
    ax2sizes = [pours, contres, abstentions, nonVotants]
    ax2colors = ['lime', 'red', 'yellow', 'lightgray']
    ax2explode = (0.1, 0.1, 0, 0)
    if nonVotants == 0:
        ax2labels = ax2labels[0: -1]
        ax2sizes = ax2sizes[0: -1]
        ax2colors = ax2colors[0: -1]
        ax2explode = (0.1, 0.1, 0)
    ax2.pie(ax2sizes, labels=ax2labels, explode=ax2explode,
            colors=ax2colors, autopct='%1.1f%%', shadow=True,
            startangle=0)
    ax2.axis('equal')
    ax2.set_title(f"Votes de {name}")

    plt.show()

# Main function
def main():
    args = parse_arguments()
    try:
        name = args.name
        if name is None:
            raise Warning('Vous devez indiquer un nom de député !')
        mp_code, nom = chose_mp(name)
        if mp_code is None :
            raise Warning('Pas de député avec ce nom !')
        votes = prep_votes(mp_code)
        participation = votes[0] + votes[1] + votes[2] + votes[3]
        print(nom)
        print(f'Participation à {participation} scrutins sur {votes[4]}')
        print(f'Votes pour : {votes[0]}')
        print(f'Votes contre : {votes[1]}')
        print(f'Abstentions : {votes[2]}')
        print(f'Non votant : {votes[3]}')
        if args.statistiques:
            plot_stat(nom, votes[0], votes[1], votes[2], votes[3], votes[4])
    except Warning as er_name:
        lg.warning(er_name)
    finally:
        print('#################### Analysis is over ######################')

if __name__ == '__main__':
    main()
