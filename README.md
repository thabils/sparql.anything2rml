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
- Json support
- reference to triple map in an object map (see RMLTC0008b-CSV)

## Current issues

- RMLTC0020b-CSV: using "path/../Danny" as an URI in SPARLQL Anything gives different behaviour than the RMLMapper
- Blanknodes hash their input while RMLMapper uses the input as identifier eg. _:Venus vs _:B7b29b0d7X2Dce2fX2D4737X2Dbb05X2D1a73df2f48ca
- Spaces in reference names (see RMLTC0010c-CSV) crashes SPARQL anything parser
- Spaces in constant values in CONSTRUCT (see RMLTC0006a-CSV) crashes the SPARQL anything parser 
- Language tag doesn't seem supported in sparql anything
