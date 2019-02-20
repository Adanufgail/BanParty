#echo "making backup of banids.csv"
#nice -n 20 tar cvf - banids.csv |nice -n 15 xz -v -7 > banids.$(date +%Y-%m-%d.%H-%M).csv.gz
mkdir temp
echo "combining banids.csv and banids.csv.temp"
cat banids.csv.temp >> banids.csv
echo "splitting files"
nice -n 19 split --verbose -a 6 -d -l 100000 banids.csv temp/tempfile
for X in $(ls temp/tempfile[0-9]*)
do
  echo $X
  for Y in $(ls temp/tempfile[0-9]*)
  do
    echo $Y
    if [[ "x$X" = "x$Y" ]]
    then
      echo same, skipping
    else
      echo sorting and uniq $X and $Y
      cat $X $Y | sort -u > $X.new
      echo  sleeping
      sleep 2
      echo removing $Y from combo
      cat $X $X.new | sort -u > $X.new2
      echo  sleeping
      sleep 2
      echo cleanup
      mv $X.new2 $X
      rm $X.new
    fi
  done
  cat $X >> banids.$(date +%Y-%m-%d.%H-%M).csv
  rm $X
done
