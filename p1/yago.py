


from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://yago-knowledge.org/sparql/query")
sparql.setQuery(
"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?s ?o WHERE {
  ?s rdf:type ?o .
} 
LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])
   

