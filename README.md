# sparql.anything2rml


## How to use


### Setup

    pip install -r requirements.txt

### CLI
To generate a SPARQL Anything file:

    python3 src/cli.py -i MAPPING_FILENAME -m create

To generate the output of a SPARQL Anything query:

    python3 src/cli.py -i MAPPING_FILENAME -m run

To generate a SPARQL Anything file and generate it's output:

    python3 src/cli.py -i MAPPING_FILENAME -m generate

All options can be found when executing python using 

    python3 src/cli.py --help

this gives the following output:

    usage: cli.py [-h] [--m {run,generate,create}] --i I [--o O] [--so SO]

    Transform RMLMapper mapping file to SPARQL Anything query.
    
    optional arguments:
      -h, --help            show this help message and exit
      --m {run,generate,create}, -mode {run,generate,create}
                            The different modes of the script: create: given a mapping file,
                            create an equivalent SPARQL Anything query run: given a query file, run this query on the SPARQL Anything JAR
                            specified in the config generate: given a mapping file, create an equivalent SPARQL Anything query and then run this file.
      --i I, -input I       path to input file
      --o O, -output O      OPTIONAL path to where the output (SPARQL anything query itself) should be generated
      --so SO, -sparql-output SO
                            OPTIONAL path to where the output of the SPARQL anything query should be generated



## Testing

### Setup
To enable testing add a sparql anything jar to the project.
After this add the path from the root of the project to config.ini file.

(jar is available on: https://github.com/SPARQL-Anything/sparql.anything/releases)

### CLI

    python3 -m unittest test/CSVtest.py test/JSONtest.py  test/XMLtest.py 


## Features

### File format support

- CSV
- JSON
- XML

### Mapping features

#### General (works everywhere)

- rr:template
- rml:reference (without spaces in name)
- rr:constant

#### rml:logicalSource

- rml:source
- rml:referenceFormulation

#### rr:subjectMap

- rr:class

#### rr:predicateObjectMap (support for multiple)

- rr:predicateMap
- rr:predicate (support for multiple)
- rr:objectMap
- rr:object

#### rr:objectMap

- rr:parentTriplesMap (only without join condition)

## Current issues

### General issues
- RMLTC0020b-CSV: using "path/../Danny" as an URI in SPARLQL Anything gives different behaviour than the RMLMapper
- RMLTC0002b-CSV: Blanknodes hash their input while RMLMapper uses the input as identifier
- RMLTC0006a-CSV: Spaces in constant values in CONSTRUCT (see ) crashes the SPARQL anything parser (test case files seem inconsistent)

### XML issues

- Possible issues because iterator of mapping is stricter then the iterator that is used in SPARQL Anything.

### Not implemented in SPARQL Anything
- Language tag
- Graph's
- Join conditions (combining multiple different files)
