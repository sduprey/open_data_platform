# -*- coding: utf-8 -*-

import pandas as pd
import glob

# Variable  Type  Label
# Communes  Char  NOM DE LA COMMUNE
# Codes_Insee Char  NUMERO DE LA COMMUNE, CODE INSEE
# NB_Allocataires Num NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
# ALL0A19   Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE MOINS DE 20 ANS
# ALL20A24  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 20 A 24 ANS
# ALL25A29  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 25 A 29 ANS
# ALL30A39  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 30 A 39 ANS
# ALL40A49  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 40 A 49 ANS
# ALL50A54* Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 50 A 54 ANS
# ALL55A59* Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 55 A 59 ANS
# ALL60A64* Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 60 A 64 ANS
# ALL65A69* Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 65 A 69 ANS
# ALL70AX*  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 70 ANS OU PLUS
# ALLAGEX   Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST D'AGE INCONNU
#
# * Attention : Avant 2011 les tranches de plus de 50 ans étaient réparties comme suit :
# ALL50A59  Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 50 A 59 ANS
# ALL60AX   Num NOMBRE DE FOYERS ALLOCATAIRES DONT LE TITUTAILRE DU DOSSIER EST AGE DE 60 ANS OU PLUS
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
# 5)L’âge retenu est l’âge atteint dans l’année (ou âge  par génération). Il correspond à la différence entre l'année d’observation et
# l'année de naissance de l'individu. Les intervalles des tranches d'âges sont des intervalles fermés.
#
# 6)L'âge inconnu correspond à des problèmes techniques ou des valeurs aberrantes saisies dans la base de données. A titre d'exemple
# les âges inférieurs à 15 ans et supérieur à 120 ans sont considérés aberrants.
#
# ***********Titres des fichiers***********
#
# -Alloc_Age_Com_XXXX.csv
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
# Retrouvez plus d'informations sur le site de la branche famille: http://www.caf.fr/
# et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales


df = pd.read_csv('source/TrancheAge2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'ALL0A19_2009', 'ALL20A24_2009', 'ALL25A29_2009', 'ALL30A39_2009',
              'ALL40A49_2009', 'ALL50A59_2009', 'ALL60AX_2009', 'ALLAGEX_2009']

files = glob.glob('source/TrancheAge*')

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
        list_col.append(col+"_TA") # TA = TrancheAge
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_TrancheAge.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Allocataires_2009_TA',
#       u'ALL0A19_2009', u'ALL20A24_2009', u'ALL25A29_2009', u'ALL30A39_2009',
#       u'ALL40A49_2009', u'ALL50A59_2009', u'ALL60AX_2009', u'ALLAGEX_2009',
#       u'NB_allocataires_2010_TA', u'ALL0A19_2010', u'ALL20A24_2010',
#       u'ALL25A29_2010', u'ALL30A39_2010', u'ALL40A49_2010', u'ALL50A59_2010',
#       u'ALL60AX_2010', u'ALLAGEX_2010', u'NB_allocataires_2011_TA',
#       u'ALL0A19_2011', u'ALL20A24_2011', u'ALL25A29_2011', u'ALL30A39_2011',
#       u'ALL40A49_2011', u'ALL50A54_2011', u'ALL55A59_2011', u'ALL60A64_2011',
#       u'ALL65A69_2011', u'ALL70AX_2011', u'ALLAGEX_2011',
#       u'NB_allocataires_2012_TA', u'ALL0A19_2012', u'ALL20A24_2012',
#       u'ALL25A29_2012', u'ALL30A39_2012', u'ALL40A49_2012', u'ALL50A54_2012',
#       u'ALL55A59_2012', u'ALL60A64_2012', u'ALL65A69_2012', u'ALL70AX_2012',
#       u'ALLAGEX_2012', u'NB_allocataires_2013_TA', u'ALL0A19_2013',
#       u'ALL20A24_2013', u'ALL25A29_2013', u'ALL30A39_2013', u'ALL40A49_2013',
#       u'ALL50A54_2013', u'ALL55A59_2013', u'ALL60A64_2013', u'ALL65A69_2013',
#       u'ALL70AX_2013', u'ALLAGEX_2013', u'NB_allocataires_2014_TA',
#       u'ALL0A19_2014', u'ALL20A24_2014', u'ALL25A29_2014', u'ALL30A39_2014',
#       u'ALL40A49_2014', u'ALL50A54_2014', u'ALL55A59_2014', u'ALL60A64_2014',
#       u'ALL65A69_2014', u'ALL70AX_2014', u'ALLAGEX_2014'
