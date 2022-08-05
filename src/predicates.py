from rdflib import Graph

from namespaces import predicate_uri, object_map_uri, object_uri, predicate_map_uri
from util import get_value, get_values


def make_construct(predicates, subject_value, subject_bnode):
    return [f'    {"_:" + subject_value[1:] if subject_bnode else subject_value} <{predicate["constant"]}> ' +
            f'{("?" + object_map["bound"]) if object_map["reference"] else ("<" + object_map["constant"] + ">")} .\n' for
            (predicate, object_map) in predicates]


def make_getters(references, source):
    if source["typing"] == "xml":
        strings = []
        # check if iterator atleast has 1 element if so add basic value for response
        if source["iterator"]:
            strings.append(f'[ a xyz:{source["iterator"][0].replace(" ", "%20")}')

        index = 0
        for value in source["iterator"][1:]:
            strings.append(f' ?{source["index"]}li{index} [ a xyz:{value.replace(" ", "%20")}')
            index += 1
        filter_string = ""
        for reference in references:
            if reference != references[reference]:
                filter_string += f'        FILTER(?{references[reference]} != xyz:{reference.replace(" ", "%20")}) . \n'
                strings.append(f'?{source["index"]}li{index} [ a xyz:{reference.replace(" ", "%20")}; ?{source["index"]}li{index + 1} ?{references[reference]}]')
                index += 2
        return f'        {";".join(strings)}{"]" * len(source["iterator"])} .\n' + filter_string
    else:
        # TODO RMLTC0010a-CSV space in name crashes sparql, changing value makes it not work
        return [f'xyz:{reference.replace(" ", "%20")}    ?{references[reference]}' for reference in references if
                reference != references[reference]]


def get_predicate_map(g: Graph, node):
    predicates = get_values(g, node, predicate_map_uri, predicate_uri)
    object_map = get_value(g, node, object_map_uri, object_uri)
    return predicates, object_map
