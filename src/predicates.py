from rdflib import Graph

from namespaces import predicate_uri, object_map_uri, object_uri, predicate_map_uri
from util import get_value


def make_construct(predicates, subject_value, subject_bnode):
    return [f'    {"_:" + subject_value[1:] if subject_bnode else subject_value} <{predicate["constant"]}> ' +
            f'{("?" + object_map["bound"]) if object_map["reference"] else ("<" + object_map["constant"] + ">")} .\n' for
            (predicate, object_map) in predicates]


def make_getters(references):
    # TODO RMLTC0010a-CSV space in name crashes sparql, changing value makes it not work
    return [f'xyz:{reference}    ?{references[reference]}' for reference in references if
            reference != references[reference]]


def get_predicate_map(g: Graph, node):
    predicate = get_value(g, node, predicate_map_uri, predicate_uri)

    object_map = get_value(g, node, object_map_uri, object_uri)
    return predicate, object_map
