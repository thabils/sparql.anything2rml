from src.main import generate_sparql_anything
from src.util import call_sparql_anything_jar, compare_n3_files_delete


def check(case, type_test):
    print(case + "-" + type_test)
    test_case_directory = f"test_cases/{type_test}/{case}-{type_test.upper()}"
    generate_sparql_anything(test_case_directory + "/mapping.ttl")
    call_sparql_anything_jar(test_case_directory, test_case_directory + "/" + "sparql_output.nq")

    return compare_n3_files_delete(test_case_directory + "/sparql_output.nq", test_case_directory + "/output.nq")
