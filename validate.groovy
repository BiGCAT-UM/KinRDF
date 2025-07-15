// MIT, Copyright (c) Egon Willighagen
@Grab(group='io.github.egonw.bacting', module='managers-rdf', version='1.0.5')

import org.apache.jena.shex.ShexStatus

workspaceRoot = "."
rdf = new net.bioclipse.managers.RDFManager(workspaceRoot);

file = "/Output/RDF_Kin_Data_2022-Dec.ttl"
clazz = args[0]
type = args[1]

store = rdf.createInMemoryStore(true);
store = rdf.importFile(store, "${file}", "TURTLE")
report = rdf.validateAllOfType(
  store,
  "/shapes/${clazz}.shex",
  "http://bigcat-um.github.io/KinRDF/shapes#${clazz}",
  "${type}"
)

println "{"
println "  \"target\": \"${clazz}\","
println "  \"conformant\": ["
report.forEachReport { reportEntry ->
  status = reportEntry.status
  reason = reportEntry.reason
  focusNode = reportEntry.focus

  switch (status) {
    case ShexStatus.conformant :
      println "    {\n      \"class\":  \"${focusNode}\",\n      \"status\": \"${status}\"\n    },"
  }
}
println "    {}"
println "  ],"
nonconformantCounter = 0
println "  \"nonconformant\": ["
report.forEachReport { reportEntry ->
  status = reportEntry.status
  reason = reportEntry.reason
  focusNode = reportEntry.focus

  switch (status) {
    case ShexStatus.nonconformant :
      nonconformantCounter = nonconformantCounter + 1
      println "    {\n      \"class\":  \"${focusNode}\",\n      \"status\": \"${status}\",\n      \"reason\": \"${reason}\"\n    },"
  }
}
println "    {}"
println "  ]"
println "}"

if (nonconformantCounter > 0) System.exit(1)
