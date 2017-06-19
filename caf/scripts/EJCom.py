# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable	Type	Label
#Communes	Char	NOM DE LA COMMUNE
#Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_Allocataires	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
#ALL_AF		Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC AF VERSABLE
#ALL_CF		Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC CF VERSABLE
#ALL_ARS		Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC ARS VERSABLE
#ALL_ASF		Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC ASF VERSABLE
#ALL_AEEH	Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC AEEH VERSABLE
#
#
#***********DESCRIPTION DES PRESTATIONS***********
#
#Créées dans leur forme actuelle en 1946, les allocations familiales (AF) sont versées aux familles d’au moins 2 enfants en Métropole
#et dès le premier enfant dans les Dom. Elles sont destinées aux enfants de moins de 20 ans à charge.
#
#Le complément familial (CF) est attribué en Métropole, aux familles d’au moins 3 enfants, âgés de 3 ans à moins de 21 ans. Dans les Dom,
#pour y avoir droit, la famille doit assumer la charge d’au moins un enfant de plus de 3 ans et de moins de 5 ans et ne pas avoir d’enfant
#de 0 à 3 ans. En Métropole comme dans les Dom, le Cf est soumis à condition de ressources. Il est non cumulable avec l’allocation de base
#de la Paje
#
#L’allocation de soutien familial (ASF) est versée sans condition de ressources pour élever un enfant de moins de 20 ans privé de l’aide
#de l’un ou de ses deux parents, ou pour aider les personnes qui ont la charge de l’éduquer. Sous une même appellation, elle concerne tout
#à la fois des enfants orphelins et ceux pour lesquels une pension alimentaire n’est pas versé
#
#L’allocation d’éducation de l’enfant handicapé (AEEH) s’adresse aux familles ayant à leur charge des enfants handicapés. Pour en bénéficier,
#l’enfant doit remplir plusieurs conditions :
#
#-être âgé de moins de 20 ans ;
#
#-avoir une incapacité permanente d’au moins 80 %. Celle-ci peut aussi être comprise entre 50 % et 80 % si l’enfant fréquente un établissement
#spécialisé ou si son état exige le recours à un service d’éducation spécialisée ou de soins à domicile ;
#
#-ne pas résider en internat avec prise en charge intégrale des frais de séjours par l’Assurance maladie, l’État ou l’Aide sociale.
#
#C’est la Commission des droits et de l’autonomie des personnes handicapées (Cdaph) qui apprécie l’état de santé de l’enfant et propose
#l’attribution de l’AEEH, pour une durée comprise entre 1 et 5 ans, sauf aggravation du taux d’incapacité.
#
#L’allocation de rentrée scolaire (ARS) aide les familles à assumer le coût de la rentrée scolaire de leurs enfants de 6 à 18 ans.
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
#***********Titres des fichiers***********
#
#EJ_Com_XXXX.csv
#où XXXX est l'année de référence
#
#***********Informations additionnelles***********
#
#Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)
#Fréquence de diffusion : Annuelle
#Granularité temporelle : Mois
#Unité : Nombre de foyers Allocataires
#Champ : France, régime général + régime agricole dans les Dom
#Zone géographique : Commune
#
#
#***********LIENS***********
#
#Retrouvez plus d'informations sur le site de la branche famille: https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/enfance-et-jeunesse
#et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales
df = pd.read_csv('source/EJCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_allocataires_2009', 
              'ALL_AF_2009', 'ALL_CF_2009',
              'ALL_ARS_2009', 'ALL_ASF_2009',
              'ALL_AEEH_2009']

files = glob.glob('source/EJCom*')

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
        list_col.append(col+"_EJC") # EJC = EJCom
    else:
        list_col.append(col)
df.columns = list_col

final_count = df.shape[0]

df.to_csv('data/full_EJCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_allocataires_2009_EJC',
#       u'ALL_AF_2009', u'ALL_CF_2009', u'ALL_ARS_2009', u'ALL_ASF_2009',
#       u'ALL_AEEH_2009', u'NB_Allocataires_2010_EJC', u'ALL_AF_2010',
#       u'ALL_CF_2010', u'ALL_ARS_2010', u'ALL_ASF_2010', u'ALL_AEEH_2010',
#       u'NB_Allocataires_2011_EJC', u'ALL_AF_2011', u'ALL_CF_2011',
#       u'ALL_ARS_2011', u'ALL_ASF_2011', u'ALL_AEEH_2011',
#       u'NB_Allocataires_2012_EJC', u'ALL_AF_2012', u'ALL_CF_2012',
#       u'ALL_ARS_2012', u'ALL_ASF_2012', u'ALL_AEEH_2012',
#       u'NB_Allocataires_2013_EJC', u'ALL_AF_2013', u'ALL_CF_2013',
#       u'ALL_ARS_2013', u'ALL_ASF_2013', u'ALL_AEEH_2013',
#       u'NB_Allocataires_2014_EJC', u'ALL_AF_2014', u'ALL_CF_2014',
#       u'ALL_ARS_2014', u'ALL_ASF_2014', u'ALL_AEEH_2014'

