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

#Regex to test for structure of content
import re

##Lists to store data in
ListTotal = []
ListSER_ID = []
ListSER_ID_type = []
ListUniprot = [] 
ListLinkUniprot = [] 
ListEnsembl = []
ListRheaID = []
ListRheaID_type = []
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
ListErrors = []

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
				

##Replace common prefixes for harmonized data structure:
ListTotal = [w.replace('RHEA:', '') for w in ListTotal]
ListTotal = [w.replace('CHEBI:', '') for w in ListTotal]

##Remove lines without ChEBI, UniProt, or Rhea
for item in ListTotal:
	a = item.split('\t')
	if (a[0]=='-')|(a[4]=='-')|(a[6]=='-')|(a[7]=='-')|(a[0]=='NA')|(a[4]=='NA')|( a[6]=='NA')|(a[7]=='NA'): #Check if one of the necessary values is missing!!
	  ListTotal.remove(item)

##Print total number of lines found in files:
ListQC.append("Total lines read: "+ str(len(ListTotal)) + '\n')

##Regex:
pattern_chebi = '^(CHEBI:)?\\d+$'
pattern_uniprot = '^([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\\.\\d+)?|([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])$'
pattern_rhea = '^(RHEA:)?\\d{5}$'

##SER_number
countSER = 0
for itemSERX in ListTotal:
	a = itemSERX.split('\t')
	pattern = '[a-zA-Z]+:[0-9]'
	result = re.match(pattern, a[0])
	result_chebi =  re.match(pattern_chebi, a[7].strip())
	result_uniprot = re.match(pattern_uniprot, a[4].strip())
	result_rhea = re.match(pattern_rhea, a[6].strip())
	if (result_chebi is not None) & (result_rhea is not None) & (result_uniprot is not None): ##check against REGEX
	  ListSER_ID.append(a[0].strip( ) + '\t' + 'dc:identifier' + ' ' + 'SER:'+ a[7].strip( ) + '-' + a[4].strip( ) + '-' + a[6].strip( )) ##Trim RHEA/CHEBI in fromt of IDs if available.
	  ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO_000028 ' + ' ' +  a[0].strip( ) + '_substrate' + ', '  + a[0].strip( )+ '_enzyme' + ', ' + a[0].strip( )+ '_reaction') #Add the 'has part' relationship, so we can link the IDs to that later.
	  ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO_000008 ' + ' ' +  a[0].strip( ) + '_measurement' ) #Add the 'has attribute' relationship, so we can link the values to that later.
	  countSER = countSER +1
	elif(result_chebi is not None) & (result_rhea is None)  & (result_uniprot is not None): ##check against REGEX; if RHEA is not available, use reaction formula
	  ListSER_ID.append(a[0].strip( ) + '\t' + 'dc:identifier' + ' ' + 'SER:'+ a[7].strip( ) + '-' + a[4].strip( ) + '-XXXXX')
	  ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO_000028 ' + ' ' +  a[0].strip( ) + '_substrate' + ', '  + a[0].strip( )+ '_enzyme' + ', ' + a[0].strip( )+ '_reaction')
	  ListSER_ID.append(a[0].strip() + '\t' + 'sio:SIO_000008 ' + ' ' +  a[0].strip( ) + '_measurement' ) #Add the 'has attribute' relationship, so we can link the values to that later.
	  #ListQC.append("CHECK: Data format for Rhea doesn't match regex, suspected to be rection formula, check data for: "+ a[0] + ' ' + a[6] + '\n')
	  countSER = countSER +1
	else:
	  ListTotal.remove(itemSERX)
	  ListErrors.append("CHECK: Data format for dc:identifier unknown, check original data for: "+ a[0] + '\n')


##Print total number of lines found in files, after removing data without SEP-ID:
ListQC.append("Lines remaining without missing SER info: "+ str(len(ListTotal)) + '\n')

##Print total number of SEP-IDs, for which measurements are available:
ListQC.append("Data format for SER correctly loaded for " + str(countSER) + " Substrate, Enzyme, and Reaction IDs. \n\n")  


