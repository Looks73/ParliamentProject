#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
from calc_votes import prep_votes

mps = pd.read_csv('data/current_mps.csv', sep=';')
votes = {}
votes['id_an'] = []
votes['pours'] = []
votes['contres'] = []
votes['abstentions'] = []
votes['nonVotants'] = []
votes['scrutins'] = []

for mp in mps.id_an:
    mp_id = 'PA' + str(mp)
    mp_votes = prep_votes(mp_id)
    votes['id_an'].append(mp)
    votes['pours'].append(mp_votes[0])
    votes['contres'].append(mp_votes[1])
    votes['abstentions'].append(mp_votes[2])
    votes['nonVotants'].append(mp_votes[3])
    votes['scrutins'].append(mp_votes[0] + mp_votes[1] + mp_votes[2] + mp_votes[3])

votes_mps = pd.DataFrame(votes)

votes_mps = votes_mps.merge(mps, on='id_an', how='right')\
    [['nom', 'num_deptmt', 'parti_ratt_financier', 'pours', 'contres',
      'abstentions', 'nonVotants', 'scrutins']]
    
votes_mps.to_csv('data/votes_mps.csv', index=False)
