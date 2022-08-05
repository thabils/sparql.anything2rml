from rdflib import Graph

from namespaces import typing_uri, source_uri, iterator_uri


def parse_source(g: Graph, node, directory, index):
    type_node = list(g.objects(node, typing_uri))
    if type_node:
        if str(type_node[0]) == "http://semweb.mmlab.be/ns/ql#CSV":
            return {"header": make_csv_header(g, node, directory), "typing": "csv"}
        elif str(type_node[0]) == "http://semweb.mmlab.be/ns/ql#JSONPath":
            return {"header": make_header(g, node, directory) + ">", "facade": make_json_facade(g, node, index),
                    "typing": "json"}
        elif str(type_node[0]) == "http://semweb.mmlab.be/ns/ql#XPath":
            return {"header": make_header(g, node, directory) + ">", "iterator": parse_xml_iterator(g, node),
                    "typing": "xml", "index": index}
    else:
        raise Exception("No typing for the source was found")


# makes the generic header used in each type of query (specify's location and sparql anything)
def make_header(g: Graph, node, directory):
    response = f' <x-sparql-anything:'

    location_source = list(g.objects(node, source_uri))
    if len(location_source) == 0:
        raise Exception("No source was found")
    response += f'location={directory}/{str(location_source[0])}'
    return response


def parse_xml_iterator(g: Graph, node):
    iterator = list(g.objects(node, iterator_uri))
    if iterator:
        return str(iterator[0]).split("/")[1:]
    else:
        raise Exception("")


def make_csv_header(g: Graph, node, directory):
    response = make_header(g, node, directory)

    # CSVW files could change this
    response += f',csv.headers=true'
    iterator = list(g.objects(node, iterator_uri))
    if len(iterator) != 0:
        response += f',csv.format={iterator[0]}'
    return response + ">"


# generates the facade out of the json iterator
def parse_iterator_json(iterator: str, index):
    split = iterator[1:iterator.find("[")].split(".")[1:]
    return f' xyz:{"/xyz:".join(split)}/fx:anySlot ?iterator{index} . \n' + f"        ?iterator{index}  "


def make_json_facade(g: Graph, node, index):
    iterator = list(g.objects(node, iterator_uri))
    facade = ""
    # if no iterator is found then there is no need for a facade
    if len(iterator) != 0:
        facade = parse_iterator_json(str(iterator[0]), index)
    return facade
