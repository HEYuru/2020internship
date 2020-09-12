


from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
"""
PREFIX dbc: <http://dbpedia.org/resource/Category:>


SELECT DISTINCT ?s ?p ?o WHERE {
     
    ?s dct:subject dbc:English_rock_singers.
    ?s ?p ?o
   filter strstarts( str(?o), 'http://dbpedia.org/ontology' )

}

limit 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"],end='  ')
    print(result["o"]["value"])


'''
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?s ?p ?o WHERE {
     
    ?s a dbo:Person.
    ?s ?p ?o.
   filter strstarts( str(?o), 'http://dbpedia.org/ontology' )
}

limit 1000

'''
