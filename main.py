import praw
import time
import os
import config

DB_PATH = "comments_replied_to.txt"
REPLY_PATH = "text.txt"

def process_reply(middle_text):
    with open(REPLY_PATH, "r") as f:
        reply = f.read()
        new_reply = reply.replace("*", middle_text)
    return new_reply

def fetch_db():
    if not os.path.isfile(DB_PATH):
        db = []
    else:
        with open(DB_PATH, "r") as f:
           db = f.read()
           db = db.split("\n")
           db = list(filter(None, db))
    return db

def append_db(comments):
    with open(DB_PATH, "a") as f:
        for comment in comments:
            f.write(comment + "\n")

def bot_login():
    r = praw.Reddit(
        username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = config.user_agent
        )
    return r

def run_bot(reddit, comments_replied_to):
    new_comments = []
    for comment in reddit.redditor(config.username_to_reply).comments.new(limit=3):
        if comment.id not in comments_replied_to:
            reply = process_reply(comment.subreddit.display_name)
            comment.reply(reply)

            print("Replied to comment " + comment.id)
            new_comments.append(comment.id)
        time.sleep(4)
    append_db(new_comments)
    

db = fetch_db()
reddit = bot_login()
run_bot(reddit, db)