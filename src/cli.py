import sys

from main import generate_sparql_anything
from util import call_sparql_anything_jar, compare_n3_files

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print('You have specified too many arguments')
        sys.exit()

    if len(sys.argv) < 3:
        print('You need to specify the mapping file and mode')
        sys.exit()

    input_file = sys.argv[1]
    mode = sys.argv[2]
    print(input_file)
    if mode == "generate":
        generate_sparql_anything(input_file)
    if mode == "test":
        generate_sparql_anything(input_file)
        test_case_directory = input_file[:input_file.rfind("/")]
        call_sparql_anything_jar(test_case_directory, test_case_directory + "/" + "sparql_output.nq")
        if compare_n3_files(test_case_directory + "/sparql_output.nq", test_case_directory + "/output.nq"):
            print("Correct!")
        else:
            print("False")

