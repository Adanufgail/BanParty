wc -l allbanids.csv
cat allbanids.csv | sort | uniq > allbanids2.csv; mv allbanids2.csv allbanids.csv
wc -l allbanids.csv
