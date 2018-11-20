# BanParty

This program is a further modification of melissa mcewen's modification of Quincy Larson's tweet deletion Python script. This is a Python 2 script that imports a file named banlist.csv that contains one Twitter ID per line and nothing else. 

It should be noted that I've found conflicting information about Twitter's rate limiting, as some say the 15 per 15 minutes holds true, others say it could be more. I took the cautious approach and did the following workflow:

1. Get list of users followers and dump them to banids.csv
2. Wait 30 seconds then repeat for each user in banlist.csv
3. Remove duplicates
4. Block and file a spam report on every one, waiting 30 seconds between each.
5. If there's an error, try to again once, then move on.

This, in an ideal environment, has the potential to block 1440 people per day. It's SLOW. On purpose.


Sources:

https://medium.com/@melissamcewen/how-to-completely-delete-your-twitter-likes-5a41c35aefb8

https://gist.github.com/melissamcewen/37125ee31615f3f7f53de47459053bf1#file-unlike-py

https://medium.freecodecamp.org/how-to-delete-your-past-tweets-in-bulk-and-for-free-save-yourself-from-your-past-self-f8844cdbda2

https://github.com/QuincyLarson/delete-tweets
