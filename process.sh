echo cull ban list
./cullbanlist.sh
echo cull safe list
./cullsafelist.sh
echo merge lists
nice -n 15 ./compare.sh
echo cull banids
nice -n 15 python ./culllist.py
