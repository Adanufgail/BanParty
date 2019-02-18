#echo "making backup of banids.csv"
#nice -n 20 tar cvf - banids.csv |nice -n 15 xz -v -7 > banids.$(date +%Y-%m-%d.%H-%M).csv.gz
echo "combining banids.csv and banids.csv.temp"
cat banids.csv.temp >> banids.csv
echo "splitting files"
nice -n 19 split --verbose -a 4 -d -l 1000000 banids.csv tempfile
mv banids.csv banids.$(date +%Y-%m-%d.%H-%M).csv
for X in $(ls tempfile[0-9]*)
do
  echo $X
  for Y in $(ls tempfile[0-9]*)
  do
    echo $Y
    if [[ "x$X" = "x$Y" ]]
    then
      echo same, skipping
    else
      echo sorting and uniq $X and $Y
      cat $X $Y | nice -n 19 sort -u > $X.new
      sleep 2
      echo removing $Y from combo
      cat $X $X.new | nice -n 19 sort -u > $X.new2
      sleep 2
      echo cleanup
      mv $X.new2 $X
      rm $X.new
    fi
  done
  cat $X >> banids.csv
  rm $X
done
