from rdflib import Graph

from logical_sources import parse_source
from namespaces import predicate_object_map_uri, logical_source_uri, subject_map_uri, rr_iri_uri
from predicates import get_predicate_map, make_getters, make_construct
from util import make_string_setter
from subjects import get_subject_map, get_subject_setter, get_subject_references


def make_query(base, construct, services):
    prefixes = "PREFIX fx:  <http://sparql.xyz/facade-x/ns/>\n" + "PREFIX xyz: <http://sparql.xyz/facade-x/data/>\n" + \
               base
    answer = prefixes + "\n" + "CONSTRUCT\n" + "  {\n"
    answer += "".join(construct)
    answer += " }\n" + "WHERE\n" + "  {\n"

    for amount, service in enumerate(services):
        source = service["source"]

        answer += f'    SERVICE{source["header"]}\n' + '      {\n'
        # xml has its own specific getters
        if source["typing"] == "xml":
            answer += service["getters"]
        else:
            # we check if there is anything that needs to be added to SERVICE, if not we leave it empty
            if service["getters"] or ("facade" in source and source["facade"]):
                answer += f'      	?s{amount}  '
            # if there are any facade's needed (currently only used for json files,
            # see https://github.com/SPARQL-Anything/sparql.anything/issues/278 for example)
            if "facade" in source:
                answer += source["facade"]
            answer += ";\n      	    ".join(service["getters"])
            if service["getters"] or ("facade" in source and source["facade"]):
                answer += ".\n"
        answer += "".join(service["setters"])
        answer += '      }\n'
    answer += '  }'
    return answer


# get the base value of the mapping file
def get_base(mapping_file):
    with open(mapping_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("@base "):
                return f'base {line[line.index(" "):-2]}\n'


# function that parses a single triple map and returns the needed information out of it
def parse_triple_map(g: Graph, triple_map, directory, reference_value, index):
    all_predicates = []
    references = {}
    setters = []

    logical_source = list(g.objects(triple_map, logical_source_uri))
    if len(logical_source) == 0:
        raise Exception("No logical source specified")
    source = parse_source(g, logical_source[0], directory, index)

    subject = list(g.objects(triple_map, subject_map_uri))
    if len(subject) == 0:
        raise Exception("No subject specified")

    subject_map = get_subject_map(g, subject[0])

    for element in get_subject_references(subject_map):
        if element not in references:
            references[element] = str(reference_value["reference"])
            reference_value["reference"] += 1

    for o in g.objects(triple_map, predicate_object_map_uri):
        predicates, object_map = get_predicate_map(g, o)
        # add all references that are used in this predicate to the dict references (if reference is not already in it)
        for predicate in predicates:
            if "references" in object_map:
                for value in object_map["references"]:
                    if value not in references:
                        references[value] = str(reference_value["reference"])
                        reference_value["reference"] += 1
            if "template" in object_map:
                # "bound" refers to the final ? value that is used in construct
                object_map["bound"] = str(reference_value["reference"])
                # add this reference to the dict of references
                references[str(reference_value["reference"])] = str(reference_value["reference"])
                reference_value["reference"] += 1
            if "reference_value" in object_map:
                # if the predicate only has one reference we can directly use this value as bound value
                object_map["bound"] = references[object_map["reference_value"]]
            # language tags dont not work
            # if "language" in object_map:
            #     object_map["bound"] = str(reference_value["reference"])
            #     references[str(reference_value["reference"])] = str(reference_value["reference"])
            #     reference_value["reference"] += 1

            if "template" in object_map or "language" in object_map:
                # if language or template is used then we will need a setter for this predicate
                # uri refers to if the value of the predicate is supposed to be a uri or a literal value
                uri = not ("typing" in object_map and object_map["typing"] != rr_iri_uri)
                setters.append(make_string_setter(object_map, object_map["bound"], references, uri))

            if "parent_triples_map" in object_map:
                # if a parent triples map is present in the predicate map we need to parse
                # the subject map of this parent triples map and use this value as the value of the predicate
                parent_subject_map = get_subject_map(g, object_map["parent_triples_map"])

                # add all references to the references dict
                for element in get_subject_references(parent_subject_map):
                    if element not in references:
                        references[element] = str(reference_value["reference"])
                        reference_value["reference"] += 1
                setters.append(get_subject_setter(parent_subject_map, references, f'?{reference_value["reference"]}'))
                object_map["bound"] = str(reference_value["reference"])
                object_map["reference"] = True
                reference_value["reference"] += 1
            all_predicates.append((predicate, object_map))

    # add an extra predicate if there is a class present in the subject map
    if "class_nodes" in subject_map:
        all_predicates.append((
            {"constant": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"},
            {"constant": f'{subject_map["class_nodes"]}',
             "reference": False}))

    getters = make_getters(references, source)

    subject_value = f'?subject{reference_value["subject"]}'
    reference_value["subject"] += 1
    # if subject is a constant we can just use this constant value in the construct part
    if "constant" in subject_map:
        subject_value = f'<{subject_map["constant"]}>'
    is_subject_bnode = "term_type" in subject_map and \
                       str(subject_map["term_type"]) == "http://www.w3.org/ns/r2rml#BlankNode"
    construct = make_construct(all_predicates, subject_value, is_subject_bnode)

    setters.append(get_subject_setter(subject_map, references, subject_value))

    return construct, source, getters, setters, reference_value


def generate_sparql_anything(mapping_file, sparql_anything_file):
    directory = mapping_file[:mapping_file.rfind("/")]
    if sparql_anything_file == "":
        # if no file is specified use this default value for the sparql anything query
        sparql_anything_file = directory + "/query.sparql"

    g = Graph()
    g.parse(mapping_file)

    base = get_base(mapping_file)
    last_reference_value = {"subject": 0, "reference": 0}
    general_construct = []
    services = []

    # parse all the different triples maps
    for index, (s, _) in enumerate(g.subject_objects(logical_source_uri)):
        construct, source, getters, setters, last_reference_value = parse_triple_map(g, s, directory,
                                                                                     last_reference_value, index)
        general_construct.extend(construct)
        services.append({"source": source, "getters": getters, "setters": setters})

    with open(sparql_anything_file, "w") as f:
        f.write(make_query(base, general_construct, services))
    return
