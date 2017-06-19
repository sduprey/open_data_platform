# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable	Type	Label
#Communes	Char	NOM DE LA COMMUNE
#Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_enfant_ARS	Num	NOMBRE D'ENFANTS OUVRANT DROIT A L'ARS VERSABLE
#ARS_5A10	Num	NOMBRE D'ENFANTS DE 5 A 10 ANS, OUVRANT DROIT A L'ARS VERSABLE
#ARS_11A14	Num	NOMBRE D'ENFANTS DE 11 A 14 ANS, OUVRANT DROIT A L'ARS VERSABLE
#ARS_15A17	Num	NOMBRE D'ENFANTS DE 15 A 17 ANS, OUVRANT DROIT A L'ARS VERSABLE
#
#***********DESCRIPTION DE LA PRESTATION***********
#
#L'ARS est une prestation versée sous conditions de ressources en une seule fois (généralement en septembre) et les enfants ouvrant droit à l'ARS
#doivent être scolarisés et agés de 6 à 18 ans.
#
#***********REMARQUES***********
#
#1) Le foyer allocataire est l’entité administrative à laquelle les Caf versent au moins une prestation. Il est composé de l’allocataire
#(personne qui perçoit au moins une prestation au regard de sa situation familiale et/ou monétaire), de son conjoint/concubin/pacsé
#éventuel, des enfants à charge et autres personnes à charge au sens de la réglementation en vigueur. Un foyer allocataire peut donc
#comporter une ou plusieurs personnes.
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
#6)Attention : L'étude des droits à l'ARS est effectuée au moment du dépot de la demande au lieu de résidence du foyer, dans le cas de mutationn entre Caf
#du fait du déménagement du foyer allocataire, des éléments du dossier peuvent ne pas être connus par la Caf versant la prestation notamment l'âge des
#enfants, c'est pourquoi la somme des différentes tranches d'âge (ARS_5A10+ARS_11A14+ARS_15A17) peut être légèrement différente du total NB_enfant_ARS.
#
#***********Titres des fichiers***********
#
#ARS_Enf_Com_XXXX.csv
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
df = pd.read_csv('source/EnfantARS2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_enfant_ARS_2009', 
              'ARS_5A10_2009', 'ARS_11A14_2009',
              'ARS_15A17_2009']

files = glob.glob('source/EnfantARS*')

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
        list_col.append(col+"_ARS") # ARS = EnfantARS
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_EnfantARS.csv', encoding='utf-8', index=False)

## Features 
#NB_enfant_ARS_2009', u'ARS_5A10_2009',
#       u'ARS_11A14_2009', u'ARS_15A17_2009', u'NB_enfant_ARS_2010',
#       u'ARS_5A10_2010', u'ARS_11A14_2010', u'ARS_15A17_2010',
#       u'NB_enfant_ARS_2011', u'ARS_5A10_2011', u'ARS_11A14_2011',
#       u'ARS_15A17_2011', u'NB_enfant_ARS_2012', u'ARS_5A10_2012',
#       u'ARS_11A14_2012', u'ARS_15A17_2012', u'NB_enfant_ARS_2013',
#       u'ARS_5A10_2013', u'ARS_11A14_2013', u'ARS_15A17_2013',
#       u'NB_enfant_ARS_2014', u'ARS_5A10_2014', u'ARS_11A14_2014',
#       u'ARS_15A17_2014'

