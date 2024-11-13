#!/bin/bash
version=$(bin/neo4j-admin --version | cut -d '.' -f 1)
if [[ $version -ge 5 ]]; then
	bin/neo4j-admin database import full --delimiter="\t" --array-delimiter="|" --quote="'" --overwrite-destination=true --skip-bad-relationships=true --skip-duplicate-nodes=true neo4j 
else
	bin/neo4j-admin import --delimiter="\t" --array-delimiter="|" --quote="'" --force=true --skip-bad-relationships=true --skip-duplicate-nodes=true --database=neo4j 
fi