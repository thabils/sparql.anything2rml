# sparql.anything2rml

## Setup

    pip install -r requirements.txt

To enable testing add a sparql anything jar to the project.
After this add the path from the root of the project to config.ini file.

(jar is available on https://github.com/SPARQL-Anything/sparql.anything/releases)

## Testing

    python3 -m unittest src/test.py 

## How to use

To generate a SPARQL Anything file:

    python3 src/cli.py "MAPPING_FILENAME" create

To generate a SPARQL Anything file and generate it's output:

    python3 src/cli.py "MAPPING_FILENAME" generate

## Current features

### File support

- CSV
- JSON (has issues with numbers)

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
- RMLTC0010c-CSV: Spaces in reference names crashes SPARQL anything parser
- RMLTC0006a-CSV: Spaces in constant values in CONSTRUCT (see ) crashes the SPARQL anything parser (test case files seem inconsistent)

### JSON related

- RMLTC0002a-JSON: SPARQL Anything doesn't accept numbers as values 

## Not implemented in SPARQL Anything
- Language tag
- Graph's
- Join conditions (combining multiple different files)

## TODO

