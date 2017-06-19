# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable	Type	Label
#Communes	Char	NOM DE LA COMMUNE
#Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_Allocataires	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
#ALL_PAJE	Num	NOMBRE DE FOYERS ALLOCATAIRES PAJE VERSABLE
#ALL_PRIM	Num	NOMBRE DE FOYERS ALLOCATAIRES PRIME NAISSANCE OU ADOPTION VERSEES
#ALL_BASEP	Num	NOMBRE DE FOYERS ALLOCATAIRES AVEC DROIT BASE PAJE VERSABLE
#ALL_CMG		Num	NOMBRE DE FOYERS ALLOCATAIRES CMG VERSABLE
#ALL_CMG_ASMA	Num	NOMBRE DE FOYERS ALLOCATAIRES CMG ASSISTANTE MATERNELLE VERSABLE
#ALL_CMG_DOM 	Num	NOMBRE DE FOYERS ALLOCATAIRES CMG GARDE A DOMICILE VERSABLE
#ALL_CMG_A 	Num	NOMBRE DE FOYERS ALLOCATAIRES CMG STRUCTURE (ENTREPRISE OU ASSOCIATION) VERSABLE
#ALL_Clca	Num	NOMBRE DE FOYERS ALLOCATAIRES CLCA VERSABLE
#
#
#***********DESCRIPTION DES PRESTATIONS***********
#
#La prestation d'accueil du jeune enfant (Paje) est versée pour un enfant né ou adopté, elle comprend quatre composantes :
#
#-la prime à la naissance et/ou à l’adoption (sous conditions de ressources);
#
#-l’allocation de base (sous conditions de ressources) pour les enfants de moins de 3 ans (ou moins de 20 ans pour des enfants adoptés) ;
#
#-le complément de libre choix d’activité (CLCA) pour toute naissance ou adoption avant le 1er janvier 2015 (si vous avez cessé ou réduit
#votre activité professionnelle pour élever votre ou vos enfant(s)) de moins de 3 ans( ou moins de 20 ans dans le cas d’adoption), puis la
#prestation partagée d’accueil d’éducation de l’enfant (PreParE) pour toute naissance ou adoption après le 31 décembre 2014 ) ;
#
#-le complément de libre choix de mode de garde (CMG), lorsque le(s) enfant(s) de moins de 6 ans sont gardés par une assistante maternelle
#agréée, par une garde à domicile, par une association ou entreprise habilitée ou par une micro-crèche
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
#5)Les colonnes ALL_CMG_ASMA ALL_CMG_A ALL_CMG_DOM et ALL_CMG sont extraites au titre du mois novembre. C'est une exception dû à des contraintes techniques.
#
#***********Titres des fichiers***********
#
#PAJE_Com_XXXX.csv
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
#Retrouvez plus d'informations sur le site de la branche famille: https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance
#et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales
df = pd.read_csv('source/PajeCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'ALL_PAJE_2009', 'ALL_PRIM_2009', 'ALL_BASEP_2009',
              'ALL_ASMA_2009','ALL_Clca_Colca_2009']

files = glob.glob('source/PajeCom*')

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
        list_col.append(col+"_PC") # PC = PageCom
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_PageCom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Allocataires_2009_PC',
#       u'ALL_PAJE_2009', u'ALL_PRIM_2009', u'ALL_BASEP_2009', u'ALL_ASMA_2009',
#       u'ALL_Clca_Colca_2009', u'NB_Allocataires_2010_PC', u'ALL_PAJE_2010',
#       u'ALL_PRIM_2010', u'ALL_BASEP_2010', u'ALL_ASMA_2010',
#       u'ALL_Clca_Colca_2010', u'NB_Allocataires_2011_PC', u'ALL_PAJE_2011',
#       u'ALL_PRIM_2011', u'ALL_BASEP_2011', u'ALL_ASMA_2011',
#       u'ALL_Clca_Colca_2011', u'NB_Allocataires_2012_PC', u'ALL_PAJE_2012',
#       u'ALL_PRIM_2012', u'ALL_BASEP_2012', u'ALL_ASMA_2012',
#       u'ALL_Clca_Colca_2012', u'NB_Allocataires_2013_PC', u'ALL_PAJE_2013',
#       u'ALL_PRIM_2013', u'ALL_BASEP_2013', u'ALL_ASMA_2013',
#       u'ALL_Clca_Colca_2013', u'NB_Allocataires_2014_PC', u'ALL_PAJE_2014',
#       u'ALL_PRIM_2014', u'ALL_BASEP_2014', u'ALL_CMG_2014',
#       u'ALL_CMG_ASMA_2014', u'ALL_CMG_DOM_2014', u'ALL_CMG_A_2014',
#       u'ALL_Clca_Colca_2014', u'NB_Allocataires_2015_PC', u'ALL_PAJE_2015',
#       u'ALL_PRIM_2015', u'ALL_BASEP_2015', u'ALL_ASMA_2015',
#       u'ALL_Clca_Colca_2015'