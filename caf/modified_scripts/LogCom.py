# -*- coding: utf-8 -*-


import pandas as pd
import glob

# Variable			Type	Label
# Communes			Char	NOM DE LA COMMUNE
# Codes_Insee			Char	NUMERO DE LA COMMUNE, CODE INSEE
# total_allocataires		Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
# total_allocataires_logement	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES BENEFICIAIRE D'UNE AIDE AU LOGEMENT
# total_ALF			Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES BENEFICIAIRE DE L'ALF
# total_ALS			Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES BENEFICIAIRE DE L'ALS
# total_APL			Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES BENEFICIAIRE DE L'APL
# locataire_ALF			Num	NOMBRE DE FOYERS ALLOCATAIRES, EN LOCATION OU EN FOYER BENEFICIAIRE DE L'ALF
# locataire_ALS			Num	NOMBRE DE FOYERS ALLOCATAIRES, EN LOCATION OU EN FOYER BENEFICIAIRE DE L'ALS
# locataire_APL			Num	NOMBRE DE FOYERS ALLOCATAIRES, EN LOCATION OU EN FOYER BENEFICIAIRE DE L'APL
# proprietaire_ALF		Num	NOMBRE DE FOYERS ALLOCATAIRES, PROPRIETAIRE BENEFICIAIRE DE L'ALF
# proprietaire_ALS		Num	NOMBRE DE FOYERS ALLOCATAIRES, PROPRIETAIRE BENEFICIAIRE DE L'ALF
# proprietaire_APL		Num	NOMBRE DE FOYERS ALLOCATAIRES, PROPRIETAIRE BENEFICIAIRE DE L'ALF
# total_locataire			Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES, EN LOCATION OU EN FOYER BENEFICIAIRE D'UNE AIDE AU LOGEMENT
# total_proprietaire		Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES, PROPRIETAIRE BENEFICIAIRE D'UNE AIDE AU LOGEMENT
#
# ***********DESCRIPTION DES PRESTATIONS***********
#
# Les aides au logement sont constituées de l’Allocation de Logement Familiale (ALF), de l’Allocation de Logement Social (ALS), et de l’Aide Personnalisée
# au Logement (APL). Ces trois aides ne sont pas cumulables. L’ordre de priorité d’attribution est le suivant : APL, ALF, ALS.
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
# 5)Les allocataires percevant une aide au logement et résidant en foyer, sont comptés parmis les locataires.
#
# ***********Titres des fichiers***********
#
# LOG_Com_XXXX.csv
# où XXXX est l'année de référence
#
# ***********Informations additionnelles***********
#
# Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)
# Fréquence de diffusion : Annuelle
# Granularité temporelle : Mois
# Unité : Nombre de foyers Allocataires
# Champ : France, régime général + régime agricole dans les Dom
# Zone géographique : Commune
#
#
# ***********LIENS***********
#
# Retrouvez plus d'informations sur le site de la branche famille: https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/logement-et-cadre-de-vie
# et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales

df = pd.read_csv('source/LOGCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'total_ALF_2009', 'total_ALS_2009', 'total_APL_2009', 'locataire_ALF_2009',
              'locataire_ALS_2009', 'locataire_APL_2009', 'proprietaire_ALF_2009', 'proprietaire_ALS_2009',
              'proprietaire_APL_2009', 'total_locataire_2009', 'total_proprietaire_2009',
              'total_allocataires_logement_2009']

files = glob.glob('source/LOGCom*')

for path_file in files:
    year = str(path_file[-8:-4])
    if (year != '2009'):
        df_temp = pd.read_csv(path_file, sep=';')
        df_temp.rename(columns={'total_allocataires':'NB_Allocataires'}, inplace=True)
        
        # Rename Col with year
        year_col = ['Communes', 'Codes_Insee']
        features_col = []
        for col in df_temp.columns[2:]:
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
        list_col.append(col+"_LC") # LC = LogCom
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_LogCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Allocataires_2009_LC',
#       u'total_ALF_2009', u'total_ALS_2009', u'total_APL_2009',
#       u'locataire_ALF_2009', u'locataire_ALS_2009', u'locataire_APL_2009',
#       u'proprietaire_ALF_2009', u'proprietaire_ALS_2009',
#       u'proprietaire_APL_2009', u'total_locataire_2009',
#       u'total_proprietaire_2009', u'total_allocataires_logement_2009',
#       u'NB_Allocataires_2010_LC', u'total_ALF_2010', u'total_ALS_2010',
#       u'total_APL_2010', u'locataire_ALF_2010', u'locataire_ALS_2010',
#       u'locataire_APL_2010', u'proprietaire_ALF_2010',
#       u'proprietaire_ALS_2010', u'proprietaire_APL_2010',
#       u'total_locataire_2010', u'total_proprietaire_2010',
#       u'total_allocataires_logement_2010', u'NB_Allocataires_2011_LC',
#       u'total_ALF_2011', u'total_ALS_2011', u'total_APL_2011',
#       u'locataire_ALF_2011', u'locataire_ALS_2011', u'locataire_APL_2011',
#       u'proprietaire_ALF_2011', u'proprietaire_ALS_2011',
#       u'proprietaire_APL_2011', u'total_locataire_2011',
#       u'total_proprietaire_2011', u'total_allocataires_logement_2011',
#       u'NB_Allocataires_2012_LC', u'total_ALF_2012', u'total_ALS_2012',
#       u'total_APL_2012', u'locataire_ALF_2012', u'locataire_ALS_2012',
#       u'locataire_APL_2012', u'proprietaire_ALF_2012',
#       u'proprietaire_ALS_2012', u'proprietaire_APL_2012',
#       u'total_locataire_2012', u'total_proprietaire_2012',
#       u'total_allocataires_logement_2012', u'NB_Allocataires_2013_LC',
#       u'total_ALF_2013', u'total_ALS_2013', u'total_APL_2013',
#       u'locataire_ALF_2013', u'locataire_ALS_2013', u'locataire_APL_2013',
#       u'proprietaire_ALF_2013', u'proprietaire_ALS_2013',
#       u'proprietaire_APL_2013', u'total_locataire_2013',
#       u'total_proprietaire_2013', u'total_allocataires_logement_2013',
#       u'NB_Allocataires_2014_LC', u'total_ALF_2014', u'total_ALS_2014',
#       u'total_APL_2014', u'locataire_ALF_2014', u'locataire_ALS_2014',
#       u'locataire_APL_2014', u'proprietaire_ALF_2014',
#       u'proprietaire_ALS_2014', u'proprietaire_APL_2014',
#       u'total_locataire_2014', u'total_proprietaire_2014',
#       u'total_allocataires_logement_2014'

