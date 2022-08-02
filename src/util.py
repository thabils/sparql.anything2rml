import copy
import subprocess

from rdflib import Graph
from rdflib.compare import isomorphic
import configparser

from namespaces import rr_constant_uri, rml_reference_uri, template_uri, typing_uri, language_uri


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
        return parse_map(g, map_list[0])
        #
        # constant = list(g.objects(map_list[0], rr_constant_uri))
        # if constant:
        #     return {"value": constant[0], "reference": False, "map": True}
        #
        # # find reference in map
        # reference = list(g.objects(map_list[0], reference_uri))
        # if reference:
        #     return {"value": reference[0], "reference": True, "map": True}
    direct = list(g.objects(node, direct_uri))
    if direct:
        return {"constant": direct[0], "reference": False}

    return {"value": ""}


def parse_map(g: Graph, object_map):
    response = {}

    typing = list(g.objects(object_map, typing_uri))
    language = list(g.objects(object_map, language_uri))

    constant = list(g.objects(object_map, rr_constant_uri))
    reference = list(g.objects(object_map, rml_reference_uri))
    template = list(g.objects(object_map, template_uri))

    if len(language):
        response["language"] = language[0]
    if len(typing):
        response["typing"] = typing[0]

    if len(reference) != 0:
        response["reference_value"] = str(reference[0])
        response["references"] = [str(reference[0])]
        response["reference"] = True

    elif len(template) != 0:
        parsed_template = parse_template(template[0])
        response["references"] = ([str(element["value"]) for element in parsed_template if element["reference"]])
        response["template"] = parsed_template
        response["reference"] = True

    elif len(constant) != 0:
        response["constant"] = str(constant[0])
        response["reference"] = False
    else:
        raise Exception("no reference, template or constant was found")

    return response


def make_template(template, references):
    strings = []
    for element in template:
        if element["reference"]:
            strings.append(f'encode_for_uri(?{references[element["value"]]})')
        else:
            strings.append(f'str("{element["value"]}")')
    return strings


def make_string_setter(object_map, reference, references):
    if "template" in object_map:
        strings = make_template(object_map["template"], references)
    else:
        strings = [f' ?{references[object_map["reference_value"]]} ']

    if "language" in object_map:
        strings.append(f'str("@{object_map["language"]}")')

    return f'        bind( concat({",".join(strings)}) as ?{reference})\n'


def make_uri_setter(subject, references, subject_value):
    strings = []
    for element in parse_template(subject["template"]):
        if element["reference"]:
            strings.append(f'encode_for_uri(?{references[element["value"]]})')
        else:
            strings.append(f'str("{element["value"]}")')
    return f'        bind(uri(concat({",".join(strings)})) as {subject_value})\n'
