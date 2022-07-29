from rdflib import Graph

from namespaces import template_uri, reference_uri, class_uri, term_type_uri, rr_constant_uri
from util import parse_template


def get_subject_map(g: Graph, node):
    answer = {}

    template = list(g.objects(node, template_uri))
    if len(template) != 0:
        answer["template"] = template[0]

    reference = list(g.objects(node, reference_uri))
    if len(reference) != 0:
        answer["reference"] = reference[0]

    class_nodes = list(g.objects(node, class_uri))
    if len(class_nodes) != 0:
        answer["class_nodes"] = class_nodes[0]

    term_type = list(g.objects(node, term_type_uri))
    if len(term_type) != 0:
        answer["term_type"] = term_type[0]

    constant = list(g.objects(node, rr_constant_uri))
    if len(constant) != 0:
        # answer["constant"] = f'"{constant[0]}"'
        answer["constant"] = str(constant[0])


    return answer


def get_subject(subject, references, subject_value):
    if "template" in subject:
        return get_subject_template(subject, references, subject_value)
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


def get_subject_template(subject, references, subject_value):
    is_blank_node = "term_type" in subject and str(subject["term_type"]) == "http://www.w3.org/ns/r2rml#BlankNode"
    strings = []
    for element in parse_template(subject["template"]):
        if element["reference"]:
            if is_blank_node:
                strings.append(f' ?{references[element["value"]]}')
            else:
                strings.append(f'encode_for_uri(?{references[element["value"]]})')
        else:
            strings.append(f'str("{element["value"]}")')
    if is_blank_node:

        return f'        bind( BNODE({strings[0]}) as {subject_value})\n'
        # TODO wait for fx:bnode

        # return f'        bind(uri(concat({",".join(strings)})) as ?bnode_subject)\n' \
        #        + f'        bind( BNODE(?bnode_subject) as ?subject)\n'
    else:
        return f'        bind(uri(concat({",".join(strings)})) as {subject_value})\n'


def find_uri(search_value, predicates):
    for predicate in predicates:
        if str(predicate["reference"]) == search_value:
            return predicate["name"]
    return ""
