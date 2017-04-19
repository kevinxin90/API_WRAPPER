import tornado.ioloop
import tornado.web
import requests
import json
import re
from utils import transform_json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")

class DgidbHandler(tornado.web.RequestHandler):
    def get(self, gene_id=None):
    	if gene_id:
	        new_doc = transform_json(gene_id)
	        self.write(new_doc)

APP_LIST = [
		('/', MainHandler),
        (r"/dgidb/(.+)/?", DgidbHandler)]

if __name__ == "__main__":
    app = tornado.web.Application(APP_LIST)

    app.listen(8899)
    tornado.ioloop.IOLoop.current().start()