from rdflib import Graph

from namespaces import predicate_uri, object_map_uri, object_uri, rml_reference_uri, template_uri, typing_uri
from util import parse_template


def make_construct(predicates, references, subject_value):
    return [f'    {subject_value} <{predicate["predicate"]}> {predicate["name"] if predicate["literal"] else( "?" + references[predicate["reference"]])} .\n' for
            predicate in predicates]


def make_getters(references):
    # TODO RMLTC0010a-CSV space in name crashes sparql, changing value makes it not work
    return [f'xyz:{reference}    ?{references[reference]}' for reference in references if reference != references[reference]]


# def get_predicate(g: Graph, node):
#     predicate_map = g.objects(node, predicate_map_uri)

def get_predicate_map(g: Graph, node):
    # predicate = get_predicate(g, node)

    predicate = list(g.objects(node, predicate_uri))

    if len(predicate) == 0:
        raise Exception("No predicate was found")

    object_maps = list(g.objects(node, object_map_uri))
    object_node = list(g.objects(node, object_uri))

    if len(object_maps) != 0:
        response = {"predicate": predicate[0], "literal": False}

        # TODO currently we assume there only is one object map
        # return {"predicate": predicate[0], "object_maps_node": object_maps[0], "literal": False}
        response.update(parse_object_map(g, object_maps[0]))
        return response
    elif len(object_node) != 0:
        return {"predicate": predicate[0], "object_node": f'<{object_node[0]}>', "literal": True}
    else:
        raise Exception("no object or object mapping was defined")
    # return {"predicate": predicate[0], "object_maps_node": object_maps_generator[0], "literal": False}


def parse_object_map(g: Graph, object_maps):
    response = {}
    reference = list(g.objects(object_maps, rml_reference_uri))
    template = list(g.objects(object_maps, template_uri))
    typing = list(g.objects(object_maps, typing_uri))

    if len(typing):
        response["typing"] = typing[0]

    if len(reference) != 0:
        response["reference"] = str(reference[0])
        response["references"] = [str(reference[0])]
    elif len(template) != 0:
        parsed_template = parse_template(template[0])
        response["references"] = ([str(element["value"]) for element in parsed_template if element["reference"]])
        response["template"] = parsed_template
    else:
        raise Exception("no reference or template in objectMap")

    return response


def make_setter(template, reference, references):
    answer = "        bind( concat("
    strings = []
    for element in template:
        if element["reference"]:
            strings.append(f'encode_for_uri(?{references[element["value"]]})')
        else:
            strings.append(f'str("{element["value"]}")')
    return answer + f'{",".join(strings)}) as ?{reference})\n'
