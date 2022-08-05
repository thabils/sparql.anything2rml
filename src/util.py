import copy
import os
import subprocess

from rdflib import Graph
import configparser

from namespaces import rr_constant_uri, rml_reference_uri, template_uri, language_uri, rr_iri_uri, \
    parent_triples_map_uri, subject_map_uri, term_type_uri


def call_sparql_anything_jar(query, output_file):
    config = configparser.ConfigParser()
    config.read("config.ini")
    jar_version = config.get("JAR", "VERSION")

    subprocess.call(['java', '-jar', jar_version, '-q', query, '-f', 'NQ', '-o', output_file])
    return


def compare_n3_files(new_file, original_file):
    # compare both files, return true if same file otherwise false
    new_file_dict = set()
    with open(new_file, "r") as f:
        for line in f:
            if line.strip():
                new_file_dict.add(line.strip())

    original_file_dict = set()
    with open(original_file, "r") as f:
        for line in f:
            if line.strip():
                original_file_dict.add(line.strip())

    print(original_file_dict.difference(new_file_dict))
    print(new_file_dict.difference(original_file_dict))
    return new_file_dict == original_file_dict


def compare_n3_files_delete(new_file, original_file):
    response = compare_n3_files(new_file, original_file)
    os.remove(new_file)
    return response

# goes through string and splits the string on escaped {, }
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


# parses for references in the template
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


def get_values(g: Graph, node, map_uri, direct_uri):
    response = []
    for element in list(g.objects(node, map_uri)):
        response.append(parse_map(g, element))
    for element in list(g.objects(node, direct_uri)):
        response.append({"constant": element, "reference": False})
    return response


def get_value(g: Graph, node, map_uri, direct_uri):
    map_list = list(g.objects(node, map_uri))
    if map_list:
        return parse_map(g, map_list[0])
    direct = list(g.objects(node, direct_uri))
    if direct:
        return {"constant": direct[0], "reference": False}

    return {"value": ""}


def parse_parent_triples_map(g, parent_triples_map):
    subject_map = list(g.objects(parent_triples_map, subject_map_uri))
    if subject_map:
        return subject_map[0]
    else:
        raise Exception("no subject map found in parent triples map")


def parse_map(g: Graph, object_map):
    response = {}
    parent_triples_map = list(g.objects(object_map, parent_triples_map_uri))

    typing = list(g.objects(object_map, term_type_uri))
    language = list(g.objects(object_map, language_uri))

    constant = list(g.objects(object_map, rr_constant_uri))
    reference = list(g.objects(object_map, rml_reference_uri))
    template = list(g.objects(object_map, template_uri))

    if len(language):
        response["language"] = language[0]
    if typing:
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
        if "typing" not in response:
            response["typing"] = rr_iri_uri

    elif len(constant) != 0:
        response["constant"] = str(constant[0])
        response["reference"] = False
    elif parent_triples_map:
        response["parent_triples_map"] = parse_parent_triples_map(g, parent_triples_map[0])
    else:
        raise Exception("no reference, template or constant was found")

    return response


def make_template(template, references, uri):
    strings = []
    for element in template:
        if element["reference"] and uri:
            strings.append(f'encode_for_uri(str(?{references[element["value"]]}))')
        elif element["reference"]:
            strings.append(f'str(?{references[element["value"]]})')
        elif uri:
            strings.append(f'str("{element["value"]}")')
        else:
            strings.append(f'str("{element["value"]}")')

    return strings


def make_string_setter(object_map, reference, references, uri):
    if "template" in object_map:
        strings = make_template(object_map["template"], references, uri)
    else:
        strings = [f' ?{references[object_map["reference_value"]]} ']

    # if "typing" in object_map and object_map["typing"] == rr_iri_uri:
    if uri:
        return f'        bind(uri(concat({",".join(strings)})) as ?{reference})\n'

    return f'        bind( concat({",".join(strings)}) as ?{reference})\n'
