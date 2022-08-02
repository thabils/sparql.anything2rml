from rdflib import Graph

from namespaces import template_uri, reference_uri, class_uri, term_type_uri, rr_constant_uri
from util import parse_template, make_uri_setter, make_string_setter


def get_subject_map(g: Graph, node):
    response = {}

    template = list(g.objects(node, template_uri))
    if template:
        response["template"] = template[0]

    reference = list(g.objects(node, reference_uri))
    if reference:
        response["reference"] = reference[0]

    class_nodes = list(g.objects(node, class_uri))
    if class_nodes:
        response["class_nodes"] = class_nodes[0]

    term_type = list(g.objects(node, term_type_uri))
    if term_type:
        response["term_type"] = term_type[0]

    constant = list(g.objects(node, rr_constant_uri))
    if constant:
        response["constant"] = str(constant[0])
    return response


def get_subject_setter(subject, references, subject_value):
    if "template" in subject:
        return get_subject_template_setter(subject, references, subject_value)
    elif "reference" in subject:
        # TODO look at test case RMLTC0020b-CSV does this typing matter?

        # currently assuming that the reference is already an iri
        return f'        bind(iri(?{references[str(subject["reference"])]}) as {subject_value})\n'
    elif "constant" in subject:
        # subject is constant so can just be added in construct
        return ""


def get_subject_references(subject):
    if "template" in subject:
        return [str(element["value"]) for element in parse_template(subject["template"]) if element["reference"]]
    elif "reference" in subject:
        return [str(subject["reference"])]
    elif "constant" in subject:
        return []


def get_subject_template_setter(subject, references, subject_value):
    is_blank_node = "term_type" in subject and str(subject["term_type"]) == "http://www.w3.org/ns/r2rml#BlankNode"
    if is_blank_node:
        return make_string_setter({"template": parse_template(subject["template"])}, subject_value[1:], references)
    else:
        return make_uri_setter(subject, references, subject_value)
