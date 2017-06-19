# -*- coding: utf-8 -*-

import pandas as pd
import glob

#Variable	Type	Label
#Communes	Char	NOM DE LA COMMUNE
#Codes_Insee	Char	NUMERO DE LA COMMUNE, CODE INSEE
#NB_enfant_AEEH	Num	NOMBRE D'ENFANTS BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_0A2	Num	NOMBRE D'ENFANTS DE 0 A 2 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_3A5	Num	NOMBRE D'ENFANTS DE 3 A 5 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_6A11	Num	NOMBRE D'ENFANTS DE 6 A 11 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_12A15	Num	NOMBRE D'ENFANTS DE 12 A 15 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_16A17	Num	NOMBRE D'ENFANTS DE 16 A 17 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#AEEH_18A20	Num	NOMBRE D'ENFANTS DE 18 A 20 ANS, BENEFICIAIRES DE L'AEEH VERSABLE
#
#
#***********REMARQUES***********
#
#1) Le foyer allocataire est l�entit� administrative � laquelle les Caf versent au moins une prestation. Il est compos� de l�allocataire
#(personne qui per�oit au moins une prestation au regard de sa situation familiale et/ou mon�taire), de son conjoint/concubin/pacs�
#�ventuel, des enfants � charge et autres personnes � charge au sens de la r�glementation en vigueur. Un foyer allocataire peut donc
#comporter une ou plusieurs personnes.
#
#2) Le droit versable signifie que le foyer allocataire remplit toutes les conditions pour �tre effectivement pay� au titre du mois
#d�observation. En particulier ne sont pas inclus dans ce p�rim�tre les b�n�ficiaires qui n�ont pas fourni l�int�gralit� de leurs
#pi�ces justificatives, ou ceux dont le montant de la prestation est inf�rieur au seuil de versement.
#
#3) Le champ g�ographique d�observation du jeu de donn�es correspond � la commune de r�sidence du foyer allocataire telle qu�elle
#est enregistr�e dans le fichier statistique des allocataires extrait d�but d�ann�e N+1 et ce quelle que soit la Caf de gestion.
#La premi�re ligne du fichier dont le num�ro commune est XXXXX recouvre deux cas possibles soit un code commune inconnu soit une
#commune de r�sidence de l'allocataire � l'�tranger.
#A partir de 2014 les r�sidants � l'�tranger et les codes communes inconnus sont dissoci�s en deux lignes.
#
#4) L'application d'un blanc ' ' est d� � deux cas de figure soit l'information est manquante, soit il y a eu application d'un secret
#statistique. Le secret statistique est appliqu� � toutes les valeurs inf�rieures � 5. De plus, pour �viter de d�duire certaines
#valeurs manquantes d'autres valeurs par croisement (exemple, diff�rence avec la totalit� dans le cas d'une seule valeur manquante), un
#secret statistique est appliqu� sur d'autres valeurs.
#
#5)Un enfant a droit � l'AEEH s'il remplit les conditions suivantes:
#�tre �g� de moins de 20 ans ;
#� avoir une incapacit� permanente d�au moins 80 %.Celle-ci peut aussi �tre comprise entre 50 % et 80 %
#si l�enfant fr�quente un �tablissement sp�cialis� ou sison �tat exige le recours � un service d��ducation
#sp�cialis�e ou de soins � domicile ;
#
#� ne pas r�sider en internat avec prise en charge int�grale des frais de s�jours par l�Assurance maladie,
#l��tat ou l�Aide sociale. C�est la Commission des droits et de l�autonomie des personnes handicap�es (Cdaph)
#qui appr�cie l��tat de sant� de l�enfant et propose l�attribution de l�Aeeh, pour une dur�e comprise entre
#1 et 5 ans, sauf aggravation du taux d�incapacit�.
#
#7)L��ge retenu est l��ge atteint dans l�ann�e (ou �ge  par g�n�ration). Il correspond � la diff�rence entre l'ann�e d�observation et
#l'ann�e de naissance de l'individu. Les intervalles des tranches d'�ges sont des intervalles ferm�s.
#
#***********Titres des fichiers***********
#
#AEEH_Enf_Com_XXXX.csv
#o� XXXX est l'ann�e de r�f�rence
#
#***********Informations additionnelles***********
#
#Source : Cnaf, fichier FILEAS et BASE COMMUNALE ALLOCATAIRES (BCA)
#Fr�quence de diffusion : Annuelle
#Granularit� temporelle : Mois
#Unit� : Nombre d'enfants
#Champ : France, r�gime g�n�ral + r�gime agricole dans les Dom
#Zone g�ographique : Commune
#
#
#***********LIENS***********
#
#Retrouvez plus d'informations sur le site de la branche famille: http://www.caf.fr/

df = pd.read_csv('source/EnfantAEEH2009.csv', sep=";")

df.columns = ['Communes', 'Codes_Insee', 'NB_enfant_AEEH_2009']

files = glob.glob('source/EnfantAEEH*')

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
    if "nb_allocataires" in col.lower(): 
        list_col.append(col+"_AEEH") # AEEH = EnfantAEEH
    else:
        list_col.append(col)
df.columns = list_col

final_count = df.shape[0]

df.to_csv('data/full_EnfantAEEH.csv', encoding='utf-8', index=False)

## Features 
#u'NB_enfant_AEEH_2009',
#       u'NB_enfant_AEEH_2010', u'NB_enfant_AEEH_2011', u'AEEH_0A2_2011',
#       u'AEEH_3A5_2011', u'AEEH_6A11_2011', u'AEEH_12A15_2011',
#       u'AEEH_16A17_2011', u'AEEH_18A20_2011', u'NB_enfant_AEEH_2012',
#       u'AEEH_0A2_2012', u'AEEH_3A5_2012', u'AEEH_6A11_2012',
#       u'AEEH_12A15_2012', u'AEEH_16A17_2012', u'AEEH_18A20_2012',
#       u'NB_enfant_AEEH_2013', u'AEEH_0A2_2013', u'AEEH_3A5_2013',
#       u'AEEH_6A11_2013', u'AEEH_12A15_2013', u'AEEH_16A17_2013',
#       u'AEEH_18A20_2013', u'NB_enfant_AEEH_2014', u'AEEH_0A2_2014',
#       u'AEEH_3A5_2014', u'AEEH_6A11_2014', u'AEEH_12A15_2014',
#       u'AEEH_16A17_2014', u'AEEH_18A20_2014'

