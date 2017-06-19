# -*- coding: utf-8 -*-

import pandas as pd
import glob
#Variable	Type	Label
#Communes	Char	NOM DE LA COMMUNE
#Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_Allocataires	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
#ALL_AAH		Num	NOMBRE D'ALLOCATAIRES AVEC AAH VERSABLE
#
#***********DESCRIPTION DE LA PRESTATION***********
#
#L’AAH est une prestation versée sous conditions de ressources et résulte de la loi d’orientation du 30 juin 1975 relative aux personnes
#handicapées. L’AAH permet de garantir un revenu minimal à un adulte handicapé Depuis 2011, le montant de l’allocation aux adultes handicapés
#(AAH) est calculé par trimestre lorsque la personne exerce une activité en milieu ordinaire. Dans les autres cas la déclaration des ressources
#est annuelle. Les modalités de cumul de la prestation avec les revenus d’activité ont également évolué. Ainsi, une personne seule peut
#désormais percevoir de l’AAH si ses revenus d’activité sont inférieurs à 1,4 fois le montant du Smic.
#
#Pour bénéficier l’AAH la personne doit avoir au moins 20 ans et un taux de handicap d’au moins 80%. Cependant, les personnes ayant un taux de
#handicap compris entre 50% et 80% peuvent y avoir droit si elles sont âgées de moins de 60 ans, n’ont pas travaillé depuis au moins un an et
#si leur handicap constitue un frein à l’accès à l’emploi. Dans tous les cas, l’éventuel bénéficiaire de l’Aah ne doit pas recevoir de pension
#ou de rente d’accident du travail supérieure à un certain montant.
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
#5)L'AAH est une prestation individualisée, dans un même foyer allocataire, il peut donc y avoir plusieurs bénéficiaires de l'AAH.
#
#***********Titres des fichiers***********
#
#AAH_Com_XXXX.csv
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
df = pd.read_csv('source/AAHCom2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'ALL_AAH_2009']

files = glob.glob('source/AAHCom*')

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
        list_col.append(col+"_AAHC") # AAHC = AAHCom
    else:
        list_col.append(col)
df.columns = list_col


df.to_csv('data/full_AAHCom.csv', encoding='utf-8', index=False)

## Features 
# u'NB_Allocataires_2009_AAHC',
#       u'ALL_AAH_2009', u'NB_Allocataires_2010_AAHC', u'ALL_AAH_2010',
#       u'NB_Allocataires_2011_AAHC', u'ALL_AAH_2011',
#       u'NB_allocataires_2012_AAHC', u'ALL_AAH_2012',
#       u'NB_allocataires_2013_AAHC', u'ALL_AAH_2013',
#       u'NB_Allocataires_2014_AAHC', u'ALL_AAH_2014'