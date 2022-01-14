'''Module d'analyse du fichier csv'''

#! /usr/bin/env python3
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt

class SetOfParliamentMembers():
#Permet de créer un Set of parliament members avec nom
    def __init__(self, name):
        self.name = name

    def data_from_csv(self, csv_file):
        self.dataframe = pd.read_csv(csv_file, sep=';')

    def data_from_dataframe(self, dataframe):
        self.dataframe = dataframe

    def display_chart(self):
        _, fig_ax = plt.subplots()
        labels = ['Hommes', 'Femmes']
        sizes = [len(self.dataframe[self.dataframe.sexe == 'H']),
                 len(self.dataframe[self.dataframe.sexe == 'F'])]
        colors = ['lightskyblue', 'lightcoral']
        explode = (0, 0.1)
        fig_ax.pie(sizes, labels=labels, explode=explode,
                colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        fig_ax.axis('equal')
        plt.title(f"{self.name} ({len(self.dataframe)} MPs)")
        plt.show()

    def split_by_political_party(self):
        splitted_mps = {}
        parties = self.dataframe['parti_ratt_financier'].dropna().unique()
        for party in parties :
            data = self.dataframe[self.dataframe['parti_ratt_financier'] == party]
            subset = SetOfParliamentMembers(f'MPs from party "{party}"')
            subset.data_from_dataframe(data)
            splitted_mps[party] = [subset, len(subset.dataframe)]
        return splitted_mps

    def split_by_searchname(self, searchname):
        data = self.dataframe[self.dataframe['nom'].str.
                              contains(searchname.capitalize())].reset_index(drop=True)
        names = SetOfParliamentMembers(f'MPs with name containing "{searchname}"')
        names.data_from_dataframe(data)
        return names

def launch_analysis(data_file, info = False, byparty = False,
                    searchname = False, groupfirst = False):
    sopm = SetOfParliamentMembers("All MPs")
    sopm.data_from_csv(os.path.join("data",data_file))

    if searchname:
        spm = sopm.split_by_searchname(searchname)
        df_pm = spm.dataframe
        name = spm.name
        if len(df_pm)>0:
            for i in range(len(df_pm)):
                print(f"Name : {df_pm.loc[i, 'nom']} ; \
                      Party : {df_pm.loc[i, 'parti_ratt_financier']}")
    else:
        spm = sopm
        df_pm = spm.dataframe
        name = spm.name

    if info:
        print(f"[{name}] : {len(df_pm)} members")

    if byparty:
        subsets = []
        for _, subset in spm.split_by_political_party().items():
            subsets.append(subset)
            subsets.sort(key = lambda x: x[1], reverse=True)
        number = len(subsets)
        if groupfirst:
            number = int(min(number, int(groupfirst)))
        if number !=0:
            for i in range(number):
                subsets[i][0].display_chart()
    else:
        spm.display_chart()