#### [0]=ERPX_number [1]=EnzymePW, [2]=ApprovedEnzymeName, [3]=EC_Number, [4]=Uniprot , 
#### [5]=Ensembl, [6]=RheaID, [7]=CHEBIID, [8]=Km, [9]=Kcat, [10]=Kcat/Km, [11]=pH, [12]=Temperature, 
#### [13]=AdditionalConditions, [14]=Organism, [15]=PMID, [16]=Database				

##EnzymePW 
##No regex or count defined, since the names of Proteins can be very diverse!
for itemEnzymePW in ListTotal:
	b = itemEnzymePW.split('\t')
	if (b[1]=='-')|(b[1]=='NA')|(b[4]=='-')|(b[4]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListUniprot.append('uniprot:' + b[4].strip( ) + '\t' + 'rdfs:label' + ' "' + b[1].strip( ) + '"^^xsd:string')

###Approved Ennzyme names (added in spreadsheet for curation, not needed in RDF model)
# ##[2]=ApprovedEnzymeName
# for itemApprovedEnzymeName in ListTotal:
	# c = itemApprovedEnzymeName.split('\t')
	# ListApprovedEnzymeName.append(b[0] + ' ' + 'rdfs:label' + ' ' + c[2])
	# for items in ListApprovedEnzymeName: 
		# if '-' in items:
			# ListApprovedEnzymeName.remove(items)

			
##EC_Numbers
countECs = 0
for itemEC_Number in ListTotal:
	d = itemEC_Number.split('\t')
	pattern = '^\\d+\\.-\\.-\\.-|\\d+\\.\\d+\\.-\\.-|\\d+\\.\\d+\\.\\d+\\.-|\\d+\\.\\d+\\.\\d+\\.(n)?\\d+$'
	result = re.match(pattern, d[3].strip())
	if (d[3]=='-')|(d[4]=='-'): #Check if necessary value is missing!!
	  continue
	elif result:
	  ListUniprot.append('uniprot:' + d[4].strip( )  + '\t' + 'wp:bdbEnzymeNomenclature' + ' ECcode:' + d[3].strip( ))
	  countECs = countECs + 1
	else:
	  ListErrors.append("CHECK: Data format for 'wp:bdbEnzymeNomenclature unknown, check original data for: "+ d[0] + ' : ' + d[3]+ '\n')
    
ListQC.append("Data format for 'wp:bdbEnzymeNomenclature correctly loaded for " + str(countECs) + " EC IDs. \n\n")  
	

##Uniprot IDs
countProteins = 0
for itemUniprot in ListTotal:
	e = itemUniprot.split('\t')
	if(e[4]=='-'): #Check if necessary value is missing!!
	  continue
	else:
	  ListUniprot.append('uniprot:' + e[4].strip( ) + '\t'  + 'rdf:type' + ' ' + "wp:Protein")
	  ListUniprot.append('uniprot:' + e[4].strip( )  + '\t' + 'sio:SIO_000028' + ' ' + e[0].strip( ) + '_enzyme')
	  ##WP IRIs:
	  ListUniprot.append('uniprot:' + e[4].strip( )  + '\t' + 'wp:bdbUniprot' + ' uniprot:' + e[4].strip( )) 
	  ##Uniprot IRIs for UniProt RDF link: "uniprotkb:P05067 a up:Protein ;"
	  ListLinkUniprot.append('uniprot:' + e[4].strip( ) + '\t' + 'bioregistry:hasDbXref' + ' ' + 'uniprotkb:'  + e[4].strip() + '.' )
	  countProteins = countProteins + 1

##Print total number of Ensembl IDs:    
ListQC.append("Data format for wp:bdbUniprot correctly loaded for " + str(countProteins) + " UniProt Protein IDs. \n\n")  

##Ensembl IDs
countGenes = 0
for itemEnsembl in ListTotal:
  f = itemEnsembl.split('\t')
  pattern = '^ENS[A-Z]*[FPTG]\\d{11}$' #Pattern is: ^ENS[A-Z]*[FPTG]\d{11}$' ; need to escape backslash! 
  result = re.match(pattern, f[5].strip( ) )
  if (f[5]=='-')|(f[5]=='NA')|(f[4]=='-')|(f[4]=='NA'): #Check if one of the necessary values is missing!!
    continue
  elif result: ##check against REGEX
    ListUniprot.append('uniprot:' + f[4].strip( ) + '\t' + 'wp:bdbEnsembl' + ' En_id:' + f[5].strip( ))
    countGenes = countGenes + 1
  else:
    ListErrors.append("CHECK: Data format for wp:bdbEnsembl unknown, check original data for: "+ f[0] + ' : ' + f[5]+ '\n')

##Print total number of Ensembl IDs:    
ListQC.append("Data format for wp:bdbEnsembl correctly loaded for " + str(countGenes) + " gene IDs. \n\n")

##Define type, extension of WP vocabulary:		
#for itemSERX in ListTotal:
#	a = itemSERX.split('\t')
#	ListSER_ID_type.append(a[0].strip( ) + '\t' + 'rdf:type ' + 'wp:InteractionData')

##RHEA IDs
countRhea = 0
countEquation = 0
for itemRheaID in ListTotal:
	g = itemRheaID.split('\t')
	pattern_rhea = '^(RHEA:)?\\d{5}$'
	result_rhea = re.match(pattern_rhea, g[6].strip())
	if (g[6]=='-')|(g[6]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	elif(result_rhea): ##regex check
	  ListRheaID.append('RHEA:' + g[6].strip( ) + '\t' + 'wp:bdbRhea'  + ' RHEA:' + g[6].strip( ) ) 
	  ListRheaID.append('RHEA:' + g[6].strip( ) + '\t' + 'sio:SIO_000028'  + ' ' + g[0].strip( ) + '_reaction') 
	  ListLinkRheaID.append('RHEA:' + g[6].strip( ) + '\t' + 'rh::accession' + ' RHEA:' + g[6].strip( ) + '.' )	
	  ListRheaID_type.append(g[0].strip( ) + '\t' + 'rdf:type ' + 'wp:InteractionData') ##To make sure statement ends with type
	  countRhea = countRhea +1
	elif ('+' in g[6])&('=' in g[6]): #if no Rhea is available, but there is a reaction equation.
	  ListRheaID.append(g[0].strip( ) + '\t' + 'rh:equation' + ' "' + g[6].strip( ) + '"^^xsd:string') ##Missing directional info!!
	  ListRheaID_type.append(g[0].strip( ) + '\t' + 'rdf:type ' + 'wp:InteractionData') ##To make sure statement ends with type
	  countEquation = countEquation + 1   
	else: #if no Rhea is available
	  ListQC.append("CHECK: Data format for Rhea unknown, check original data for: "+ g[0] + ' : ' + g[6]+ '\n')

##Print total number of Ensembl IDs:    
ListQC.append("Data format for wp:bdbRhea correctly loaded for " + str(countRhea) + " rhea interaction IDs. \n\n")  
ListQC.append("Data format for rh:equation correctly loaded for " + str(countEquation) + " reaction formulas. \n\n")  


##CHEBI IDs
countSubstrates = 0
for itemSubstrate in ListTotal:
	h = itemSubstrate.split('\t')
	pattern_chebi = '^(CHEBI:)?\\d+$'
	result_chebi =  re.match(pattern_chebi, h[7])
	if (h[7]=='-')|(h[7]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	elif(result_chebi):
	  ListSubstrate.append('CHEBI:' + h[7].strip( ) +'\t' + 'sio:SIO_000028' + ' ' + h[0].strip())
	  ListSubstrateIDs.append('CHEBI:' + h[7].strip( ) + "\t" + "wp:bdbChEBI" + ' ' + h[7].strip( )+ '.')
	  countSubstrates = countSubstrates + 1
	else:
	  ListErrors.append("CHECK: Data format for CHEBI ID unknown, check original data for: "+ h[0] + " : " + h[7] + '\n')

ListQC.append("Data format for wp:bdbChEBI correctly loaded for " + str(countSubstrates) + " substrate IDs. \n\n")  

####No regex or count defined for the following items, since these can be very diverse.

##Regex:
pattern_float = '^\d+\.\d+$'

##Km
countKm = 0
for itemKm in ListTotal:
  i = itemKm.split('\t')
  i[8] = i[8].replace(',', '.')
  result_float =  re.match(pattern_float, i[8])
  if(i[8]=='-')|(i[8]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!! [16] = Database, needed for provenance and ending statement in RDF!
    continue
  elif(result_float): ##Check if entry contains a number with decimal(s)
    ListKm.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKm ' + ' "' + i[8].strip() + '"^^xsd:float')
    countKm = countKm + 1
  elif(i[8].strip().isnumeric()): ##Check if entry contains a number without decimal(s)
    ListKm.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKm ' + ' "' + i[8].strip() + '"^^xsd:float')
    countKm = countKm + 1
  else:
    ListErrors.append("CHECK: Data format for Km data not a number, check original data for: "+ h[0] + " : " + i[8] + '\n')
	  
ListQC.append("Data format for Km correctly loaded for " + str(countKm) + " values. \n\n")  


##Kcat
countKcat = 0
for itemKcat in ListTotal:
  i = itemKcat.split('\t')
  i[9] = i[9].replace(',', '.')
  result_float =  re.match(pattern_float, i[9])
  if(i[9]=='-')|(i[9]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!!
    continue
  elif(result_float):
    ListKcat.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKcat ' + ' "' + i[9].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q883112'
    countKcat = countKcat + 1
  elif(i[9].strip().isnumeric()):
    ListKcat.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKcat ' + ' "' + i[9].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q883112'
    countKcat = countKcat + 1
  else:
    ListErrors.append("CHECK: Data format for Kcat data not numeric, check original data for: "+ h[0] + " : " + i[9] + '\n')

ListQC.append("Data format for Kcat correctly loaded for " + str(countKcat) + " values. \n\n") 


#KcatKm
countKcatKm = 0
for itemKcatKm in ListTotal:
  i = itemKcatKm.split('\t')
  i[10] = i[10].replace(',', '.')
  result_float =  re.match(pattern_float, i[10])
  if(i[10]=='-')|(i[10]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!!
    continue
  elif(result_float):
    ListKcatKm.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKmKcat' + ' "' + i[10].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q7575016
    countKcatKm = countKcatKm + 1	
  elif(i[10].strip().isnumeric()):
    ListKcatKm.append(i[0].strip() + '_measurement' + '\t' + 'SER:hasKmKcat' + ' "' + i[10].strip() + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q7575016
    countKcatKm = countKcatKm + 1	
  else:
    ListErrors.append("CHECK: Data format for KcatKm data not numeric, check original data for: "+ h[0] + " : " + i[10] + '\n')


ListQC.append("Data format for KcatKm correctly loaded for " + str(countKcatKm) + " values. \n\n") 

			
#pH##--> Add to measurement
for item_pH in ListTotal:
  i = item_pH.split('\t')
  if(i[11]=='-')|(i[11]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!!
    continue
  else:
    List_pH.append(i[0].strip( ) + '_measurement' + '\t' + 'SER:hasPh'+ ' "' + i[11].strip( ) + '"^^xsd:float') #Line from after 2020-01-17 ##wd:Q40936

			
#Temperature##--> Add to measurement
for itemTemperature in ListTotal:
  i = itemTemperature.split('\t')
  if(i[12]=='-')|(i[12]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!!
    continue
  else:
    ListTemperature.append(i[0].strip( ) + '_measurement' + '\t' + 'wdt:P2076 ' + ' "' + i[12].strip( ) + '"^^xsd:float') #Line from after 2020-01-17


#AdditionalConditions##--> Add to measurement
for itemAdditionalConditions in ListTotal:
	i = itemAdditionalConditions.split('\t')
	if(i[13]=='-')|(i[13]=='NA')|(i[16]=='-')|(i[16]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListAdditionalConditions.append(i[0].strip( )  + '_measurement' + '\t' + 'dcterms:description' + ' "' + i[13].strip('"') + '"@en')

##Create a list to check listed organism (Latin and common English names) for vertebrates:
ListCommonLatinOrganismsWP = ['Bos taurus', 'Canis familiaris', 'Danio rerio', 'Equus caballus', 'Gallus gallus', 'Homo sapiens', 'Mus musculus', 'Pan troglodytes', 'Rattus norvegicus', 'Sus scrofa']
ListCommonEnglishOrganismsWP = ['Cow', 'Dog', 'Zebrafish', 'Horse', 'Chicken', 'Human', 'Mouse', 'Chimpanzee', 'Rat', 'Boar']

##TODO: if English name, change to Latin for data model.
##TODO: report names which are not known/incorrect; examples:
#Alcaligenes sp. 


#[14]=Organism			##--> Add to measurement
for itemOrganism in ListTotal:
	j = itemOrganism.split('\t')
	if(j[14]=='-')|(j[14]=='NA')|(j[16]=='-')|(j[16]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	elif(i[14].isalpha()):
	  if(i[14] in ListCommonLatinOrganismsWP)| i[14] in ListCommonEnglishOrganismsWPOrganismsWP):
	    ListOrganism.append(j[0].strip( ) + '_measurement'  + '\t' + 'wp:organismName' + ' "' + j[14].strip('"') + '"^^xsd:string')
	else:
	  ListErrors.append("CHECK: Data format for Organism name is not recognized, check original data for: "+ j[0] + " : " + j[14] + '\n')


#[15]=PMID	##--> Add to measurement	
for itemPMID in ListTotal:
	k = itemPMID.split('\t')
	if(k[15]=='-')|(k[15]=='NA')|(k[16]=='-')|(k[16]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	if k[15].isnumeric():
	  ListPMID.append(k[0].strip( ) + '_measurement' + '\t' + 'dcterms:references' + " pubmed:" + k[15].strip( ))
	elif ';' in k[15]:
		k2 = k[15].split(';') ##Split multiple references in one line.
		k2 = [x.strip(' ') for x in k2]
		ListPMID.append(k[0].strip( ) + '_measurement' + '\t' + 'dcterms:references' + " pubmed:" + ', '.join(k2))
	else:
		print("Data format for PubMed IDs unknown, check original data for: " + k[0] + ' : ' + k[15])

			
#[16]=Database ##--> Add to measurement				
for itemDatabase in ListTotal:
	l = itemDatabase.split('\t')
	if(l[16]=='-')|(l[16]=='NA'): #Check if one of the necessary values is missing!!
	  continue
	else:
	  ListDatabase.append(l[0].strip( ) + '_measurement' + '\t' + 'dc:source' + ' "' + l[16].strip( ) + '"^^xsd:string')

AllDict = {}			

##Connect all List data in a Dictionary
##All items are separated with ; (since each line has his own SER_ID.
for itemListSER in ListSER_ID:
	(key, val) = itemListSER.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')

##Finalize statements with type info (if Rhea ID exists):	
for itemListSERtype in ListSER_ID_type:
	(key, val) = itemListSERtype.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' .')	
	
unique_ListUniprot = list(dict.fromkeys(ListUniprot))

for itemListUniprot in unique_ListUniprot:
	(key, val) = itemListUniprot.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		

#Remove duplicates
unique_ListRheaID = list(dict.fromkeys(ListRheaID))

for itemListRheaID in unique_ListRheaID:
	(key, val) = itemListRheaID.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' ;')		
	
##Finalize statements with type info (without Rhea ID, with equation):	
for itemListRheatype in ListRheaID_type:
	(key, val) = itemListRheatype.strip('\n').split('\t')
	AllDict.setdefault(key, [])
	AllDict[key].append(val + ' .')		

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

##Remove duplicates for linked lists:
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
RDF_Kin_data.write("@prefix CHEBI:   <http://purl.obolibrary.org/obo/CHEBI_> . \n".encode()) #To link to Rhea RDF
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

RDF_Kin_data_QC.write("\nReported Errors in Data: \n\n".encode())

##Write Error info to file:
if len(ListErrors) >0:
  for item in ListErrors:
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
