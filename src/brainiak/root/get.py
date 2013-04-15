from tornado.web import HTTPError

from brainiak import triplestore
from brainiak.prefixes import prefix_to_slug
from brainiak.utils import sparql
from brainiak.utils.links import crud_links, split_into_chunks, collection_links, normalize

# Note that pagination was done outside the query
# because we are filtering query results based on prefixes
# (accessible from the application and not through SPARQL)
from brainiak.utils.resources import decorate_with_resource_id

QUERY_LIST_CONTEXT = """
SELECT DISTINCT ?graph
WHERE {GRAPH ?graph { ?s ?p ?o }}
"""


def list_all_contexts(params, request):
    sparql_response = triplestore.query_sparql(QUERY_LIST_CONTEXT)
    all_contexts_uris = sparql.filter_values(sparql_response, "graph")

    filtered_contexts = filter_and_build_contexts(all_contexts_uris)
    total_contexts = len(filtered_contexts)

    if not filtered_contexts:
        raise HTTPError(404, log_message="No contexts were found.")

    contexts_pages = split_into_chunks(filtered_contexts, int(params["per_page"]))
    contexts = contexts_pages[int(params["page"])]

    contexts_json = build_json(contexts, total_contexts, params, request)
    return contexts_json


def filter_and_build_contexts(contexts_uris):
    contexts = []
    for uri in contexts_uris:
        slug = prefix_to_slug(uri)
        if slug != uri:
            context_info = {
                "title": slug,
                "@id": uri
            }
            contexts.append(context_info)
    decorate_with_resource_id(contexts)
    return contexts


def build_json(contexts, total_items, params, request):
    base_url = "{0}://{1}{2}".format(request.protocol, request.host, request.path)
    resource_url = "%s/{resource_id}" % normalize(base_url)
    links = crud_links(base_url, resource_url, params) + \
            collection_links(base_url, params, total_items)
    json = {
        'items': contexts,
        'item_count': total_items,
        'links': links
    }
    return json
