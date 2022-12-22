##This script has been tested with Python version 3.8.15
import sys
print("Python version: ", sys.version)
print("Version info: ", sys.version_info)

import os
from os.path import join

#Update the path to where the data is stored.
dir_code = os.getcwd()
if dir_code.endswith('KinRDF'):
  dataFolder = dir_code + "/KineticsData"
else:
  parentPath = os.path.dirname(dir_code) #go up one directory
  dir_code = parentPath
  dataFolder = dir_code + "/KineticsData"
os.chdir(dataFolder) ##Update directory to folder with data
dir_code = os.getcwd()

##TODO:
#Build in check for empty values (especially for provenance).

#Regex to test for structure of content
import re

##Lists to store data in
ListTotal = []
ListSER_ID = []
ListEnzymePW = []
ListApprovedEnzymeName = []
ListEC_Number = []
ListUniprot = [] 
ListLinkUniprot = [] 
ListEnsembl = []
ListRheaID = []
ListLinkRheaID = [] 
ListSubstrate = []
ListSubstrateIDs = []
ListKm = []
ListKcat = []
ListKcatKm = []
List_pH = []
ListTemperature = []
ListAdditionalConditions = []
ListOrganism = []
ListPMID = []
ListDatabase = []
ListQC = []

##Read in files with kinetics data.
count = 0
countSER = 1
for (dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.txt') :
			count = count + 1
			thefile = os.path.join(dirname,filename)
			f = open(filename, "r")
			next(f)
			for line in f:
				SER_Name = "SER:" + str(countSER)
				ListTotal.append(SER_Name + '\t' + line.strip('\n'))
				countSER += 1

##SER_number
countSER = 0
for itemSERX in ListTotal:
	a = itemSERX.split('\t')
	pattern = '[a-zA-Z]+:[0-9]'
	result = re.match(pattern, a[0])
	pattern_chebi = '^(CHEBI:)?\\d+$'
	result_chebi =  re.match(pattern_chebi, a[7])
	pattern_uniprot = '^([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\\.\\d+)?|([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])$'
	result_uniprot = re.match(pattern_uniprot, a[4])
	pattern_rhea = '^(RHEA:)?\\d{5}$'
	result_rhea = re.match(pattern_rhea, a[6])
	if ('-' in a[0])|('-' in a[4])|('-' in a[6])|('-' in a[7]): #Check if one of the necessary values is missing!!
	  continue
	elif result: ##Create a unique IRI based on Substrate [7], Enzyme [4], and Reaction [6] ID. Note: if one of the three is missing, report in QC.
	  if (result_chebi is not None) & (result_uniprot is not None) & (result_rhea is not None): ##check against REGEX
	    #print(result_chebi + ' ' + result_uniprot + ' ' + result_rhea)
	    ListSER_ID.append(a[0].strip( ) + '\t' + 'dc:identifier' + ' ' + 'SER:'+ a[7].strip( ) + '-' + a[4].strip( ) + '-' + a[6].strip( )) ##Trim RHEA/CHEBI in fromt of IDs if available.
	    ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO:000028 ' + ' ' +  a[0].strip( ) + '_substrate' + ', '  + a[0].strip( )+ '_enzyme' + ', ' + a[0].strip( )+ '_reaction') #Add the 'has part' relationship, so we can link the IDs to that later.
	    ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO_000008 ' + ' ' +  a[0].strip( ) + '_measurement' ) #Add the 'has attribute' relationship, so we can link the values to that later.
	    countSER = countSER +1
	else:
		ListQC.append("CHECK: Data format for dc:identifier unknown, check original data for: "+ a[0] + '\n')

ListQC.append("Data format for SER correctly loaded for " + str(countSER) + " Substrate, Enzyme, and Reaction IDs. \n\n")  
			
##Define type, extension of WP vocabulary:		
for itemSERX in ListTotal:
	a = itemSERX.split('\t')
	pattern = '[a-zA-Z]+:[0-9]'
	result = re.match(pattern, a[0])
	if ('-' in a[0])|('-' in a[4])|('-' in a[6])|('-' in a[7]):
	  continue
	elif result:
	  ListSER_ID.append(a[0].strip( ) + '\t' + 'rdf:type ' + 'wp:InteractionData')
	else:
		print("CHECK: Data format for rdf:type IDs unknown, check original data for: " + a[0])

#LengthList = len(ListSER_ID)
		
# #Read in tsv file: [0]=ERPX_number [1]=EnzymePW, [2]=ApprovedEnzymeName, [3]=EC_Number, [4]=Uniprot , [5]=Ensembl, [6]=RheaID, [7]=CHEBIID, [8]=Km, [9]=Kcat, [10]=Kcat/Km, [11]=pH, [12]=Temperature, [13]=AdditionalConditions, [14]=Organism, [15]=PMID, [16]=Database				

##EnzymePW --> Add to enzyme_SER:X
for itemEnzymePW in ListTotal:
	b = itemEnzymePW.split('\t')
	if ('-' in b[0])|('-' in b[4])|('-' in b[6])|('-' in b[7]): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListEnzymePW.append(b[0].strip( ) + '\t' + 'rdfs:label' + ' "' + b[1].strip( ) + '"^^xsd:string')
#	for items in ListEnzymePW: 
#		if '-' in items:
#			ListEnzymePW.remove(items)				
			
###Ignore for now...
# ##[2]=ApprovedEnzymeName
# for itemApprovedEnzymeName in ListTotal:
	# c = itemApprovedEnzymeName.split('\t')
	# ListApprovedEnzymeName.append(b[0] + ' ' + 'rdfs:label' + ' ' + c[2])
	# for items in ListApprovedEnzymeName: 
		# if '-' in items:
			# ListApprovedEnzymeName.remove(items)
			
##EC_Number --> Add to enzyme_SER:X
countECs = 0
for itemEC_Number in ListTotal:
	d = itemEC_Number.split('\t')
	pattern = '^\\d+\\.-\\.-\\.-|\\d+\\.\\d+\\.-\\.-|\\d+\\.\\d+\\.\\d+\\.-|\\d+\\.\\d+\\.\\d+\\.(n)?\\d+$'
	result = re.match(pattern, d[3].strip())
	if ('-' in d[0])|('-' in d[4])|('-' in d[6])|('-' in d[7]): #Check if one of the necessary values is missing!!
	  continue
	elif result:
	  ListUniprot.append(d[0].strip( ) + '_enzyme'  + '\t' + 'wp:bdbEnzymeNomenclature' + ' ECcode:' + d[3].strip( ))
	  countECs = countECs + 1
	else:
	  ListQC.append("CHECK: Data format for 'wp:bdbEnzymeNomenclature unknown, check original data for: "+ d[0] + ' : ' + d[3]+ '\n')
    
ListQC.append("Data format for 'wp:bdbEnzymeNomenclature correctly loaded for " + str(countECs) + " EC IDs. \n\n")  
	
#	ListSubstrate.append(h[0].strip( ) + '_substrate' +'\t' + 'rdf:type' + ' ' + "wp:Metabolite")
#	ListSubstrateIDs.append(h[0].strip( ) + '_substrate' + "\t" + "wp:bdbChEBI " + 'CHEBI:' + h[7].strip( )+ '.')	
	
##Uniprot IRIs for WPRDF link && Uniprot interoperability IRIs --> Add to SER:X_enzyme
##Since this list will only include two statements, we can already add the ';' and '.' after the entries.
for itemUniprot in ListTotal:
	e = itemUniprot.split('\t')
	if ('-' in e[0])|('-' in e[4])|('-' in e[6])|('-' in e[7]): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListUniprot.append(e[0].strip( ) + '_enzyme' + '\t'  + 'rdf:type' + ' ' + "wp:Protein")
	  ##Wp IRIs: to be updated
	  ListUniprot.append(e[0].strip( ) + '_enzyme' + '\t' + 'wp:bdbUniprot' + ' uniprot:' + e[4].strip( ))
	  ##Uniprot IRIs for UniProt RDF link: "uniprotkb:P05067 a up:Protein ;"
	  ListLinkUniprot.append(e[0].strip( ) + '_enzyme' + '\t' + 'bioregistry:hasDbXref' + ' ' + 'uniprotkb:'  + e[4].strip() + '.' )	

##Ensembl --> Add to enzyme_SER:X
countGenes = 0
for itemEnsembl in ListTotal:
  f = itemEnsembl.split('\t')
  pattern = '^ENS[A-Z]*[FPTG]\\d{11}$' #Pattern is: ^ENS[A-Z]*[FPTG]\d{11}$' ; need to escape backslash! 
  result = re.match(pattern, f[5].strip( ) )
  if ('-' in f[0])|('-' in f[4])|('-' in f[6])|('-' in f[7])|('-' in f[5]): #Check if one of the necessary values is missing!!
    continue
  elif result: ##check against REGEX
    ListUniprot.append(f[0].strip( ) + '_enzyme' + '\t' + 'wp:bdbEnsembl' + ' En_id:' + f[5].strip( ))
    countGenes = countGenes + 1
  else:
    ListQC.append("CHECK: Data format for 'wp:bdbEnsembl unknown, check original data for: "+ f[0] + ' : ' + f[5]+ '\n')
    
ListQC.append("Data format for 'wp:bdbEnsembl correctly loaded for " + str(countGenes) + " gene IDs. \n\n")  
  
    
##Update interoperability with Rhea RDF:
#  ?rhea rdfs:subClassOf rh:Reaction .
#  ?rhea rh:id ?id .
#  ?rhea rh:accession ?accession .
#  ?rhea rh:equation ?equation .

# rhea: http://rdf.rhea-db.org/10000
# id: "10000"xsd:long
# accession: "RHEA:10000"xsd:string
# equation: "H2O + pentanamide = NH4(+) + pentanoate"xsd:string

##RheaID ##Check if rh:accession shouldn't be wp:bdbdRhea (since accession is used to levarage between reactionscheme and RheaID by RHEA RDF).
##--> Add to SER:X_reaction
for itemRheaID in ListTotal:
	g = itemRheaID.split('\t')
	if g[6].isnumeric(): #without prefix
	  ListRheaID.append(g[0].strip( ) + '\t' + 'wp:bdbRhea' + ' RHEA:' + g[6].strip( ) )
	  ListLinkRheaID.append('rh:' + g[6].strip( ) + '\t' + 'rdfs:subClassOf ' + 'rh:Reaction ; ')
	  ListLinkRheaID.append('rh:' + g[6].strip( ) + '\t' + 'wp:bdbRhea' + ' RHEA:' + g[6].strip( ) + '.' )	
	elif 'RHEA:' in g[6]: #with prefix
	  ListRheaID.append(g[0].strip( ) + '\t' + 'wp:bdbRhea' + ' RHEA:' + g[6].strip( ).replace("RHEA:", "") )
	  ListLinkRheaID.append('rh:' + g[6].strip( ).replace("RHEA:", "") + '\t' + 'rdfs:subClassOf ' + 'rh:Reaction ; ')
	  ListLinkRheaID.append('rh:' + g[6].strip( ).replace("RHEA:", "") + '\t' + 'wp:bdbRhea' + ' RHEA:' + g[6].strip( ).replace("RHEA:", "") + '.' )	
	  #ListRheaID.append(g[0].strip( ) + '\t' + 'rh:accession' + ' ' + g[6].strip( ))  #old
	else: #if no Rhea is available
	  ListRheaID.append(g[0].strip( ) + '\t' + 'rh:equation' + ' "' + g[6].strip( ) + '"^^xsd:string') ##Missing directional info!!
	for items in ListRheaID: 
		if '-' in items:
			ListRheaID.remove(items)
	for items in ListLinkRheaID: 
		if '-' in items:
			ListLinkRheaID.remove(items)	
			
			
##CHEBIID for substrate ##--> Add to SER:X_substrate
for itemSubstrate in ListTotal:
	h = itemSubstrate.split('\t')
	if ('-' in h[0])|('-' in h[4])|('-' in h[6])|('-' in h[7]): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListSubstrate.append(h[0].strip( ) + '_substrate' +'\t' + 'rdf:type' + ' ' + "wp:Metabolite")
	  ListSubstrateIDs.append(h[0].strip( ) + '_substrate' + "\t" + "wp:bdbChEBI" + ' ' + h[7].strip( )+ '.')

#Km##--> Add to measurement
for itemKm in ListTotal:
  i = itemKm.split('\t')
  ListKm.append(i[0].strip() + '\t' + 'SER:hasKm ' + ' "' + i[8].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q61751178'
  for items in ListKm: 
    if '-' in items:
      ListKm.remove(items)	
			
#Kcat ##--> Add to measurement
for itemKcat in ListTotal:
  i = itemKcat.split('\t')
  #ListKcat.append(i[0].strip( ) + '\t' + 'wd:Q883112' + ' ' + i[9].strip( )) #Old line.
  ListKcat.append(i[0].strip() + '\t' + 'SER:hasKcat ' + ' "' + i[9].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q883112'
  for items in ListKcat: 
    if '-' in items:
      ListKcat.remove(items)	

#KcatKm##--> Add to measurement
for itemKcatKm in ListTotal:
  i = itemKcatKm.split('\t')
  #ListKcatKm.append(i[0].strip( ) + '\t' + 'wd:Q7575016' + ' ' + i[10].strip( )) #Old line
  ListKcatKm.append(i[0].strip() + '\t' + 'SER:hasKmKcat' + ' "' + i[10].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q7575016
  for items in ListKcatKm: 
    if '-' in items:
      ListKcatKm.remove(items)				
			
#pH##--> Add to measurement
for item_pH in ListTotal:
  i = item_pH.split('\t')
  List_pH.append(i[0].strip( ) + '\t' + 'SER:hasPh'+ ' "' + i[11].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q40936
  for items in List_pH:
    if '-' in items:
      List_pH.remove(items)			
			
#Temperature##--> Add to measurement
for itemTemperature in ListTotal:
  i = itemTemperature.split('\t')
  ListTemperature.append(i[0].strip( ) + '\t' + 'wdt:P2076 ' + ' "' + i[12].strip( ) + '"^^xsd:float') #Line from after 2020-01-17
  for items in ListTemperature:
    if '-' in items in items:
      ListTemperature.remove(items)	

#AdditionalConditions##--> Add to measurement
for itemAdditionalConditions in ListTotal:
	i = itemAdditionalConditions.split('\t')
	ListAdditionalConditions.append(i[0].strip( ) + '\t' + 'dcterms:description' + ' "' + i[13].strip('"') + '"@en')
	for items in ListAdditionalConditions: 
		if '-' in items:
			ListAdditionalConditions.remove(items)			

#[14]=Organism			##--> Add to measurement
for itemOrganism in ListTotal:
	j = itemOrganism.split('\t')
	ListOrganism.append(j[0].strip( ) + '\t' + 'wp:organismName' + ' "' + j[14].strip('"') + '"^^xsd:string')
	for items in ListOrganism: 
		if '-' in items:
			ListOrganism.remove(items)	

#[15]=PMID	##--> Add to measurement	
for itemPMID in ListTotal:
	k = itemPMID.split('\t')
	if k[15].isnumeric():
	  ListPMID.append(k[0] + '\t' + 'dcterms:references' + " pubmed:" + k[15].strip( ))
	elif ';' in k[15]:
		k2 = k[15].split(';') ##Split multiple references in one line.
		k2 = [x.strip(' ') for x in k2]
		ListPMID.append(k[0].strip( ) + '\t' + 'dcterms:references' + " pubmed:" + ', '.join(k2))
	elif '-' in k[15]:
	  continue
	else:
		print("Data format for PubMed IDs unknown, check original data!")
	for items in ListPMID: 
		if '-' in items in items:
			ListPMID.remove(items)	
			
#[16]=Database ##--> Add to measurement				
for itemDatabase in ListTotal:
	l = itemDatabase.split('\t')
	ListDatabase.append(l[0].strip( ) + '\t' + 'dc:source' + ' "' + l[16].strip( ) + '"^^xsd:string')
	for items in ListDatabase: 
		if '-' in items:
			ListDatabase.remove(items)	

			
AllDict = {}			

##Connect all List data in a Dictionary
##All items are separated with ; (since each line has his own SER_ID.
for itemListSER in ListSER_ID:
	(key, val) = itemListSER.strip('\n').split('\t')
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

#for itemListEnsembl in ListEnsembl:
#	(key, val) = itemListEnsembl.strip('\n').split('\t')
#	AllDict.setdefault(key, [])
#	AllDict[key].append(val + ' ;')	

for itemListRheaID in ListRheaID:
	(key, val) = itemListRheaID.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		

for itemListSubstrate in ListSubstrate:
	(key, val) = itemListSubstrate.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')	

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

##Remove duplicates in ListLinkUniProt and ListLinkRheaID
unique_ListLinkUniprot = list(dict.fromkeys(ListLinkUniprot))
unique_ListLinkRheaID= list(dict.fromkeys(ListLinkRheaID))
unique_ListSubstrateIDs= list(dict.fromkeys(ListSubstrateIDs))
  
## Add UniProt proteins for interoperability:  
for itemListLinkedUniprot in unique_ListLinkUniprot:
	(key, val) = itemListLinkedUniprot.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val)
	
## Add Rhea interaction IDs for interoperability:  
for itemListLinkRheaID in unique_ListLinkRheaID:
	(key, val) = itemListLinkRheaID.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val)	
  
##Add ChEBI IDs for substrates ListSubstrateIDs  
for itemListSubstrateIDs in unique_ListSubstrateIDs:
	(key, val) = itemListSubstrateIDs.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val)	
  
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
RDF_Kin_data.write("@prefix SER: <http://vocabularies.wikipathways.org/kin#> . \n".encode())  #Need to make URL for this prefix!
RDF_Kin_data.write("@prefix dc: <http://purl.org/dc/elements/1.1/> . \n".encode()) 
RDF_Kin_data.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \n".encode()) 
RDF_Kin_data.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n".encode()) 
RDF_Kin_data.write("@prefix wp: <http://vocabularies.wikipathways.org/wp#> . \n".encode()) #From WikiPathways
RDF_Kin_data.write("@prefix rh: <http://rdf.rhea-db.org/> . \n".encode()) #From Rhea
#RDF_Kin_data.write("@prefix RHEA:   <https://www.rhea-db.org/reaction?id=> . \n".encode()) #For website link, not for IRI!
RDF_Kin_data.write("@prefix RHEA:   <https://identifiers.org/rhea/> . \n".encode()) #To link to WPRDF
RDF_Kin_data.write("@prefix dcterms: <http://purl.org/dc/terms/> . \n".encode()) 
RDF_Kin_data.write("@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> . \n".encode())
RDF_Kin_data.write("@prefix uniprot:   <https://identifiers.org/uniprot/> . \n".encode())
RDF_Kin_data.write("@prefix uniprotkb:   <http://purl.uniprot.org/uniprot/> . \n".encode())
RDF_Kin_data.write("@prefix up:   <http://purl.uniprot.org/core/> . \n".encode())
RDF_Kin_data.write("@prefix ECcode:   <https://identifiers.org/ec-code/> . \n".encode())
RDF_Kin_data.write("@prefix En_id:   <http://identifiers.org/ensembl/> . \n".encode())
RDF_Kin_data.write("@prefix pubmed:  <http://www.ncbi.nlm.nih.gov/pubmed/> . \n".encode()) #For WPRDF interoperability
RDF_Kin_data.write("@prefix wd: <http://www.wikidata.org/entity/> . \n".encode()) #From WikiData
RDF_Kin_data.write("@prefix wdt: <http://www.wikidata.org/prop/direct/> . \n".encode()) #From WikiData
RDF_Kin_data.write("@prefix sio: <http://semanticscience.org/resource/> . \n".encode()) #Semanticscience Integrated Ontology
RDF_Kin_data.write("@prefix bioregistry: <https://bioregistry.io/oboinowl:> . \n\n".encode()) #Bioregistry hasDbXref

# #Second, print the NEW prefixes (if needed)

#Third, print the dictionaries.
##ERPX_number			
for KeySERX, ValueSERX in AllDict.items():
	RDF_Kin_data.write(KeySERX.encode('utf-8') + "\n".encode())
	for item in ValueSERX:
		RDF_Kin_data.write("\t".encode() + item.encode('utf-8') + "\n".encode())
	RDF_Kin_data.write("\n".encode())	
# for i in range(LengthList):
     # RDF_Kin_data.write("This is line %d\r\n" % (i+1))

#Close this file as well
RDF_Kin_data.close()

# # Empty the QC file before writing new content:
open('QC_RDF_Kin_Data_2022-Dec.ttl', 'w').close()

# # open a file for writing:
RDF_Kin_data_QC = open('QC_RDF_Kin_Data_2022-Dec.ttl', 'wb')

##Write QC info to file:
if len(ListQC) >0:
  for item in ListQC:
    RDF_Kin_data_QC.write(item.encode())

#Close this file as well
RDF_Kin_data_QC.close()

# # Go back to parent folder before finishing the script:
dir_code = os.getcwd()
parentPath = os.path.dirname(dir_code) #go up one directory
dir_code = parentPath

#Remove all variables in working directory:
for element in dir():
    if element[0:2] != "__":
        del globals()[element]
del element
