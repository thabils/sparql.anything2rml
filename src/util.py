import subprocess

import rdflib
from rdflib import Graph
from rdflib.compare import isomorphic


def find_literal(list_nodes):
    for node in list_nodes:
        if node is rdflib.term.Literal:
            return node
    return ""


def call_sparql_anything_jar(directory, output_file):
    subprocess.call(
        ['java', '-jar', 'sparql-anything-0.7.0.jar', '-q', directory + '/query.sparql', '-f', 'NQ', '-o', output_file])
    return


def compare_n3_files(new_file, original_file):
    # compare both files, return true if same file otherwise false
    g1 = Graph().parse(new_file)
    g2 = Graph().parse(original_file)
    return isomorphic(g1, g2)


# def parse_template(template, predicates):
#     response = []
#     while template.find("{") != -1:
#         if template.find("{") != 0:
#             response.append({"value": template[:template.find("{")], "reference": False})
#
#         temp_uri = find_uri(template[template.find("{") + 1:template.find("}")], predicates)
#         response.append({"value": str(temp_uri), "reference": True})
#         template = template[template.find("}") + 1:]
#     return response


def parse_template(template):
    response = []
    while template.find("{") != -1:
        if template.find("{") != 0:
            response.append({"value": template[:template.find("{")], "reference": False})
        response.append({"value": str(template[template.find("{") + 1:template.find("}")]), "reference": True})
        template = template[template.find("}") + 1:]
    return response


def find_uri(search_value, predicates):
    for predicate in predicates:
        if str(predicate["reference"]) == search_value:
            return predicate["name"]
    return ""
