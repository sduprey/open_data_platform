# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable		Type	Label
#Communes		Char	NOM DE LA COMMUNE
#Codes_Insee		Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_Allocataires		Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
#NB_allocataire_RSA	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES RSA
#Dont_RSA_jeune		Num	NOMBRE DE FOYERS ALLOCATAIRES RSA JEUNE
#RSA_SOCLE_non_Majore	Num	NOMBRE DE FOYERS ALLOCATAIRES RSA SOCLE SANS MAJORATION VERSABLE
#RSA_SOCLE_Majore	Num	NOMBRE DE FOYERS ALLOCATAIRES RSA SOCLE AVEC MAJORATION VERSABLE
#RSA_activite		Num	NOMBRE DE FOYERS ALLOCATAIRES RSA ACTIVITE VERSABLE
#
#***********DESCRIPTION DE LA PRESTATION***********
#
#Le RSA est une prestation sous conditions de ressources versée mensuellement sur la base des ressources du trimestre précédent. Entré
#en vigueur le 1er juin 2009 en France métropolitaine et le 1er janvier 2011 dans les départements d’Outre-mer, cette prestation remplace
#le revenu minimum d'insertion (RMI) et l'allocation de parent isolé (API) pour les personnes privées d'emploi. Il apporte une incitation
#financière aux personnes sans ressource qui reprennent un emploi (le RSA garantit à quelqu'un qui reprend un travail que ses revenus augmentent).
#Enfin il complète les ressources des personnes dont l'activité professionnelle ne leur apporte que des revenus limités.
#
#Le RSA est versé sans limitation de durée, tant que les revenus du bénéficiaire sont inférieurs au montant maximal du RSA. Le montant versé
#peut varier si la situation familiale, professionnelle et les ressources du foyer évoluent. Le RSA est constitué de trois composantes : le
#"RSA socle", le "RSA socle et activité" et le "RSA activité". Ainsi, le RSA couvre une population large, puisqu’il concerne aussi bien des
#foyers n’ayant aucune ressource, que des personnes percevant des revenus d’activité proches du Smic. Un foyer allocataire du "RSA socle seul"
#n’a pas de revenus d’activité (toutefois, en cas de reprise d’activité, le bénéficiaire peut cumuler salaires et allocation pendant trois mois).
#Les bénéficiaires du "RSA socle et activité" ont de faibles revenus d’activité et l’ensemble de leurs ressources est inférieur au montant
#forfaitaire. Ceux du "RSA activité seul" ont de faibles revenus d’activité et l’ensemble de leurs ressources est supérieur au montant forfaitaire.
#Deux types de publics peuvent se combiner aux composantes de RSA :
#
#-les personnes en état de grossesse ou assumant seules la charge d’au moins un enfant bénéficient du "RSA majoré" (on parle alors de "socle majoré"
#ou "socle et activité majoré" ou "activité majoré")
#
#-les bénéficiaires du RSA ne faisant partie du public "RSA majoré" correspondent au RSA "non majoré". Au sein du public "non majoré" on peut
#distinguer le public "RSA jeune". Le public RSA jeune concerne les jeunes de moins de 25 ans isolés et sans enfant à charge et versé sous
#condition d’activité antérieure (deux ans au cours des trois dernières années).
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
#5)Dans les ressources associées à ce descriptif l'expression "RSA SOCLE" renvoi au "RSA socle seul" et au "RSA socle et activité" classique.
#
#
#***********Titres des fichiers***********
#
#RSA_Com_XXXX.csv
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
#Retrouvez plus d'informations sur le site de la branche famille: https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/solidarite-et-insertion/
#et sur le Cahier des données sociales : http://www.caf.fr/etudes-et-statistiques/publications/cahier-des-donnees-sociales
df = pd.read_csv('source/RSACom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_allocataires_2009', 
              'NB_allocataire_RSA_2009', 'Dont_RSA_jeune_2009',
              'RSA_SOCLE_non_Majore_2009', 'RSA_SOCLE_Majore_2009',
              'RSA_activite_2009']

files = glob.glob('source/RSACom*')

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
        list_col.append(col+"_RSAC") # RSAC = RSACom
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_RSACom.csv', encoding='utf-8', index=False)

## Features 
#u'NB_allocataires_2009_RSAC',
#       u'NB_allocataire_RSA_2009', u'Dont_RSA_jeune_2009',
#       u'RSA_SOCLE_non_Majore_2009', u'RSA_SOCLE_Majore_2009',
#       u'RSA_activite_2009', u'NB_allocataires_2010_RSAC',
#       u'NB_allocataire_RSA_2010', u'Dont_RSA_jeune_2010',
#       u'RSA_SOCLE_non_Majore_2010', u'RSA_SOCLE_Majore_2010',
#       u'RSA_activite_2010', u'NB_allocataires_2011_RSAC',
#       u'NB_allocataire_RSA_2011', u'Dont_RSA_jeune_2011',
#       u'RSA_SOCLE_non_Majore_2011', u'RSA_SOCLE_Majore_2011',
#       u'RSA_activite_2011', u'NB_allocataires_2012_RSAC',
#       u'NB_allocataire_RSA_2012', u'Dont_RSA_jeune_2012',
#       u'RSA_SOCLE_non_Majore_2012', u'RSA_SOCLE_Majore_2012',
#       u'RSA_activite_2012', u'NB_allocataires_2013_RSAC',
#       u'NB_allocataire_RSA_2013', u'Dont_RSA_jeune_2013',
#       u'RSA_SOCLE_non_Majore_2013', u'RSA_SOCLE_Majore_2013',
#       u'RSA_activite_2013', u'NB_allocataires_2014_RSAC',
#       u'NB_allocataire_RSA_2014', u'Dont_RSA_jeune_2014',
#       u'RSA_SOCLE_non_Majore_2014', u'RSA_SOCLE_Majore_2014',
#       u'RSA_activite_2014'

