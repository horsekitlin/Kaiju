import pymongo
from bson.objectid import ObjectId
from pymongo import Connection
from pymongo.database import Database

 # connect
connection = Connection()
db = Database(connection, "kaiju")


text_file = open('zhottp.ssv')
for line in enumerate(text_file.readlines()):
    word_arr = list(line)
    words = [str(w).replace('\n', '') for w in word_arr ]
   # word_arr = line.split(' ')
    db.words.insert({ "count":words[0], "word":words[1].split(' ')[0], "phonetic":words[1].split(' ')[1] })
