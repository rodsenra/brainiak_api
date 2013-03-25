from brainiak import triplestore
from brainiak.utils.sparql import create_explicit_triples, create_instance_uri


# TODO: test
def create_instance(query_params, instance_data):
    class_uri = query_params["class_uri"]
    instance_uri = create_instance_uri(class_uri)

    triples = create_explicit_triples(instance_uri, instance_data)
    implicit_triples = create_implicit_triples(instance_uri, class_uri)
    triples.extend(implicit_triples)
    string_triples = join_triples(triples)

    prefixes = instance_data.get("@context", {})
    string_prefixes = join_prefixes(prefixes)
    response = query_create_instances(string_triples, string_prefixes, query_params["graph_uri"])
    return instance_uri



QUERY_INSERT_TRIPLES = """
%(prefix)s
INSERT DATA INTO <%(graph_uri)s>
{
%(triples)s
}
"""


def query_create_instances(triples, prefix, graph_uri):
    query = QUERY_INSERT_TRIPLES % {"triples": triples, "prefix": prefix, "graph_uri": graph_uri}
    return triplestore.query_sparql(query)
