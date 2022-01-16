# ----------------------------------
#       Chargement votes
# ----------------------------------
votes:
	@rm -rf data/xml/votes
	@curl -s 'https://data.assemblee-nationale.fr/static/openData/repository/15/loi/scrutins/Scrutins_XV.xml.zip' > scrutins.zip
	@unzip scrutins.zip
	@mv xml data/xml/votes
	@rm scrutins.zip

ex_votes:
	@rm -rf data/votes.csv
	@python extract_votes.py

# ----------------------------------
#       Chargement interventions
# ----------------------------------
interventions:
	@rm -rf data/xml/compteRendus
	@curl -s 'https://data.assemblee-nationale.fr/static/openData/repository/15/vp/syceronbrut/syseron.xml.zip' > debats.zip
	@unzip debats.zip
	@mv xml/compteRendu data/xml/compteRendus
	@rm debats.zip

ex_interventions:
	@rm -rf data/interventions.csv
	@python extract_interventions.py

# -------------------------------------------
#       Calcul des votes pour tous les mp
# -------------------------------------------
votes_mps:
	@rm -rf data/votes_mps.csv
	@python votes_mps.py 

# ----------------------------------
#       Calcul des votes par mp
# ----------------------------------
votes_mp:
	@python calc_votes.py -n $(filter-out $@,$(MAKECMDGOALS)) -s

# ----------------------------------
#       Evaluation parite
# ----------------------------------
parite:
	@python parite.py -d current_mps.csv

parite_byparty:
	NB=$(strip $(filter-out $@,$(MAKECMDGOALS)))
	NREF=$(strip )
ifeq (NB, NREF)
	@python parite.py -d current_mps.csv -p
else
	@python parite.py -d current_mps.csv -p -g $(filter-out $@,$(MAKECMDGOALS))
endif