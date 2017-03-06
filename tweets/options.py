"""
Declare key words/phrases and number of likes that will exclude a tweet from
being deleted by delete-the-tweets.py. Also define the max tweets searched
by delete-maintenance.py.

Notes on KEY_WORDS --------

NOTE 1: INCLUDE THE '@' SYMBOL WHEN INCLUDING USER HANDLES. User handles are
the unique 'user_name' of a twitter account and are easily found immediately
below a user's 'name' when viewing their bio/timeline. If still unclear,
please look at README for an example image.

NOTE 2: The script is case insensitive so whether you enter key words/phrases
as properly capitalized or not does not matter.

NOTE 3: Including the word 'RT' will prevent all retweets, excluding quoted,
from being deleted.

-------------

If you would like all tweets irrespective of likes and mentions/word contents
deleted, leave the values below unmodified.
"""
KEY_WORDS = []
LIKES = None
MAX = None
