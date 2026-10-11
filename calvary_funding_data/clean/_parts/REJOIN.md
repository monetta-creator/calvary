# Rejoin after cloning

```sh
cd calvary_funding_data/clean
cat _parts/fact_grants.csv.part* > fact_grants.csv
cat _parts/fact_org_relationships.csv.part* > fact_org_relationships.csv
```

fact_grants 928,658 rows; fact_org_relationships 544,041 rows (count with pandas).
