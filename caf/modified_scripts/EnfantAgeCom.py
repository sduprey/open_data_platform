# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable		Type	Label
#Communes		Char	NOM DE LA COMMUNE
#Codes_Insee		Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_enfants		Num	NOMBRE D'ENFANTS BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_0_2_ans	Num	NOMBRE D'ENFANTS DE 0 A 2 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_3_5_ans	Num	NOMBRE D'ENFANTS DE 3 A 5 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_6_11_ans	Num	NOMBRE D'ENFANTS DE 6 A 11 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_12_15_ans	Num	NOMBRE D'ENFANTS DE 12 A 15 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_16_17_ans	Num	NOMBRE D'ENFANTS DE 16 A 17 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_18_19_ans	Num	NOMBRE D'ENFANTS DE 18 A 19 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#NB_Enfants_20_24_ans	Num	NOMBRE D'ENFANTS DE 20 A 24 ANS, BENEFICIAIRES D'AU MOINS UNE PRESTATION CAF VERSABLE
#
#***********DESCRIPTION DE LA PRESTATION***********
#
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
#3) A partir de 2014, le champ géographique d’observation du jeu de données correspond à la commune de résidence du foyer allocataire
#telle qu’elle est enregistrée dans le fichier statistique des allocataires extrait début d’année N+1 et ce quelle que soit la Caf de
#gestion.Les deux premières lignes du fichier recouvrent les allocataires résidents à l'étranger (code 99999) et les allocataires
#dont la commune de résidence est inconnue (code XXXXX).
#En 2012 et 2013 les résidents à l'étranger n'ont pas été comptabilisés.
#En 2009, 2010 et 2011, la première ligne (code 99999) recouvre, en plus des résidents à l'étranger, tous les allocataires vivant sur
#une commune en dehors du territoire de leur caf de gestion.
#
#4) L'application d'un blanc ' ' est dû à deux cas de figure soit l'information est manquante, soit il y a eu application d'un secret
#statistique. Le secret statistique est appliqué à toutes les valeurs inférieures à 5. De plus, pour éviter de déduire certaines
#valeurs manquantes d'autres valeurs par croisement (exemple, différence avec la totalité dans le cas d'une seule valeur manquante), un
#secret statistique est appliqué sur d'autres valeurs.
#
#5)L’âge retenu est l’âge atteint dans l’année (ou âge  par génération). Il correspond à la différence entre l'année d’observation et
#l'année de naissance de l'individu. Les intervalles des tranches d'âges sont des intervalles fermés.
#
#6)Pour les familles de treize enfants ou plus, seuls les 12 plus jeunes enfants ont leur âges enregistrés, les ainés sont comptés par
#défaut dans la tranche âge [20 24] ans.
#
#***********Titres des fichiers***********
#
#enfant_age_Com_XXXX.csv
#où XXXX est l'année de référence
#
#***********Informations additionnelles***********
#
#Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)
#Fréquence de diffusion : Annuelle
#Granularité temporelle : Mois
#Unité : Nombre d'enfants
#Champ : France, régime général + régime agricole dans les Dom
#Zone géographique : Commune
#
#
#***********LIENS***********
#
#Retrouvez plus d'informations sur le site de la branche famille: http://www.caf.fr/
df = pd.read_csv('source/EnfantAgeCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Enfants_0_2_ans_2009', 
              'NB_Enfants_3_5_ans_2009', 'NB_Enfants_6_11_ans_2009',
              'NB_Enfants_12_15_ans_2009', 'NB_Enfants_16_17_ans_2009',
              'NB_Enfants_18_19_ans_2009', 'NB_Enfants_20_24_ans_2009',
              'NB_Enfants_2009']

files = glob.glob('source/EnfantAgeCom*')

# Warning no file for 2010, waiting fix from CAF

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
    # We have to add indicator to create unique feature name before merging
    if col not in ['Communes', 'Codes_Insee']:
        list_col.append(col+"_EAC") # EAC = EnfantAgeCom
    else:
        list_col.append(col)
df.columns = list_col

final_count = df.shape[0]

df.to_csv('data/full_EnfantAgeCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Enfants_0_2_ans_2009_EAC',
#       u'NB_Enfants_3_5_ans_2009_EAC', u'NB_Enfants_6_11_ans_2009_EAC',
#       u'NB_Enfants_12_15_ans_2009_EAC', u'NB_Enfants_16_17_ans_2009_EAC',
#       u'NB_Enfants_18_19_ans_2009_EAC', u'NB_Enfants_20_24_ans_2009_EAC',
#       u'NB_Enfants_2009_EAC', u'NB_Enfants_0_2_ans_2011_EAC',
#       u'NB_Enfants_3_5_ans_2011_EAC', u'NB_Enfants_6_11_ans_2011_EAC',
#       u'NB_Enfants_12_15_ans_2011_EAC', u'NB_Enfants_16_17_ans_2011_EAC',
#       u'NB_Enfants_18_19_ans_2011_EAC', u'NB_Enfants_20_24_ans_2011_EAC',
#       u'NB_Enfants_2011_EAC', u'NB_Enfants_0_2_ans_2012_EAC',
#       u'NB_Enfants_3_5_ans_2012_EAC', u'NB_Enfants_6_11_ans_2012_EAC',
#       u'NB_Enfants_12_15_ans_2012_EAC', u'NB_Enfants_16_17_ans_2012_EAC',
#       u'NB_Enfants_18_19_ans_2012_EAC', u'NB_Enfants_20_24_ans_2012_EAC',
#       u'NB_Enfants_2012_EAC', u'NB_Enfants_0_2_ans_2013_EAC',
#       u'NB_Enfants_3_5_ans_2013_EAC', u'NB_Enfants_6_11_ans_2013_EAC',
#       u'NB_Enfants_12_15_ans_2013_EAC', u'NB_Enfants_16_17_ans_2013_EAC',
#       u'NB_Enfants_18_19_ans_2013_EAC', u'NB_Enfants_20_24_ans_2013_EAC',
#       u'NB_Enfants_2013_EAC', u'NB_Enfants_0_2_ans_2014_EAC',
#       u'NB_Enfants_3_5_ans_2014_EAC', u'NB_Enfants_6_11_ans_2014_EAC',
#       u'NB_Enfants_12_15_ans_2014_EAC', u'NB_Enfants_16_17_ans_2014_EAC',
#       u'NB_Enfants_18_19_ans_2014_EAC', u'NB_Enfants_20_24_ans_2014_EAC',
#       u'NB_Enfants_2014_EAC'

