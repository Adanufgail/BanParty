echo "combining banids.csv and banids.csv.temp"
cat banids.csv banids.csv.temp > banidscombined.csv
echo "making backup of banids.csv"
mv banids.csv banids.$(date +%Y-%m-%d.%H-%M).csv
echo "splitting files"
split --verbose -d -l 1000000 banidscombined.csv banids
rm banidscombined.csv
for X in $(ls banids[0-9]*)
do
  echo $X
  for Y in $(ls banids[0-9]*)
  do
    echo $Y
    if [[ "x$X" = "x$Y" ]]
    then
      echo same, skipping
    else
      echo sorting and uniq $X and $Y
      cat $X $Y | sort | uniq > $X.new
      sleep 2
      echo removing $Y from combo
      cat $X $X.new | sort | uniq -d > $X.new2
      sleep 2
      echo cleanup
      mv $X.new2 $X
      rm $X.new
    fi
  done
  cat $X >> banids.csv
  rm $X
done
