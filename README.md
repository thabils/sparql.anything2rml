# sparql.anything2rml

## Setup
To enable testing add a sparql anything jar to the project.
After this add the path from the root of the project to config.ini file.

(jar is available on https://github.com/SPARQL-Anything/sparql.anything/releases)

## Testing
    python3 -m unittest src/test.py 

## How to use

    python3 src/cli.py "MAPPING_FILENAME"

## TODO

- Graph support
- RefObjectMap support
- Language tag support
- Json support
- reference to triple map in an object map (see RMLTC0008b-CSV)

## Current issues

- RMLTC0020b-CSV: using "path/../Danny" as an URI in SPARLQL Anything gives different behaviour than the RMLMapper
- Blanknodes with a template existing out of more then 1 part eg "{firstName} {name}" are currently not possible in SPARLQL Anything
- Blanknodes hash there input while RMLMapper uses the input as identifier eg. _:Venus vs _:B7b29b0d7X2Dce2fX2D4737X2Dbb05X2D1a73df2f48ca
- Spaces in references (see RMLTC0010c-CSV) crashes SPARQL anything parser
- Spaces in CONSTRUCT (see RMLTC0006a-CSV) crashes the SPARQL anything parser 
