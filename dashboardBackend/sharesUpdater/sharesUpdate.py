from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
from datetime import timedelta
import zipfile
import pandas as pd
import os
import time
import datetime
import redislite
import pyarrow as pa
from django.conf import settings

def redis_connection():
	redis_instance = redis_instance = redislite.Redis('/tmp/redis.db')
	return redis_instance

def webdriver_options_setup():
	op = webdriver.ChromeOptions()
	op.add_argument("start-maximized")
	op.add_argument("--disable-blink-features=AutomationControlled")
	op.add_argument("--window-size=1920,1080")
	op.add_argument("--allow-insecure-localhost")
	op.add_argument("--headless")
	op.add_argument('--disable-dev-shm-usage')
	op.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
	return op

def is_file_downloaded(filename, timeout):
    end_time = time.time() + timeout
    print(filename)
    while not os.path.exists(filename):
        time.sleep(1)
        if time.time() > end_time:
            print("File not found within time")
            return False

    if os.path.exists(filename):
        print("File found")
        return True

class downloadShares:
	download_dir = "downloads" #Change the path to download directory
	csv_name = download_dir+"\\"
	zip_name = download_dir+"\\"
	day = ""
	month = ""
	year = ""
	web = webdriver.Chrome(options=webdriver_options_setup())
	prevDt = ""

	def set_file_name(self):
		self.zip_name += "EQ"+str(self.day)+str(self.prevDt.strftime('%m'))+str(self.prevDt.strftime('%y'))+"_CSV.ZIP"
		self.csv_name += "EQ"+str(self.day)+str(self.prevDt.strftime('%m'))+str(self.prevDt.strftime('%y'))+".CSV"

	def enable_download(self):
	    self.web.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
	    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.download_dir}}
	    self.web.execute("send_command", params)

	def get_zip(self):
	    url = 'https://www.bseindia.com/download/BhavCopy/Equity/'
	    url = url + self.zip_name.split('/')[1]
	    self.web.get(url)

	    return is_file_downloaded(self.zip_name,5)

	def webdriver_setup(self):
		self.enable_download()
		self.web.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Chrome/83.0.4103.53 Safari/537.36'})
		self.web.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.web.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})

	def extract_zip(self):
		with zipfile.ZipFile(self.zip_name,"r") as zip_ref:
			zip_ref.extractall(self.download_dir)
		os.remove(self.zip_name)

	def read_csv(self):
		df = pd.read_csv(self.csv_name)
		return df

	def set_date(self):
		dt = date.today()
		weekDay = dt.weekday()
		print(weekDay)
		if weekDay == 6:
			self.prevDt = dt - timedelta(days=2)
		elif weekDay == 5:
			self.prevDt = dt - timedelta(days=1)
		elif weekDay == 0 and datetime.datetime.now().hour < 18:
			self.prevDt = dt - timedelta(days=3)
		else:
			self.prevDt = dt
		self.day = self.prevDt.strftime("%d")
		self.month = self.prevDt.strftime("%b")
		self.year = self.prevDt.strftime("%Y")
		print(self.day + "-" + self.month + "-" + self.year)

	def getShares(self):
		print("Inside getShares")
		if self.get_zip():
			print("If zip downloaded")
			self.extract_zip()
			df = self.read_csv()
		return df


def getNewSharesList():
	ob = downloadShares()
	ob.set_date()
	ob.set_file_name()
	ob.webdriver_setup()
	df = ob.getShares()
	rcon = redis_connection()
	df = df[['SC_CODE','SC_NAME','OPEN','CLOSE','LOW','HIGH']]
	df.columns = ["code","name","openPrice","closePrice","lowPrice","highPrice"]
	print(len(df))
	setCacheData(rcon,"share",df)

def setCacheData(r,key,value):
	context = pa.default_serialization_context()
	r.set(key,context.serialize(value).to_buffer().to_pybytes())
	r.persist(key)