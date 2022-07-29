import copy
import subprocess

import rdflib
from rdflib import Graph
from rdflib.compare import isomorphic
import configparser

from namespaces import rr_constant_uri, reference_uri


def find_literal(list_nodes):
    for node in list_nodes:
        if node is rdflib.term.Literal:
            return node
    return ""


def call_sparql_anything_jar(directory, output_file):
    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config.sections())
    jar_version = config.get("JAR", "VERSION")
    print(jar_version)

    subprocess.call(
        ['java', '-jar', jar_version, '-q', directory + '/query.sparql', '-f', 'NQ', '-o', output_file])
    return


def compare_n3_files(new_file, original_file):
    # compare both files, return true if same file otherwise false
    g1 = Graph().parse(new_file)
    g2 = Graph().parse(original_file)
    return isomorphic(g1, g2)


def parse_escaped_curly_brackets(template):
    temp_template = copy.copy(template)
    strings = []
    index = temp_template.find("\\")
    while index != -1:
        if index != 0:
            strings.append(temp_template[:index])
            temp_template = temp_template[index + 1:]
        else:
            if index + 1 == temp_template.find("{"):
                strings.append("{")
                temp_template = temp_template[index + 2:]
            elif index + 1 == temp_template.find("}"):
                strings.append("}")
                temp_template = temp_template[index + 2:]
            else:
                strings.append("\\")
                temp_template = temp_template[index + 1:]
        index = temp_template.find("\\")
    strings.append(temp_template)
    return strings


def parse_string(template):
    response = []
    index_l = template.find("{")
    index_r = template.find("}")
    # this is an escaped character of a string to short to have any references in it
    if len(template) == 1:
        return [{"value": template, "reference": False}]

    while index_l != -1:
        if index_r < index_l:
            raise Exception("invalid template")
        if index_l != 0:
            response.append({"value": template[:index_l], "reference": False})
        response.append({"value": template[index_l + 1: index_r], "reference": True})
        template = template[index_r + 1:]
        index_l = template.find("{")
        index_r = template.find("}")

    if template != "":
        response.append({"value": template, "reference": False})
    return response


def parse_template(template):
    strings = parse_escaped_curly_brackets(template)
    final_response = []
    add_element = ""

    for element in [j for i in strings for j in parse_string(i)]:
        if element["reference"]:
            if add_element != "":
                final_response.append({"value": add_element, "reference": False})
                add_element = ""
            final_response.append(element)
        else:
            add_element += element["value"]
    if add_element != "":
        final_response.append({"value": add_element, "reference": False})
    return final_response


def find_uri(search_value, predicates):
    for predicate in predicates:
        if str(predicate["reference"]) == search_value:
            return predicate["name"]
    return ""


def get_value(g: Graph, node, map_uri, direct_uri):
    map_list = list(g.objects(node, map_uri))
    if len(map_list) == 0:
        return list(g.objects(node, direct_uri))
    # find constant in map
    predicate_constant = list(g.objects(map_list[0], rr_constant_uri))
    if len(predicate_constant) == 0:
        # find reference in map
        return list(g.objects(map_list[0], reference_uri))
    return predicate_constant
