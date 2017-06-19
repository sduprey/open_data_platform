# -*- coding: utf-8 -*-

import pandas as pd
import glob


###### Description du fichier Excel
# Variable	Type	Label
# Communes	Char	NOM DE LA COMMUNE
# Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
# NB_allocataires	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
#
# TR50PFRB	Num	Nombre de foyers allocataires dont les ressources sont constituées à 50 % ou plus des prestations Caf
# TR100PFRB	Num	Nombre de foyers allocataires dont les ressources sont constituées à 100 % des prestations Caf
#
#
# ***********DESCRIPTION DES PRESTATIONS***********
#
#
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


df = pd.read_csv('../source/DependancePrestaCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'TR50PFRB_2009', 'TR100PFRB_2009']

files = glob.glob('source/DependancePrestaCom*')

for path_file in files:
    year = str(path_file[-8:-4])
    if (year != '2009'):
        df_temp = pd.read_csv(path_file, sep=';')
        
        # Rename Col with year
        year_col = ['Communes', 'Codes_Insee']
        features_col = []
        for col in df_temp.columns[-3:]:
            year_col.append(col +"_"+ year)
            features_col.append(col +"_"+ year)
        
        # Adding key for mergeing
        features_col.append('Codes_Insee')
        df_temp.columns = year_col
        df = pd.merge(df, df_temp[features_col], how='inner', on='Codes_Insee')


# Rename col to have unique name in futur merge
list_col = []
for col in df.columns:
    if "NB_Allocataires" in col:
        list_col.append(col+"_DPC") # DPC = DependancePrestaCom
    else:
        list_col.append(col)
df.columns = list_col

final_count = df.shape[0]

df.to_csv('data/full_DependancePrestaCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Allocataires_2009_DPC',
#       u'TR50PFRB_2009', u'TR100PFRB_2009', u'NB_Allocataires_2010_DPC',
#       u'TR50PFRB_2010', u'TR100PFRB_2010', u'NB_Allocataires_2011_DPC',
#       u'TR50PFRB_2011', u'TR100PFRB_2011', u'NB_Allocataires_2012_DPC',
#       u'TR50PFRB_2012', u'TR100PFRB_2012', u'NB_Allocataires_2013_DPC',
#       u'TR50PFRB_2013', u'TR100PFRB_2013', u'NB_Allocataires_2014_DPC',
#       u'TR50PFRB_2014', u'TR100PFRB_2014'

