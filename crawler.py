# coding: utf-8
import praw
import json

r = praw.Reddit(user_agent='raketbewijs')

subreddits = []
try:
    with open('subreddits.txt') as f:
        subreddits = f.read().splitlines()
except IOError, OSError:
    print 'File subreddits.txt not found!'
print 'Found {0} subreddits.'.format(len(subreddits))

posts = {}
try:
    posts = json.load(open('posts.json'))
except IOError, OSError:
    print 'File posts.json not found!'
nr_posts = sum([len(posts[sr]) for sr in [s for s in posts]])
print 'Found {0} populated subreddits with {1} posts.'.format(len(posts), nr_posts)

for subreddit in subreddits:
    print 'Processing {0}'.format(subreddit)
    submissions = r.get_subreddit(subreddit).get_new(limit=1000)

    nr_submissions_added = 0
    nr_submissions = 0
    if subreddit not in posts:
        posts[subreddit] = {}
    for submission in submissions:
        nr_submissions = nr_submissions + 1
        if submission.id not in posts[subreddit]:
            nr_submissions_added = nr_submissions_added + 1
            posts[subreddit][submission.id] = [submission.title, submission.selftext]
    print '    Added {0} of {1} submissions.'.format(nr_submissions_added, nr_submissions)
    print '    We now have {0} submissions for {1}.'.format(len(posts[subreddit]), subreddit)

new_nr_posts = sum([len(posts[sr]) for sr in [s for s in posts]])
print 'In total we now have {0} subreddits, with {1} posts ({2} new).'.format(len(posts), new_nr_posts, new_nr_posts-nr_posts)

json.dump(posts, open("posts.json", 'w'))
