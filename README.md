# BanParty
In the wake of BlockTogether not supporting accounts with more than 200K Blocks, and with the Twitter Blockchain app crashing out after 3-10K blocks from a user, it was necessary for me to craft my own tool to block large scale users on Twitter. It's become obvious that Twitter will never have improved controls for moderation, nor will they ever take threats, dangerous rhetoric, and the spread of blatant propaganda seriously.

This program is a further modification of melissa mcewen's modification of Quincy Larson's tweet deletion Python script. This is a Python 2 script that imports a file named banlist.csv that contains one Twitter ID per line and nothing else. 

load.py loads the list of Twitter handles from banlist.csv and compiles a list of their IDs and the IDs of all of their followers in banids.csv.

block.py goes through banids.csv and bans every single one. With the Twitter Python API's wait command, if you go over the rate limit, it just pauses the script, so the wait functions aren't necessary.

count.py dumps a list of all currently blocked IDs to allbanids.csv. Mine (@mlubert) is currently there as an example, with nearly 1 million blocks of GG supporters, Trump Supporters, Known Bots and Harassers, and people critical of MeToo, The Russia Probe, Supporters of Kavanaugh, all businesses known ot advertise on Twitter, etc. If you want to remove scum, it's a good start. It's likely there are bad blocks in there that should be removed, but it will not be edited except to add entries. You are free to create your own curated lists.


Sources:

https://medium.com/@melissamcewen/how-to-completely-delete-your-twitter-likes-5a41c35aefb8

https://gist.github.com/melissamcewen/37125ee31615f3f7f53de47459053bf1#file-unlike-py

https://medium.freecodecamp.org/how-to-delete-your-past-tweets-in-bulk-and-for-free-save-yourself-from-your-past-self-f8844cdbda2

https://github.com/QuincyLarson/delete-tweets
