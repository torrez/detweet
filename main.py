#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os 
import time

import tornado.ioloop
import tornado.web
import tornado.auth
from tornado.escape import json_encode, json_decode
from tornado.options import define, options

define('on_port', default=5000, help="Run on port")
define('twitter_consumer_key', default=os.environ['twitter_consumer_key'])
define('twitter_consumer_secret', default=os.environ['twitter_consumer_secret'])
#see this gist for a Tornado cookie secret: https://gist.github.com/didip/823887
define('cookie_secret', default=os.environ['cookie_secret'])

class BaseHandler(tornado.web.RequestHandler):
    """
    Gives every handler the ability to decrypt the Twitter user saved
    in the secure cookie.
    """
    def get_current_user(self):
        user = self.get_secure_cookie('user_id')
        if user:
            return json_decode(user)
        else:
            return None

class MainHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if user:
            self.write("<a href=\"/bye-bye\">disable retweets for everyone</a><br>")
            self.write("<a href=\"/sign-out\">sign out</a>")
        else:
            self.write("<a href=\"/sign-in\">sign in</a>")


class SignInHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie('user_id', json_encode(
                {
                    'screen_name': user['screen_name'], 
                    'id': user['id'],
                    'access_token': user['access_token']
                })
            )
            self.redirect("/")
        else:
            yield self.authorize_redirect()


class SignOutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user_id")
        return self.redirect("/")


class ByeByeHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #get everyone i follow
        friend_ids = yield self.twitter_request(
            "/friends/ids",
            count=5000,
            access_token=self.current_user["access_token"])
        for id in friend_ids['ids']:
            self.write("User #{0}…".format(id))
            self.flush()
            yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + .1)
            try:
                friend = yield self.twitter_request(
                    "/friendships/update",
                    post_args={"user_id": id, "retweets": "false"},
                    access_token=self.current_user["access_token"])
                self.write("DETWEETED!<br>")
            except:
                self.write("DIDN’T WORK!<br>")
        self.finish("We’re Done!")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/sign-in", SignInHandler),
    (r"/sign-out", SignOutHandler),
    (r"/bye-bye", ByeByeHandler),
], twitter_consumer_key=options.twitter_consumer_key, 
twitter_consumer_secret=options.twitter_consumer_secret,
cookie_secret=options.cookie_secret)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(int(options.on_port))
    tornado.ioloop.IOLoop.instance().start()



