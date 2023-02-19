# ----------------------------------
#       Chargement parlementaires
# ----------------------------------
load_mps:
	@rm -rf data/current_mps.csv
	@curl -s 'https://www.nosdeputes.fr/deputes/enmandat/csv' > data/current_mps.csv

# ----------------------------------
#       Chargement votes
# ----------------------------------
votes:
	@say "Cette fonction extrait les résultats de tous les scrutins ; c'est long"
	@rm -rf data/xml/votes
	@curl 'http://data.assemblee-nationale.fr/static/openData/repository/16/loi/scrutins/Scrutins.xml.zip' > scrutins.zip
	@unzip scrutins.zip
	@mv xml data/xml/votes
	@rm scrutins.zip

ex_votes:
	@say "Cette fonction calcule les votes de tous les parlementaires"
	@rm -rf data/votes.csv
	@python extract_votes.py

# ----------------------------------
#       Chargement interventions
# ----------------------------------
interventions:
	@say "Cette fonction extrait les compte-rendus de l'assemblée nationale ; c'est très long"
	@rm -rf data/xml/compteRendus
	@curl 'https://data.assemblee-nationale.fr/static/openData/repository/16/vp/syceronbrut/syseron.xml.zip' > debats.zip
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