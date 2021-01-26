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

# Data sample schema: 

# [
#   "COUNTER",
#   "INTERPOLATED",
#   "AF3","T7","Pz","T8","AF4",
#   "RAW_CQ",
#   "MARKER_HARDWARE",
#   "MARKERS"
# ]

# e.g. "eeg":[93,0,4146.667,4485.641,4166.154,4222.051,4132.308,450.0,0,[]]

# channels indexes = eeg[2], ..., eeg[6]
# Streamer().sub(['eeg'])