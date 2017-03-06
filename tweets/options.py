"""
Declare key words, phrases, handles that if found in a tweet will exclude it
from deletion.

NOTE: DO *NOT* INCLUDE THE @ SYMBOL WHEN INCLUDING USER HANDLES.
FURTHER, MAKE SURE YOU ARE USING THE USER HANDLE AND NOT THE GENERAL NAME OF
THE ACCOUNT. THE USER HANDLE IS THE *UNIQUE* IDENTIFIER FOR YOUR ACCOUNT
AND IS THE NAME THAT INCLUDES THE "@" SIGN PREVIOUSLY MENTIONED.

For those unfamilier with python lists, each element is surrounded by single
OR double quotes and then a comma like so: 
KEY_WORDS = ["LOL", "Hello!", "Retween this", "Important"]

If you would like all tweets irrespective of likes and mentions/word contents
deleted, leave the values below unmodified.
"""
KEY_WORDS = []
LIKES = None
MAX = None
