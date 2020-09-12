from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://dbpedia.org>
    select ?dbid ?yagoid 
    where {
      ?dbid a <http://www.w3.org/2002/07/owl#Thing>;
        owl:sameAs ?yagoid .
    filter strstarts( str(?yagoid), 'http://yago-knowledge.org/resource/' )
}
limit 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["dbid"]["value"],end='  ')
    print(result["yagoid"]["value"])
