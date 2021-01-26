from cortex import Cortex
from dotenv import load_dotenv
load_dotenv()
import os

class Streamer():
	def __init__(self):
		user = {
			"license" : os.environ.get("LICENSE_KEY"),
			"client_id" : os.environ.get("CLIENT_ID"),
			"client_secret" : os.environ.get("CLIENT_SECRET"),
			"debit" : 1
		}
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def sub(self, streams):
		self.c.sub_request(streams)

Streamer().sub(['eeg'])