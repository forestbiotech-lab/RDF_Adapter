from rdflib import Graph, Literal

graph = Graph()
graph.parse("TraceRice.nt", format="nt")
q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-synt-ax-ns#>
    PREFIX ppeo: <http://purl.org/ppeo/PPEO.owl#>
    <http://purl.org/ppeo/PPEO.owl>
    SELECT ?s WHERE {
        ?s rdf:type ppeo:investigation.
    }
    """
for investigation in graph.subjects("<http://www.w3.org/1999/02/22-rdf-synt-ax-ns#type>", "<http://purl.org/ppeo/PPEO.owl#investigation>"):
    print(investigation)


query = """
SELECT ?subject
WHERE {
    ?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ppeo/PPEO.owl#investigation> . 
}
"""


query2 = """
SELECT ?p ?o
WHERE {
    <http://brapi.biodata.pt/raiz/Study_TRACE-RICE:genomic_data_ITQB> ?p ?o .
}
"""

# Execute the query
results = graph.query(query2)


def is_literal(node):
  return isinstance(node, Literal)

# Print the filtered subjects
for row in results:
    print(is_literal(row[1]))
    print(" ".join(row))