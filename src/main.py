from rdflib import Graph

from logical_sources import get_sparql_header
from namespaces import predicate_object_map_uri, logical_source_uri, subject_map_uri
from predicates import get_predicate_map, make_getters, make_construct, make_setter
from subjects import get_subject_map, get_subject, get_subject_references


def make_query(base, construct, services):
    prefixes = "PREFIX fx:  <http://sparql.xyz/facade-x/ns/>\n" + "PREFIX xyz: <http://sparql.xyz/facade-x/data/>\n" + \
               base
    answer = prefixes + "\n" + "CONSTRUCT\n" + "  {\n"
    answer += "".join(construct)
    answer += " }\n" + "WHERE\n" + "  {\n"

    for amount, service in enumerate(services):
        answer += f'    SERVICE{service["sparql_header"]}\n' + '      {\n'

        for index, getter in enumerate(service["getters"]):
            if index == 0:
                answer += f'      	?s{amount}  '
            else:
                answer += '      	    '
            answer += getter
            if index + 1 == len(service["getters"]):
                answer += ".\n"
            else:
                answer += ";\n"

        answer += "".join(service["setters"])
        answer += '      }\n'
    answer += '  }'
    return answer


def get_base(mapping_file):
    with open(mapping_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("@base "):
                return f'base {line[line.index(" "):-2]}\n'


def parse_triple_map(g: Graph, triple_map, directory, last_reference_value):
    predicates = []
    references = {}
    setters = []

    logical_source = list(g.objects(triple_map, logical_source_uri))
    if len(logical_source) == 0:
        raise Exception("No logical source specified")
    sparql_header = get_sparql_header(g, logical_source[0], directory)

    for o in g.objects(triple_map, predicate_object_map_uri):
        predicate = get_predicate_map(g, o)
        if "references" in predicate:
            for value in predicate["references"]:
                if value not in references:
                    references[value] = str(last_reference_value)
                    last_reference_value += 1
        if "template" in predicate:
            predicate["bound"] = str(last_reference_value)
            references[str(last_reference_value)] = str(last_reference_value)
            last_reference_value += 1
        if "reference" in predicate:
            predicate["bound"] = references[predicate["reference"]]
        if "language" in predicate:
            predicate["bound"] = str(last_reference_value)
            references[str(last_reference_value)] = str(last_reference_value)
            last_reference_value += 1

        if "template" in predicate or "language" in predicate:
            setters.append(make_setter(predicate, predicate["bound"], references))

        predicates.append(predicate)

    subject_map = get_subject_map(g, next(g.objects(triple_map, subject_map_uri)))
    for element in get_subject_references(subject_map):
        if element not in references:
            references[element] = str(last_reference_value)
            last_reference_value += 1

    if "class_nodes" in subject_map:
        predicates.append(
            {"constant": f'<{subject_map["class_nodes"]}>',
             "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
             "literal": True})

    getters = make_getters(references)

    subject_value = f'?subject{last_reference_value}'
    if "constant" in subject_map:
        subject_value = f'<{subject_map["constant"]}>'
    subject_bnode = "term_type" in subject_map and str(subject_map["term_type"]) == "http://www.w3.org/ns/r2rml#BlankNode"
    construct = make_construct(predicates, subject_value, subject_bnode)
    setters.append(get_subject(subject_map, references, subject_value))
    return construct, sparql_header, getters, setters, last_reference_value


def generate_sparql_anything(mapping_file):
    directory = mapping_file[:mapping_file.rfind("/")]
    # mapping_file = directory + "/mapping.ttl"
    sparql_anything_file = directory + "/query.sparql"

    g = Graph()
    g.parse(mapping_file)

    base = get_base(mapping_file)
    last_reference_value = 0
    general_construct = []
    services = []

    # parse all the different triples maps
    for s, _ in g.subject_objects(logical_source_uri):
        construct, sparql_header, getters, setters, last_reference_value = parse_triple_map(g, s, directory,
                                                                                            last_reference_value)
        general_construct.extend(construct)
        services.append({"sparql_header": sparql_header, "getters": getters, "setters": setters})

    with open(sparql_anything_file, "w") as f:
        f.write(make_query(base, general_construct, services))
    return

# print(generate_sparql_anything("test_cases/RMLTC0001a-CSV"))
# print(generate_sparql_anything("!used_test_cases/RMLTC0001b-CSV"))
# print(generate_sparql_anything("!used_test_cases/RMLTC0002a-CSV"))
# print(generate_sparql_anything("!used_test_cases/RMLTC0003c-CSV"))
# print(generate_sparql_anything("test_cases/RMLTC0015a-CSV"))
