echo cull ban list
./cullbanlist.sh
echo cull safe list
./cullsafelist.sh
echo merge lists
./compare.sh
echo cull banids
python ./culllist.py
