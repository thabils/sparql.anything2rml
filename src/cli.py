import argparse
import sys

from main import generate_sparql_anything
from util import call_sparql_anything_jar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform RMLMapper mapping file to SPARQL Anything query.')

    parser.add_argument('--m', '-mode', dest="mode", default="generate", type=str,
                        choices=["run", "generate", "create"],
                        help="The different modes of the script:\n" \
                             + "      create: given a mapping file, create an equivalent SPARQL Anything query\n"
                             + "run: given a query file, run this query on the SPARQL Anything JAR specified in the "
                               "config\n "
                             + "generate: given a mapping file, create an equivalent SPARQL Anything query and then "
                               "run this file.\n")

    parser.add_argument('--i', '-input', type=str, required=True, help='path to input file ')

    parser.add_argument('--o', '-output', default="", type=str,
                        help='OPTIONAL path to where the output (SPARQL anything query itself) should be generated')

    parser.add_argument('--so', '-sparql-output', default="", type=str,
                        help='OPTIONAL path to where the output of the SPARQL anything query should be generated')

    args = parser.parse_args(sys.argv[1:])
    input_file = args.i

    print(input_file)

    if args.mode == "generate" or args.mode == "create":
        print("creating file")
        generate_sparql_anything(args.i, args.o)
    if args.mode == "generate" or args.mode == "run":
        test_case_directory = input_file[:input_file.rfind("/")]
        sparql_query = args.o
        if sparql_query == "":
            sparql_query = test_case_directory + "/query.sparql"
        sparql_output = args.so
        if sparql_output == "":
            sparql_output = test_case_directory + "/sparql_output.nq"
        call_sparql_anything_jar(sparql_query, sparql_output)
