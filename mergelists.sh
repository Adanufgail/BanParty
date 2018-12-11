wc -l banids.csv*; cat banids.csv banids.csv.temp | sort | uniq > banids2.csv; mv banids2.csv banids.csv; wc -l banids.csv
