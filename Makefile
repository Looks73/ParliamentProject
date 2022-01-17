# ----------------------------------
#       Chargement votes
# ----------------------------------
votes:
	@say "Cette fonction extrait les résultats de tous les scrutins ; c'est long"
	@rm -rf data/xml/votes
	@curl -s 'https://data.assemblee-nationale.fr/static/openData/repository/15/loi/scrutins/Scrutins_XV.xml.zip' > scrutins.zip
	@unzip scrutins.zip
	@mv xml data/xml/votes
	@rm scrutins.zip
	@say "C'est fini"

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
	@curl -s 'https://data.assemblee-nationale.fr/static/openData/repository/15/vp/syceronbrut/syseron.xml.zip' > debats.zip
	@unzip debats.zip
	@mv xml/compteRendu data/xml/compteRendus
	@rm debats.zip
	@say "C'est fini"

ex_interventions:
	@say "Cette fonction recherche les interventions de tous les parlementaires"
	@rm -rf data/interventions.csv
	@python extract_interventions.py

# -------------------------------------------
#       Calcul des votes pour tous les mp
# -------------------------------------------
votes_mps:
	@say "Cette fonction calcule les statistiques de vote de tous les parlementaires"
	@rm -rf data/votes_mps.csv
	@python votes_mps.py 

# ----------------------------------
#       Calcul des votes par mp
# ----------------------------------
votes_mp:
	@say "cette fonction calcule les statistiques de vote du parlementaire choisi"
	@python calc_votes.py -n $(filter-out $@,$(MAKECMDGOALS)) -s

# ----------------------------------
#       Evaluation parite
# ----------------------------------
parite:
	@say "Cette fonction évalue la parité de l'assemblée nationale"
	@python parite.py -d current_mps.csv

parite_byparty:
	NB=$(strip $(filter-out $@,$(MAKECMDGOALS)))
	NREF=$(strip )
ifeq (NB, NREF)
	@python parite.py -d current_mps.csv -p
else
	@python parite.py -d current_mps.csv -p -g $(filter-out $@,$(MAKECMDGOALS))
endif