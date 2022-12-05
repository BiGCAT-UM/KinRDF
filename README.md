# KinRDF
Conversion of kinetic data to an RDF model, compatible with WikiPathways PathWayModels.

Setup this project in Rstudio:
```cmd
###Install Python on your local machine to run this script:
### See https://support.posit.co/hc/en-us/articles/360023654474-Installing-and-Configuring-Python-with-RStudio
##Update PIP (package manager for Python packages/modules):
sudo pip install --upgrade pip
##Add virtual environment package:
sudo pip install virtualenv
##Move to correct project directory (in this case, the GitHub folder calles KinRDF)
cd /home/../KinRDF
##Create a new virtual environment in a folder called my_env:
sudo virtualenv my_env
##Activate the virtual environment:
source my_env/bin/activate
##Check if python is activated:
which python
##Check version of Python
python3 --version
```

Run the RDF locally (with Virtuoso Docker, on Linux):
Documentation curtosy of Marvin Martens [https://github.com/marvinm2/AOPWikiRDF]

## Set up a Virtuoso SPARQL endpoint with AOP-Wiki RDF (on linux):

### Step 1 - Create folder to mount
Open the terminal and create a local folder to map to the docker container. Note the path to the folder to enter it at step 3. In this example, the folder '/kinRdf' was created and entered it by using:
```
mkdir -p kinRdf
```

### Step 2 - Move the RDF (.ttl) files into the newly created folder
```
cp Output/RDF_Kin_Data_2022-Dec.ttl kinRdf/KINRDF.ttl
```

### Step 3 - Run the Docker image
Be sure to use ports 8890:8890 and 1111:1111. In this case, the container was named "KinRDF". Also, this step configures the mapped local folder with the data, which is in this example "/kinRdf". The Docker image used is openlink/virtuoso-opensource-7. Run the Docker image by entering:
```
sudo docker run -d --env DBA_PASSWORD=dba -p 8890:8890 -p 1111:1111 --name KinRDF --volume `pwd`/kinRdf/:/database/data/  openlink/virtuoso-opensource-7
```

### Step 4 - Enter the running container
The SPARQL endpoint should already be accessible through [localhost:8890/sparql/](http://localhost:8890/sparql/). However, while the Docker image is running, the data is not yet loaded. Therefore you need to enter the it by using:

```
sudo docker exec -it KinRDF  bash
```

### Step 5 - Move the .ttl files
First, enter the "/data" folder and move the Turtle file(s) to the folder upstream by using:

```
mv data/KINRDF.ttl .
exit
```

### Step 6 - Enter the container SQL and reset
Enter the running docker container SQL by using: 

```
sudo docker exec -i KinRDF isql 1111
```

In case the service is already active and contains older RDF, be sure to perform a global reset and delete the old RDF files from the load_list, using the following commands:

```
RDF_GLOBAL_RESET();
DELETE FROM load_list WHERE ll_graph = 'KinRDF.org';
```

The presence of files in the load_list can be viewed using the following command:

```
select * from DB.DBA.load_list;
```

### Step 7 - Load the RDF
Use the following commands to complete the loading of prefixes in the SPARQL endpoint. If errors occur, try again within a few seconds (which often works), or look at http://docs.openlinksw.com/virtuoso/errorcodes/ to find out what they mean. Add more pre-defined PREFIXES if needed:

```
log_enable(2);
DB.DBA.XML_SET_NS_DECL ('SEP', 'http://vocabularies.wikipathways.org/kin#',2);
DB.DBA.XML_SET_NS_DECL ('dc', 'http://purl.org/dc/elements/1.1/',2);
DB.DBA.XML_SET_NS_DECL ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#',2);
DB.DBA.XML_SET_NS_DECL ('wp', 'http://vocabularies.wikipathways.org/wp#',2);
DB.DBA.XML_SET_NS_DECL ('rh', 'http://rdf.rhea-db.org/',2);
DB.DBA.XML_SET_NS_DECL ('dcterms', 'http://purl.org/dc/terms/#',2);
DB.DBA.XML_SET_NS_DECL ('xsd', 'http://www.w3.org/2001/XMLSchema#',2);
DB.DBA.XML_SET_NS_DECL ('S_id', 'http://identifiers.org/uniprot/',2);
DB.DBA.XML_SET_NS_DECL ('ECcode', 'https://identifiers.org/ec-code/',2);
DB.DBA.XML_SET_NS_DECL ('En_id', 'http://identifiers.org/ensembl/',2);
DB.DBA.XML_SET_NS_DECL ('PMID', 'http://identifiers.org/pubmed/',2);
DB.DBA.XML_SET_NS_DECL ('RHEA', 'https://www.rhea-db.org/reaction?id=',2);
DB.DBA.XML_SET_NS_DECL ('wd', 'http://www.wikidata.org/entity/',2);
DB.DBA.XML_SET_NS_DECL ('wdt', 'http://www.wikidata.org/prop/direct/',2);
log_enable(1);
grant select on "DB.DBA.SPARQL_SINV_2" to "SPARQL";
grant execute on "DB.DBA.SPARQL_SINV_IMP" to "SPARQL";
```

Load the data: 

```
ld_dir('.', 'KINRDF.ttl', 'KinRDF.org');
```

To finalize the loading of data, use:
```
rdf_loader_run();
```

Check the status and look if the all.ttl file is loaded by entering:
```
select * from DB.DBA.load_list;
```

If the "il_state" = 2, the loading is complete. If issues occurred in this step, have a look at http://vos.openlinksw.com/owiki/wiki/VOS/VirtBulkRDFLoader. 
Quit the SQL by entering:
```
quit;
```

### Step 8 - Enter the Virtuoso service with loaded AOP-Wiki RDF
The container is running with loaded RDF, available through http://localhost:8890, or enter the SPARQL endpoint directly through http://localhost:8890/sparql/. You can check if the data is loaded correctly, by executing the following SPARQL querie:

```SPARQL
select distinct ?Concept where {[] dc:identifier ?Concept} LIMIT 100
```

### Step 9 - Stop and remove the Docker container when done
```
sudo docker stop KinRDF
sudo docker rm KinRDF
```
