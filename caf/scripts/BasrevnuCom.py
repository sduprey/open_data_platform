# -*- coding: utf-8 -*-


import pandas as pd
import glob

# Variable		Type	Label
# Communes		Char	NOM DE LA COMMUNE
# Codes_Insee		Char	NUMERO DE LA COMMUNE, CODE INSEE
# NB_allocataires_ress	Num	NOMBRE DE FOYERS ALLOCATAIRES DE REFERENCE POUR CALCUL DES "BAS REVENUS" (CF définition du Jeux de Données)
# NB_pers_couv_ress	Num	NOMBRE DE PERSONNES COUVERTES DE REFERENCE POUR CALCUL DES "BAS REVENUS" (CF définition du Jeux de Données)
# ALL_bas_revenu		Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES BAS REVENUS
# Pers_bas_revenu		Num	NOMBRE TOTAL DE PERSONNES COUVERTES PAR LES FOYERS BAS REVENUS
#
#
# ***********DESCRIPTION DES PRESTATIONS***********
#
# Pour une explication exhaustive sur les "bas revenus" voir directement la page de définition du Jeux de Données.
#
#
# ***********REMARQUES***********
#
# 1)Le foyer allocataire est composé du responsable du dossier (personne qui perçoit au moins une prestation au regard de sa situation
# familiale et/ou monétaire), et l'ensemble des autres ayants droit au sens de la règlementation en vigueur (conjoint, enfant(s) et
# autre(s) personne(s) à charge).
# Plusieurs foyers allocataires peuvent cohabiter dans un même lieu, ils constituent alors un seul ménage au sens de la définition
# statistique Insee. C’est le cas, par exemple, lorsque un couple perçoit des allocations logement et héberge son enfant titulaire d'un
# minimum social des Caf (RSO, RSA, AAH).
# En pratique, le terme "allocataire" est souvent utilisé à la place de "foyer allocataire".
#
# 2) Le droit versable signifie que le foyer allocataire remplit toutes les conditions pour être effectivement payé au titre du mois
# d’observation. En particulier ne sont pas inclus dans ce périmètre les bénéficiaires qui n’ont pas fourni l’intégralité de leurs
# pièces justificatives, ou ceux dont le montant de la prestation est inférieur au seuil de versement.
#
# 3) A partir de 2014, le champ géographique d’observation du jeu de données correspond à la commune de résidence du foyer allocataire
# telle qu’elle est enregistrée dans le fichier statistique des allocataires extrait début d’année N+1 et ce quelle que soit la Caf de
# gestion.Les deux premières lignes du fichier recouvrent les allocataires résidents à l'étranger (code 99999) et les allocataires
# dont la commune de résidence est inconnue (code XXXXX).
# En 2012 et 2013 les résidents à l'étranger n'ont pas été comptabilisés.
# En 2009, 2010 et 2011, la première ligne (code 99999) recouvre, en plus des résidents à l'étranger, tous les allocataires vivant sur
# une commune en dehors du territoire de leur caf de gestion.
#
# 4) L'application d'un blanc ' ' est dû à deux cas de figure soit l'information est manquante, soit il y a eu application d'un secret
# statistique. Le secret statistique est appliqué à toutes les valeurs inférieures à 5. De plus, pour éviter de déduire certaines
# valeurs manquantes d'autres valeurs par croisement (exemple, différence avec la totalité dans le cas d'une seule valeur manquante), un
# secret statistique est appliqué sur d'autres valeurs.
#
#
# ***********Titres des fichiers***********
#
# Bas_revenu_Com_XXXX.csv
# où XXXX est l'année de référence
#
# ***********Informations additionnelles***********
#
# Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)M
# Fréquence de diffusion : Annuelle
# Granularité temporelle : Mois
# Unité : Nombre de foyers Allocataires
# Champ : France, régime général + régime agricole dans les Dom
# Zone géographique : Commune
#
#
# ***********LIENS***********
#
# Retrouvez plus d'informations sur le site de la branche famille: http://www.caf.fr/
# et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales


df = pd.read_csv('source/BasrevenuCom2009.csv', sep=";")


# Old Columns parsing : https://github.com/anthill/open-moulinette/pull/40
#df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
#              'ALL_bas_revenu_2009', 'Pers_bas_revenu_2009']

df.columns = ['Communes', 'Codes_Insee', 'ALL_bas_revenu_2009', 
              'Pers_bas_revenu_2009', 'NB_pers_couv_ress_2009',  'NB_allocataires_2009']

files = glob.glob('source/BasrevenuCom*')

for path_file in files:
    year = str(path_file[-8:-4])
    if (year != '2009'):
        df_temp = pd.read_csv(path_file, sep=';')
        
        # Rename Col with year
        year_col = ['Communes', 'Codes_Insee']
        features_col = []
        for col in df_temp.columns[-4:]:
            year_col.append(col +"_"+ year)
            features_col.append(col +"_"+ year)
        
        # Adding key for mergeing
        features_col.append('Codes_Insee')
        df_temp.columns = year_col
        df = pd.merge(df, df_temp[features_col], how='inner', on='Codes_Insee')


# Rename col to have unique name in futur merge
list_col = []
for col in df.columns:
    if "nb_allocataires" in col.lower(): 
        list_col.append(col+"_BC") # BC = BasrevnuCOM
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_BasrevenuCom.csv', encoding='utf-8', index=False)

## Features 
#u'ALL_bas_revenu_2009',
#       u'Pers_bas_revenu_2009', u'NB_pers_couv_ress_2009',
#       u'NB_allocataires_2009_BC', u'ALL_bas_revenu_2010',
#       u'Pers_bas_revenu_2010', u'NB_pers_couv_ress_2010',
#       u'NB_allocataires_ress_2010_BC', u'ALL_bas_revenu_2011',
#       u'Pers_bas_revenu_2011', u'NB_pers_couv_ress_2011',
#       u'NB_allocataires_ress_2011_BC', u'ALL_bas_revenu_2012',
#       u'Pers_bas_revenu_2012', u'NB_pers_couv_ress_2012',
#       u'NB_allocataires_ress_2012_BC', u'ALL_bas_revenu_2013',
#       u'Pers_bas_revenu_2013', u'NB_pers_couv_ress_2013',
#       u'NB_allocataires_ress_2013_BC', u'ALL_bas_revenu_2014',
#       u'Pers_bas_revenu_2014', u'NB_pers_couv_ress_2014',
#       u'NB_allocataires_ress_2014_BC'
