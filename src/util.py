import copy
import subprocess

import rdflib
from rdflib import Graph
from rdflib.compare import isomorphic
import configparser

from namespaces import rr_constant_uri, reference_uri


def call_sparql_anything_jar(directory, output_file):
    config = configparser.ConfigParser()
    config.read("config.ini")
    jar_version = config.get("JAR", "VERSION")

    subprocess.call(['java', '-jar', jar_version, '-q', directory + '/query.sparql', '-f', 'NQ', '-o', output_file])
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


def get_value(g: Graph, node, map_uri, direct_uri):
    map_list = list(g.objects(node, map_uri))
    if map_list:
        # find constant in map
        constant = list(g.objects(map_list[0], rr_constant_uri))
        if constant:
            return {"value": constant[0], "reference": False}

        # find reference in map
        reference = list(g.objects(map_list[0], reference_uri))
        if reference:
            return {"value": reference[0], "reference": True}
    direct = list(g.objects(node, direct_uri))
    if direct:
        return {"value": direct[0], "reference": False}

    return {"value": ""}

