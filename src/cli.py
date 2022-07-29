import sys

from main import generate_sparql_anything


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('You have specified too many arguments')
        sys.exit()

    if len(sys.argv) < 2:
        print('You need to specify the mapping file')
        sys.exit()

    input_file = sys.argv[1]

    print(input_file)
    generate_sparql_anything(input_file)

