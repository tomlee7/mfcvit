	#Tornado Libraries
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine

#Other Libraries
import urllib
#from passlib.hash import sha256_crypt as scrypt
import motor
from bson import json_util
import json
import requests
import os
#import urllib2
#import hashlib
from bson.objectid import ObjectId
import re
#import pymongo
#from utilityFunctions import sendMessage,sendRequestToken
import textwrap
import random
import csv
from datetime import datetime

db=motor.motor_tornado.MotorClient("mongodb://mfcvit:mfcvit@ds038379.mlab.com:38379/feedbackdb")['feedbackdb']
class IndexHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render('index.html')
class feedbackHandler(RequestHandler):
	@coroutine
	def post(self):
		name=self.get_argument('name')
		email=self.get_argument('email')
		feedback=self.get_argument('feedback')
		doc=yield db.users.find_one({"email":email})
		if not doc:
			doc=yield db.users.insert({"username":name,"email":email,"feedback":feedback})
			with open("feedback.csv","a+") as csvfile:
				writeCSV=csv.writer(csvfile)
				writeCSV.writerow([name,email,feedback])
			csvfile.close()
			self.redirect("/");
		else:
			self.redirect("/");


settings = dict(
		db=db,
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		debug=True)

application=Application([
(r"/", IndexHandler),
(r"/feedback",feedbackHandler)
],**settings)

if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(os.environ.get("PORT", 5000))
	IOLoop.current().start()
