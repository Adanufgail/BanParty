wc -l banlist.csv
cat banlist.csv | sort | uniq > banlist2.csv; mv banlist2.csv banlist.csv
wc -l banlist.csv
