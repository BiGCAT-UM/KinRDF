##This script has been tested with Python version 3.8.15
import sys
print("Python version: ", sys.version)
print("Version info: ", sys.version_info)

import os
from os.path import join

#Set Working directory to where this file is located:
#abspath = os.path.abspath("createRDFKinData.py")
#dname = os.path.dirname(abspath)
#os.chdir(dname)

#Update the path to where the data is stored.
dir_code = os.getcwd()
parentPath = os.path.dirname(dir_code) #go up one directory
dir_code = parentPath
dataFolder = dir_code + "/KineticsData"
os.chdir(dataFolder) ##Update directory to folder with data
dir_code = os.getcwd()

##TODO:
#Build in check for empty values (especially for provenance).
#Build queries to test for content (all number with point/decimal?) -> Jenkins

##Lists to store data in
ListTotal = []
ListSEP_ID = []
ListEnzymePW = []
ListApprovedEnzymeName = []
ListEC_Number = []
ListUniprot = [] 
ListEnsembl = []
ListRheaID = []
ListSubstrate = []
ListKm = []
ListKcat = []
ListKcatKm = []
List_pH = []
ListTemperature = []
ListAdditionalConditions = []
ListOrganism = []
ListPMID = []
ListDatabase = []

##Read in files with kinetics data.
count = 0
countSEP = 1
for (dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.txt') :
			count = count + 1
			thefile = os.path.join(dirname,filename)
			f = open(filename, "r")
			next(f)
			for line in f:
				SEP_Name = "SEP:" + str(countSEP)
				ListTotal.append(SEP_Name + '\t' + line.strip('\n'))
				countSEP += 1

##ERPX_number			
for itemSEPX in ListTotal:
	a = itemSEPX.split('\t')
	ListSEP_ID.append(a[0].strip( ) + '\t' + 'dc:identifier' + ' ' + a[0].strip( ))
	for items in ListSEP_ID: 
		if '-' in items:
			ListSEP_ID.remove(items)

#LengthList = len(ListSEP_ID)
		
# #Read in tsv file: [0]=ERPX_number [1]=EnzymePW, [2]=ApprovedEnzymeName, [3]=EC_Number, [4]=Uniprot , [5]=Ensembl, [6]=RheaID, [7]=CHEBIID, [8]=Km, [9]=Kcat, [10]=Kcat/Km, [11]=pH, [12]=Temperature, [13]=AdditionalConditions, [14]=Organism, [15]=PMID, [16]=Database				

##EnzymePW
for itemEnzymePW in ListTotal:
	b = itemEnzymePW.split('\t')
	ListEnzymePW.append(b[0].strip( ) + '\t' + 'rdfs:label' + ' "' + b[1].strip( ) + '"^^xsd:string')
	for items in ListEnzymePW: 
		if '-' in items:
			ListEnzymePW.remove(items)				
			
###Ignore for now...
# ##[2]=ApprovedEnzymeName
# for itemApprovedEnzymeName in ListTotal:
	# c = itemApprovedEnzymeName.split('\t')
	# ListApprovedEnzymeName.append(b[0] + ' ' + 'rdfs:label' + ' ' + c[2])
	# for items in ListApprovedEnzymeName: 
		# if '-' in items:
			# ListApprovedEnzymeName.remove(items)
			
##EC_Number
for itemEC_Number in ListTotal:
	d = itemEC_Number.split('\t')
	ListEC_Number.append(d[0].strip( ) + '\t' + 'wp:bdbEnzymeNomenclature' + ' ECcode:' + d[3].strip( ))
	for items in ListEC_Number: 
		if '-' in items:
			ListEC_Number.remove(items)				
	
##Uniprot
for itemUniprot in ListTotal:
	e = itemUniprot.split('\t')
	ListUniprot.append(e[0].strip( ) + '\t' + 'wp:bdbUniprot' + ' S_id:' + e[4].strip( ))
	for items in ListUniprot: 
		if '-' in items:
			ListUniprot.remove(items)				

##Ensembl
for itemEnsembl in ListTotal:
	f = itemEnsembl.split('\t')
	ListEnsembl.append(f[0].strip( ) + '\t' + 'wp:bdbEnsembl' + ' En_id:' + f[5].strip( ))
	for items in ListEnsembl: 
		if '-' in items:
			ListEnsembl.remove(items)			

##RheaID
for itemRheaID in ListTotal:
	g = itemRheaID.split('\t')
	if 'RHEA:' in g[6]:
		ListRheaID.append(g[0].strip( ) + '\t' + 'rh:accession' + ' ' + g[6].strip( ))  ##Check if rh:accession shouldn't be wp:bdbdRhea (since accession is used to levarage between reactionscheme and RheaID by RHEA RDF).
	else:
		ListRheaID.append(g[0].strip( ) + '\t' + 'rh:equation' + ' "' + g[6].strip( ) + '"^^xsd:string')
	for items in ListRheaID: 
		if '-' in items:
			ListRheaID.remove(items)	
			
			
##CHEBIID for substrate
for itemSubstrate in ListTotal:
	h = itemSubstrate.split('\t')
	ListSubstrate.append('CHEBI:' + h[7].strip( ) + ' ' + 'dcterms:isPartOf' + '\t' + h[0].strip( ))
	for items in ListSubstrate: 
		if '-' in items:
			ListSubstrate.remove(items)	

#Km
for itemKm in ListTotal:
  i = itemKm.split('\t')
  ListKm.append(i[0].strip( ) + '\t' + 'SEP:hasKm "' + ' ' + i[8].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q61751178'
  for items in ListKm: 
    if '-' in items:
      ListKm.remove(items)	
			
#Kcat
for itemKcat in ListTotal:
  i = itemKcat.split('\t')
  #ListKcat.append(i[0].strip( ) + '\t' + 'wd:Q883112' + ' ' + i[9].strip( )) #Old line.
  ListKcat.append(i[0].strip( ) + '\t' + 'SEP:hasKcat ' + ' "' + i[9].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q883112'
  for items in ListKcat: 
    if '-' in items:
      ListKcat.remove(items)	

#KcatKm
for itemKcatKm in ListTotal:
  i = itemKcatKm.split('\t')
  #ListKcatKm.append(i[0].strip( ) + '\t' + 'wd:Q7575016' + ' ' + i[10].strip( )) #Old line
  ListKcatKm.append(i[0].strip( ) + '\t' + 'SEP:hasKmKcat' + ' "' + i[10].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q7575016
  for items in ListKcatKm: 
    if '-' in items:
      ListKcatKm.remove(items)				
			
#pH
for item_pH in ListTotal:
  i = item_pH.split('\t')
  List_pH.append(i[0].strip( ) + '\t' + 'SEP:hasPh "'+ ' ' + i[11].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q40936
  for items in List_pH:
    if '-' in items:
      List_pH.remove(items)			
			
#Temperature
for itemTemperature in ListTotal:
  i = itemTemperature.split('\t')
  ListTemperature.append(i[0].strip( ) + '\t' + 'wdt:P2076' + ' ' + i[12].strip( ) + '^^xsd:float') #Line from after 2020-01-17
  for items in ListTemperature:
    if '-' in items or '' in items:
      ListTemperature.remove(items)	

#AdditionalConditions
for itemAdditionalConditions in ListTotal:
	i = itemAdditionalConditions.split('\t')
	ListAdditionalConditions.append(i[0].strip( ) + '\t' + 'dcterms:description' + ' "' + i[13].strip('"') + '"@en')
	for items in ListAdditionalConditions: 
		if '-' in items:
			ListAdditionalConditions.remove(items)			

#[14]=Organism			
for itemOrganism in ListTotal:
	j = itemOrganism.split('\t')
	ListOrganism.append(j[0].strip( ) + '\t' + 'wp:organismName' + ' "' + j[14].strip('"') + '"^^xsd:string')
	for items in ListOrganism: 
		if '-' in items:
			ListOrganism.remove(items)	

#[15]=PMID			
for itemPMID in ListTotal:
	k = itemPMID.split('\t')
	if '/' in k[15]:
		k2 = k[15].split('/')
		k2 = [x.strip(' ') for x in k2]
		ListPMID.append(k[0].strip( ) + '\t' + 'dcterms:references' + " PMID:" + ', PMID:'.join(k2))
	else:
		ListPMID.append(k[0].strip( ) + '\t' + 'dcterms:references' + " PMID:" + k[15].strip( ))
	for items in ListPMID: 
		if '-' in items or '' in items:
			ListPMID.remove(items)	
			
#[16]=Database				
for itemDatabase in ListTotal:
	l = itemDatabase.split('\t')
	ListDatabase.append(l[0].strip( ) + '\t' + 'dc:source' + ' "' + l[16].strip( ) + '"^^xsd:string')
	for items in ListDatabase: 
		if '-' in items:
			ListDatabase.remove(items)	

			
AllDict = {}			

##Connect all List data in a Dictionary
##All items are separated with ; (since each line has his own SEP_ID.
for itemListSEP in ListSEP_ID:
	(key, val) = itemListSEP.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')
	
for itemListEnzymePW in ListEnzymePW:
	(key, val) = itemListEnzymePW.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		
	
for itemListEC_Number in ListEC_Number:
	(key, val) = itemListEC_Number.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

for itemListUniprot in ListUniprot:
	(key, val) = itemListUniprot.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		

for itemListEnsembl in ListEnsembl:
	(key, val) = itemListEnsembl.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

for itemListRheaID in ListRheaID:
	(key, val) = itemListRheaID.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		

# for itemListSubstrate in ListSubstrate:
	# (key, val) = itemListSubstrate.strip('\n').split('\t')
	# AllDict.setdefault(key, [])
	# AllDict[key].append(val + ' ;')	

for itemListKm in ListKm:
	(key, val) = itemListKm.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		
	
for itemListKcat in ListKcat:
	(key, val) = itemListKcat.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

for itemListKcatKm in ListKcatKm:
	(key, val) = itemListKcatKm.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		
	
for itemList_pH in List_pH:
	(key, val) = itemList_pH.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')

for itemListTemperature in ListTemperature:
	(key, val) = itemListTemperature.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	
	
for itemListAdditionalConditions in ListAdditionalConditions:
	(key, val) = itemListAdditionalConditions.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

for itemListOrganism in ListOrganism:
	(key, val) = itemListOrganism.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

for itemListPMID in ListPMID:
	(key, val) = itemListPMID.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		
	
##Last item should end with a .
for itemListDatabase in ListDatabase:
  (key, val) = itemListDatabase.strip('\n').split('\t')
  AllDict.setdefault(key, [])
  AllDict[key].append(val + ' .')		
  
# # Go to output folder
dir_code = os.getcwd()
parentPath = os.path.dirname(dir_code) #go up one directory
outputFolder = parentPath + "/Output"
os.chdir(outputFolder) ##Update directory to folder to store output data
dir_code = os.getcwd()

# # Empty the data file before writing new content:
open('RDF_Kin_Data_2022-Dec.ttl', 'w').close()

# # open a file for writing:
RDF_Kin_data = open('RDF_Kin_Data_2022-Dec.ttl', 'wb')

# # Clean all content in the file
#TODO

# #First, print the prefixes from existing databases
##.encode() needed to write to files in Python 3.x (compared to 2.x)
RDF_Kin_data.write("@prefix SEP: <http://vocabularies.wikipathways.org/kin> . \n".encode())  #Need to make URL for this prefix!
RDF_Kin_data.write("@prefix dc: <http://purl.org/dc/elements/1.1/> . \n".encode()) 
RDF_Kin_data.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n".encode()) 
RDF_Kin_data.write("@prefix wp: <http://vocabularies.wikipathways.org/wp#> . \n".encode()) #From WikiPathways
RDF_Kin_data.write("@prefix rh: <http://rdf.rhea-db.org/> . \n".encode()) #From Rhea
RDF_Kin_data.write("@prefix dcterms: <http://purl.org/dc/terms/> . \n".encode()) 
RDF_Kin_data.write("@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> . \n".encode())
RDF_Kin_data.write("@prefix S_id:   <http://identifiers.org/uniprot/> . \n".encode())
RDF_Kin_data.write("@prefix ECcode:   <https://identifiers.org/ec-code/> . \n".encode())
RDF_Kin_data.write("@prefix En_id:   <http://identifiers.org/ensembl/> . \n".encode())
RDF_Kin_data.write("@prefix PMID:   <http://identifiers.org/pubmed/> . \n".encode())
RDF_Kin_data.write("@prefix RHEA:   <https://www.rhea-db.org/reaction?id=> . \n".encode())
RDF_Kin_data.write("@prefix wd: <http://www.wikidata.org/entity/> . \n".encode()) #From WikiData
RDF_Kin_data.write("@prefix wdt: <http://www.wikidata.org/prop/direct/> . \n\n".encode()) #From WikiData

# #Second, print the NEW prefixes (if needed)

#Third, print the dictionaries.
##ERPX_number			
for KeySEPX, ValueSEPX in AllDict.items():
	RDF_Kin_data.write(KeySEPX.encode('utf-8') + "\n".encode())
	for item in ValueSEPX:
		RDF_Kin_data.write("\t".encode() + item.encode('utf-8') + "\n".encode())
	RDF_Kin_data.write("\n".encode())	
# for i in range(LengthList):
     # RDF_Kin_data.write("This is line %d\r\n" % (i+1))

#Close this file as well
RDF_Kin_data.close()

# # Go back to parent folder before finishing the script:
dir_code = os.getcwd()
parentPath = os.path.dirname(dir_code) #go up one directory
dir_code = parentPath

#Remove all variables in working directory:
for element in dir():
    if element[0:2] != "__":
        del globals()[element]
del element
