# -*- coding: utf-8 -*-

import pandas as pd
import glob

# Variable	Type	Label
# Communes	Char	NOM DE LA COMMUNE
# Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
# NB_Allocataires	Num	NOMBRE TOTAL DE FOYERS ALLOCATAIRES DE LA BRANCHE FAMILLE
# COUP_0_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES COUPLES SANS ENFANT
# COUP_1_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES COUPLES AVEC 1 ENFANT
# COUP_2_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES COUPLES AVEC 2 ENFANTS
# COUP_3_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES COUPLES AVEC 3 ENFANTS
# COUP_4plus_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES COUPLES AVEC 4 A X ENFANTS
# Homme_Isole	Num	NOMBRE DE FOYERS ALLOCATAIRES MESSIEURS ISOLES
# Femme_Isolee	Num	NOMBRE DE FOYERS ALLOCATAIRES MESDAMES ISOLEES
# MONO_1_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES MONOPARENTS AVEC 1 ENFANT
# MONO_2_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES MONOPARENTS AVEC 2 ENFANTS
# MONO_3_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES MONOPARENTS AVEC 3 ENFANTS
# MONO_4plus_ENF	Num	NOMBRE DE FOYERS ALLOCATAIRES MONOPARENTS AVEC 4 A X ENFANTS
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
# 5)Les notions de couples, de familles monoparentales et de personnes isolées sont établies au sens de la législation familiale.
#
# 6)La notion d'enfant dans ce jeu de données renvoit à la notion d'enfant à charge au sens de la législation familiale.
# Pour avoir la charge d’un enfant, l’allocataire doit assurer financièrement son entretien de manière effective et permanente
# et assumer à son égard la responsabilité affective et éducative, sans obligation de lien de parenté avec l’enfant. On
# distingue deux notions d’enfant à charge dans la législation :
#
# • enfant à charge au sens des prestations familiales (Pf) :
# un enfant est reconnu à charge s’il est âgé d’un mois à moins
# de 20 ans quelle que soit sa situation, dès lors que son salaire
# net mensuel ne dépasse pas 55 % du Smic brut ;
#
# •enfant à charge au sens de la législation familiale:
# en plus des enfants à charge au sens des Pf, sont également considérés à charge
# pour les aides au logement, les enfants âgés de moins de 21 ans en Métropole (22 ans dans les Dom), les enfants âgés de 20 à
# 25 ans pour le calcul du Rmi/Rsa, et dès le mois de leur naissance, les enfants bénéficiaires de l’allocation de base de la Paje.
#
# ***********Titres des fichiers***********
#
# Alloc_Config_Com_XXXX.csv
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

df = pd.read_csv('source/ConfigFamiliale2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_Allocataires_2009', 
              'COUP_0_ENF_2009', 'COUP_1_ENF_2009', 'COUP_2_ENF_2009', 'COUP_3_ENF_2009', 'COUP_4plus_ENF_2009',
              'Homme_Isole_2009', 'Femme_Isolee_2009', 'MONO_1_ENF_2009', 'MONO_2_ENF_2009',
              'MONO_3_ENF_2009', 'MONO_4plus_ENF_2009']

files = glob.glob('source/ConfigFamiliale*')

for path_file in files:
    year = str(path_file[-8:-4])
    if (year != '2009'):
        df_temp = pd.read_csv(path_file, sep=';')
        
        # Rename Col with year
        year_col = ['Communes', 'Codes_Insee']
        features_col = []
        for col in df_temp.columns[-12:]:
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
        list_col.append(col+"_CF") # CF = ConfigFamiliale
    else:
        list_col.append(col)
df.columns = list_col

df.to_csv('data/full_ConfigFamiliale.csv', encoding='utf-8', index=False)

## Features 
#u'NB_Allocataires_2009_CF',
#       u'COUP_0_ENF_2009', u'COUP_1_ENF_2009', u'COUP_2_ENF_2009',
#       u'COUP_3_ENF_2009', u'COUP_4plus_ENF_2009', u'Homme_Isole_2009',
#       u'Femme_Isolee_2009', u'MONO_1_ENF_2009', u'MONO_2_ENF_2009',
#       u'MONO_3_ENF_2009', u'MONO_4plus_ENF_2009', u'NB_allocataires_2010_CF',
#       u'COUP_0_ENF_2010', u'COUP_1_ENF_2010', u'COUP_2_ENF_2010',
#       u'COUP_3_ENF_2010', u'COUP_4plus_ENF_2010', u'Homme_Isole_2010',
#       u'Femme_Isolee_2010', u'MONO_1_ENF_2010', u'MONO_2_ENF_2010',
#       u'MONO_3_ENF_2010', u'MONO_4plus_ENF_2010', u'NB_allocataires_2011_CF',
#       u'COUP_0_ENF_2011', u'COUP_1_ENF_2011', u'COUP_2_ENF_2011',
#       u'COUP_3_ENF_2011', u'COUP_4plus_ENF_2011', u'Homme_Isole_2011',
#       u'Femme_Isolee_2011', u'MONO_1_ENF_2011', u'MONO_2_ENF_2011',
#       u'MONO_3_ENF_2011', u'MONO_4plus_ENF_2011', u'NB_allocataires_2012_CF',
#       u'COUP_0_ENF_2012', u'COUP_1_ENF_2012', u'COUP_2_ENF_2012',
#       u'COUP_3_ENF_2012', u'COUP_4plus_ENF_2012', u'Homme_Isole_2012',
#       u'Femme_Isolee_2012', u'MONO_1_ENF_2012', u'MONO_2_ENF_2012',
#       u'MONO_3_ENF_2012', u'MONO_4plus_ENF_2012', u'NB_allocataires_2013_CF',
#       u'COUP_0_ENF_2013', u'COUP_1_ENF_2013', u'COUP_2_ENF_2013',
#       u'COUP_3_ENF_2013', u'COUP_4plus_ENF_2013', u'Homme_Isole_2013',
#       u'Femme_Isolee_2013', u'MONO_1_ENF_2013', u'MONO_2_ENF_2013',
#       u'MONO_3_ENF_2013', u'MONO_4plus_ENF_2013', u'NB_allocataires_2014_CF',
#       u'COUP_0_ENF_2014', u'COUP_1_ENF_2014', u'COUP_2_ENF_2014',
#       u'COUP_3_ENF_2014', u'COUP_4plus_ENF_2014', u'Homme_Isole_2014',
#       u'Femme_Isolee_2014', u'MONO_1_ENF_2014', u'MONO_2_ENF_2014',
#       u'MONO_3_ENF_2014', u'MONO_4plus_ENF_2014'

