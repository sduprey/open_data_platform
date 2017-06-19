# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable		Type	Label
#Communes		Char	NOM DE LA COMMUNE
#Codes_Insee		Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_Pers_Couv_Al		Num	NOMBRE DE PERSONNES COUVERTES PAR UNE AIDE AU LOGEMENT VERSABLE
#Pers_Couv_Al_ALF	Num	NOMBRE DE PERSONNES COUVERTES PAR ALF VERSABLE
#Pers_Couv_Al_ALS	Num	NOMBRE DE PERSONNES COUVERTES PAR ALS VERSABLE
#Pers_Couv_Al_APL	Num	NOMBRE DE PERSONNES COUVERTES PAR APL VERSABLE
#
#
#***********REMARQUES***********
#
#1)Le foyer allocataire est composé du responsable du dossier (personne qui perçoit au moins une prestation au regard de sa situation
#familiale et/ou monétaire), et l'ensemble des autres ayants droit au sens de la règlementation en vigueur (conjoint, enfant(s) et
#autre(s) personne(s) à charge).
#Plusieurs foyers allocataires peuvent cohabiter dans un même lieu, ils constituent alors un seul ménage au sens de la définition
#statistique Insee. C’est le cas, par exemple, lorsque un couple perçoit des allocations logement et héberge son enfant titulaire d'un
#minimum social des Caf (RSO, RSA, AAH).
#En pratique, le terme "allocataire" est souvent utilisé à la place de "foyer allocataire".
#
#2) Le droit versable signifie que le foyer allocataire remplit toutes les conditions pour être effectivement payé au titre du mois
#d’observation. En particulier ne sont pas inclus dans ce périmètre les bénéficiaires qui n’ont pas fourni l’intégralité de leurs
#pièces justificatives, ou ceux dont le montant de la prestation est inférieur au seuil de versement.
#
#3) Le champ géographique d’observation du jeu de données correspond à la commune de résidence du foyer allocataire telle qu’elle
#est enregistrée dans le fichier statistique des allocataires extrait début d’année N+1 et ce quelle que soit la Caf de gestion.
#La première ligne du fichier dont le numéro commune est XXXXX recouvre deux cas possibles soit un code commune inconnu soit une
#commune de résidence de l'allocataire à l'étranger.
#A partir de 2014 les résidants à l'étranger et les codes communes inconnus sont dissociés en deux lignes.
#
#4) L'application d'un blanc ' ' est dû à deux cas de figure soit l'information est manquante, soit il y a eu application d'un secret
#statistique. Le secret statistique est appliqué à toutes les valeurs inférieures à 5. De plus, pour éviter de déduire certaines
#valeurs manquantes d'autres valeurs par croisement (exemple, différence avec la totalité dans le cas d'une seule valeur manquante), un
#secret statistique est appliqué sur d'autres valeurs.
#
#***********Titres des fichiers***********
#
#LOG_Perscouv_Presta_Com_XXXX.csv
#où XXXX est l'année de référence
#
#***********Informations additionnelles***********
#
#Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)
#Fréquence de diffusion : Annuelle
#Granularité temporelle : Mois
#Unité : Personnes couvertes
#Champ : France, régime général + régime agricole dans les Dom
#Zone géographique : Commune
#
#
#***********LIENS***********
#
#Retrouvez plus d'informations sur le site de la branche famille: https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/logement-et-cadre-de-vie

df = pd.read_csv('source/LOGPersPrestaCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Pers_Couv_Al_2009', 
              'Pers_Couv_Al_ALF_2009', 'Pers_Couv_Al_ALS_2009',
              'Pers_Couv_Al_APL_2009']

files = glob.glob('source/LOGPersPrestaCom*')

for path_file in files:
    year = str(path_file[-8:-4])
    if (year != '2009'):
        df_temp = pd.read_csv(path_file, sep=';')
        
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
    if "nb_allocataires" in col.lower(): # NB_Allocataires (2009) != NB_allocataires (2010)
        list_col.append(col+"_LPPC") # LPPC = LOGPersPrestaCom
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_LogPersPrestaCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Pers_Couv_Al_2009',
#       u'Pers_Couv_Al_ALF_2009', u'Pers_Couv_Al_ALS_2009',
#       u'Pers_Couv_Al_APL_2009', u'NB_Pers_Couv_Al_2010',
#       u'Pers_Couv_Al_ALF_2010', u'Pers_Couv_Al_ALS_2010',
#       u'Pers_Couv_Al_APL_2010', u'NB_Pers_Couv_Al_2011',
#       u'Pers_Couv_Al_ALF_2011', u'Pers_Couv_Al_ALS_2011',
#       u'Pers_Couv_Al_APL_2011', u'NB_Pers_Couv_Al_2012',
#       u'Pers_Couv_Al_ALF_2012', u'Pers_Couv_Al_ALS_2012',
#       u'Pers_Couv_Al_APL_2012', u'NB_Pers_Couv_Al_2013',
#       u'Pers_Couv_Al_ALF_2013', u'Pers_Couv_Al_ALS_2013',
#       u'Pers_Couv_Al_APL_2013', u'NB_Pers_Couv_Al_2014',
#       u'Pers_Couv_Al_ALF_2014', u'Pers_Couv_Al_ALS_2014',
#       u'Pers_Couv_Al_APL_2014'
