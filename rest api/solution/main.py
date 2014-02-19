import os
import json

import tornado.ioloop
import tornado.web
import tornado.template

word_list = []

def _get_word_stats():
    stats = {}
    for word in word_list:
        if word not in stats:
            stats[word] = 1
        else:
            stats[word] += 1
    return stats

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("word.html")


class WordHandler(tornado.web.RequestHandler):
    """Handler for specific instances
    """

    def get(self):
        self.render("word.html")

    def put(self):
        word = self.get_argument('word')
        word_parts = word.strip().split(" ")
        self.set_header('Content-type', "application/json")
        if len(word_parts) > 1:
            self.set_status(405)
            ret = json.dumps({'error': "PUT requests must be one word in length"})
        else:
            print "adding word %s" % word
            word_list.append(word)
            self.set_status(200)
            ret = json.dumps(_get_word_stats())
        self.write(ret)


class WordsHandler(tornado.web.RequestHandler):
    """Assumes a list of words to be returned
    """

    def get(self, word=None):
        self.set_header('Content-type', "application/json")
        self.set_status(200)
        if word: # the word parameter was passed in (/words/<word>)
            words = _get_word_stats()
            if word in words:
                ret = json.dumps({word: words[word]})
            else:
                ret = json.dumps({word: 0})
        else: # the word parameter was not passed in 
            ret = json.dumps(_get_word_stats())
        self.write(ret)


# initialize settings, routing
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))               
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/word", WordHandler),
    (r"/words", WordsHandler),
    (r"/words/(.*)", WordsHandler),
], **settings)

if __name__ == "__main__":
    # start the app
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
