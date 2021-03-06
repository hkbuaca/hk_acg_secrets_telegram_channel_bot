import json
import logging

from flask import Flask, redirect
from google.appengine.ext import deferred

from apis.facebook_feed import get_page_feed, get_post_async
from database import StoryPost

app = Flask(__name__)


@app.route('/')
def hello():
    logging.debug(redirect("https://t.me/hk_acg_feeds", code=302))
    return redirect("https://t.me/hk_acg_feeds", code=302)


def task(stories, which_board):
    def check_story(rpc):
        try:
            result = rpc.get_result()
            fb_object = json.loads(result.content)
            # if story and story.get('score') >= 100:
            story = StoryPost.cvt_FBObject_StoryPost(fb_object)
            StoryPost.add(story, which_board)
        # except urlfetch.DownloadError as ex:
        #   logging.exception(ex)
        except Exception as e:
            logging.exception(e)
            
    # TODO: don't fetch already loaded (>=150 score) stories
    # logging.debug(stories)
    stories_new = filter(lambda id: not StoryPost.checkPostIdAlreadyExist(id), stories)
    rpcs = map(lambda id: get_post_async(id, check_story), stories_new)
    for rpc in rpcs:
        rpc.wait()


def pick_id(result, limit=100):
    lst = map(lambda e: e['id'], result['data'])
    ret = [lst[i::limit] for i in xrange(limit)]
    ret = ret[::-1]  # list(reversed(ret))
    # logging.debug(ret)
    return ret


@app.route('/cron/pink')
def cron_pink():
    stories = get_page_feed('pink')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'pink')
    logging.debug('OK')
    return 'OK'


@app.route('/cron/blue')
def cron_blue():
    stories = get_page_feed('blue')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'blue')
    logging.debug('OK')
    return 'OK'


@app.route('/cron/black')
def cron_black():
    stories = get_page_feed('black')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'black')
    logging.debug('OK')
    return 'OK'


@app.route('/cron/cos')
def cron_cos():
    stories = get_page_feed('cos')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'cos')
    logging.debug('OK')
    return 'OK'


@app.route('/cron/music_plastic')
def cron_music_plastic():
    stories = get_page_feed('music_plastic')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'music_plastic')
    logging.debug('OK')
    return 'OK'


@app.route('/cron/maid')
def cron_maid():
    stories = get_page_feed('maid')
    if stories is None:
        logging.debug('stories is none')
        return 'stories is none', 500
    chunks = pick_id(stories, 50)
    for chunk in chunks:
        deferred.defer(task, chunk, 'maid')
    logging.debug('OK')
    return 'OK'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    logging.debug('?_?', 404)
    return '?_?', 404


@app.errorhandler(500)
def application_error(e):
    logging.exception(e)
    """Return a custom 500 error."""
    logging.debug('xx( : {}'.format(e))
    return 'xx( : {}'.format(e), 500
