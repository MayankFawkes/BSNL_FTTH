import tkinter
from tkinter import TOP, BOTTOM, HORIZONTAL, END, S, W, E, N
from tkinter import messagebox, ttk, PhotoImage, simpledialog
from requests import post, get, packages, Session, exceptions
from urllib3.exceptions import InsecureRequestWarning
from time import sleep, time, ctime
from re import findall
from functools import wraps
from threading import Thread
from webbrowser import open as openlink
import os, tempfile, base64, atexit

__author__ = "Mayank Gupta"
__version__ = "2.0.0"

class main(tkinter.Tk):
	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		self.title(f"BSNL FTTH v{__version__}")
		self.geometry("650x520")
		self.resizable(False, False)
		nameoficon = self.makeicon()
		self.iconbitmap(nameoficon.name)
		self.deleting_list = [nameoficon.name]
		s = ttk.Style()
		s.theme_use('clam')
		s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
		self.bind("<Escape>", lambda e: self.on_closing())
		self.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

	def makeicon(self):
		iconhexdata = b'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'
		
		with tempfile.NamedTemporaryFile(delete=False) as iconfile:
			iconfile.write(base64.b64decode(iconhexdata))

		return iconfile
	
	def on_closing(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.destroy()
			for n in self.deleting_list:
				os.remove(n)


class frameTOP(tkinter.Frame,):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.pack(side = TOP)

class INFObox(tkinter.Toplevel):
	def __init__(self,):
		super().__init__(root)
		self.title(f"Credits")
		# self.geometry("365x400")
		self.resizable(False, False)
		self.widget()

	def widget(self):
		tkinter.Label(self, text="Tech Solution & Gaming (Partner)", font=("TkDefaultFont", 15)).grid(row=0, column=0, columnspan=2, padx=10, pady=(25,5))

		tkinter.Button(self, text=f'Youtube', height="2", width="10", command=lambda: openlink("https://www.youtube.com/channel/UCFW1OrFlAOdvN8Nl09BKZyw")).grid(row=1, column=0, columnspan=2, padx=30, pady=30)

		tkinter.Label(self, text="Mayank Gupta (Owner)", font=("TkDefaultFont", 15)).grid(row=2, column=0, columnspan=2, padx=10, pady=(25,5))
		tkinter.Label(self, text="mayankfawkes@gmail.com", font=("TkDefaultFont", 10)).grid(row=3, column=0, columnspan=2, padx=10, pady=(5,15))

		tkinter.Button(self, text=f'Github', height="2", width="10", command=lambda: openlink("https://github.com/MayankFawkes")).grid(row=4, column=0, padx=30, pady=30)
		tkinter.Button(self, text=f'Website', height="2", width="10", command=lambda: openlink("https://mayankfawkes.xyz")).grid(row=4, column=1, padx=30, pady=30)

class frameBOTTOM(tkinter.Frame):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.pack(side = BOTTOM)

		self.processtest = tkinter.StringVar()

		self.isupdateaviable = tkinter.StringVar()
		self.isupdateaviable.set(f"<--- Click For Updates")

		self.widget()

		Thread(target=self.refresh).start()

	def SoftwareUpdate(self):
		ver, type = self.__http("update")
		self.logs(f'UPDATE: {ver}')
		if ver["latest"] == __version__:
			self.isupdateaviable.set("Update Not Available")
		else:
			openlink(ver["download"])
			self.isupdateaviable.set(f'Latest v{ver["latest"]} Available')

	def _http(self, type, data):
		types = {"get": get, "post": post}
		try:
			if data["type"] == "direct":
				res = types[type](data["link"], verify=False, headers=data["headers"], data=data["data"]).json()
				return res, data["type"]
			if data["type"] == "indirect":
				sess = Session()
				sess.headers.update(data["headers"])
				res = sess.post(url=data["link"], verify=False, data=data["data"]).json()
				self.logs(f'Location: {res}')
				if int(res["resultCode"]) == 200:
					dataSend = {"location":res["location"],
						"actionName":"manual",
						"_search":"false",
						"nd":int(time()*1000),
						"rows":4,
						"page":1,
						"sidx":"",
						"sord":"asc",}
					daa = sess.post("https://fuptopup.bsnl.co.in/fetchUserQuotaPM.do",verify=False,data=dataSend).json()
					return daa, data["type"]
			return dict(), None

		except exceptions.ConnectionError:
			messagebox.showerror("Connection","Internet not connected")

	def __http(self,need, phone=None):
		packages.urllib3.disable_warnings(category=InsecureRequestWarning)
		if need == "data":
			sett = self.settings()
			links = {
				# 1 : {"link": "http://117.247.44.144/mysmartportal/bsnlconnect6.0/bb_usage.php","type":"post",
				# "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, "data":{"userUsageforAuth":""}},
				2 : {"link": "https://redirect2.bbportal.bsnl.co.in/portal/fetchUserQuotaPM.do","type":"direct",
				"headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, "data":{}},
				4 : {"link": "https://redirect1.bbportal.bsnl.co.in/portal/fetchUserQuotaPM.do","type":"direct",
				"headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, "data":{}},
				3 : {"link": "https://fuptopup.bsnl.co.in/getLocationByIP.do","type":"indirect",
				"headers": {"User-Agent": "Mozilla"}, "data":{'actionName':'manual'}},
			}
			if sett:
				self.logs(f'SETTINGS: {sett}')
				data, type = self._http("post", links[sett])
				return data, sett, type
			for number, link in links.items():
				data, type = self._http("post", link)
				if int(data["resultCode"]) == 200:
					return data, number, type
			return {"resultCode": 404, "msg": "Contact admin with logs.txt"},None,"direct"
		if need == "update":
			link = {"link": "https://raw.githubusercontent.com/MayankFawkes/BSNL_FTTH/master/"
					"latest.json?flush_cache=True","type":"direct",
					"headers": {}, "data":{}}
			return self._http("get", link)

		if need == "bill":
			link = {"link": f"https://portal.bsnl.in/myBsnlApp/rest/billsummary/svctype/CDR/phoneno/{phone}",
					"type":"direct", "headers": {}, "data":{}}
			return self._http("get", link)

	def settings(self,number=None):
		if number:
			with open("SETTINGS","w") as file:
				file.write(f'{number}')
				file.close()
				return True
		try:
			return int(open("SETTINGS","r").read())
		except:
			return None

	def logs(self,mess):
		with open("logs.txt","a") as file:
			file.write(f"{ctime()}: {mess}\n")
			file.close()

	def fetch(self):
		r, number, type = self.__http("data")
		self.logs(f'FETCH: {r}, {number}, {type}')
		self.settings(number)
		data = dict()
		if type == "direct":
			data["status"] = r["resultCode"]
			data["msg"] = r["msg"]
			data["row"] = {}
			if "records" in r.keys():
				data["records"] = r["records"]
				for n in r["rows"]:
					if n["serviceType"].lower() == "BASE".lower():
						data["row"]["today"] = n["dailyTotalUsage"]
						data["row"]["totalUsed"] = n["totalUsage"]
						data["row"]["serviceName"] = n["serviceName"]
						tup = findall(r"U-([0-9]+)G-([0-9]+)Mbps-R-([0-9]+)Mbps", n["serviceName"])[0]
						for k,l,m in zip(tup, ["total", "speed", "afterspeed"],["GB","MBPS","MBPS"]):
							data["row"][l] = f"{k} {m}"
				return data
		if type == "indirect":
			data["status"] = r["resultCode"]
			data["msg"] = r["msg"]
			data["row"] = {}
			if "records" in r.keys():
				data["records"] = r["records"]
				for n in r["rows"]:
					if n["serviceType"].lower() == "Base".lower():
						data["row"]["today"] = n["dailyUsedOctets"]
						data["row"]["totalUsed"] = n["totalOctets"]
						data["row"]["serviceName"] = n["serviceName"]
						data["row"]["download"] = n["downloadOctets"]
						data["row"]["upload"] = n["uploadOctets"]
						try:
							tup = findall(r"HS-H-UPG-([0-9]+)MB-([0-9]+)G-([0-9]+)MB-GPON-M", n["serviceName"])[0]
							for k,l,m in zip(tup, ["speed", "total", "afterspeed"],["MBPS","GB","MBPS"]):
								data["row"][l] = f"{k} {m}"
						except:
							tup = findall(r"HS-H-UPG-([0-9]+.)MB-([0-9]+.?[0-9]*)TB-([0-9]+.?[0-9]*)MB-GPON-M", n["serviceName"])[0]
							tup = list(map(float, tup))
							tup[1] = tup[1]*1000
							for k,l,m in zip(tup, ["speed", "total", "afterspeed"],["MBPS","GB","MBPS"]):
								data["row"][l] = f"{k} {m}"

				return data
		return data

	def convert(self, val, type):
		if type == "GB":
			return float(val)
		return float(val)/1024.0

	def refresh(self):
		data = self.fetch()
		self.logs(f'REFRESH: {data}')
		avia = True
		values = {
			"today": self.Today,
			"upload": self.Upload,
			"download": self.Download, 
			"totalUsed": self.TotalUsed,
			"serviceName": self.Service,
			"total": self.Total,
			"speed": self.Speed,
			"afterspeed": self.FUP
		}

		if data["status"] is not 200:
			messagebox.showerror("Error", str(data["msg"]))
			avia = False
		
		if "records" in data.keys():
			if data["records"] < 1:
				messagebox.showerror("Error", str("No records found"))
				avia = False
		if avia:
			for n,m in data["row"].items():
				self.updateEntry(values[n],m)

			usedtillnow, typeU = findall('([0-9]+.?[0-9]*) ([A-Z]{2})', data["row"]["totalUsed"])[0]
			totalwehave, typeT = findall('([0-9]+.?[0-9]*) ([A-Z]{2})', data["row"]["total"])[0]

			usedtillnow = self.convert(usedtillnow, typeU)
			totalwehave = self.convert(totalwehave, typeT)

			self.logs(f'{usedtillnow}, {totalwehave}')

			percentage = (usedtillnow * 100)/totalwehave

			percentage = float(f"{percentage:.3f}")
			self.progress['value']=percentage
			self.update_idletasks()
			self.processtest.set(f'{percentage}% USED   {totalwehave-usedtillnow}GBs LEFT')

	def updateEntry(self, obj, s):
		obj["state"] = "normal"
		obj.delete(0, END)
		obj.insert(0,s)
		obj["state"] = "disable"

	def _get_html(self, artt):
		html = '<h1>Wait Loading...</h1><form action="https://mybillview.bsnl.co.in/BSNLSelfcare_OntheFlyV1.0.2/selfcare/OntheFly/statement" method="post">'
		for n, m in artt.items():
			html+=f'<input type="hidden" name="{n}", value="{m}">'
		html+='<input style="visibility:hidden;"id="submit" type="submit" value="Get Bill"></form><script>window.document.getElementById("submit").click()</script>'
		return html

	def _date(self, lst_date):
		months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
		date = ""
		for n in reversed(lst_date):
			try:date+=months[n.lower()]
			except:date+=n
		return date

	def _delete(self,name):
		sleep(8)
		os.remove(name)

	def open_bill(self):
		try:
			number = int(open("PHONE","r").read())
		except:
			number = simpledialog.askstring("Landline Number","Enter Number without 0.")
			with open("PHONE","w") as file:
				file.write(f'{number}')
				file.close()
		if number:
			self.logs(f'Number Found: {number}')
			data, type = self.__http("bill", phone=number)
			data = data["ROWSET"]["ROW"][0]

			self.logs(f'Original Data: {data}')

			raw = {
				"StatementIdentifier": "TEST",
				"SystemIdentifier": "CWSC",
				"InvoiceNumber": data["INVOICE_NO"],
				"BillingAccountNumber": data["ACCOUNT_NO"],
				"SSACode": data["SSA_CODE"],
				"InvoiceDate": self._date(data["INVOICE_DATE"].split("-")),
			}
			self.logs(f'Dict raw data: {raw}')
			
			with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as iconfile:
				iconfile.write(self._get_html(raw).encode())

			openlink(f"{iconfile.name}")
			self.master.deleting_list.append(iconfile.name)
			return True
		messagebox.showinfo("Landline","Landline number not found.")


	def widget(self):
		self.progress = ttk.Progressbar(self,orient=HORIZONTAL, style="red.Horizontal.TProgressbar", length=400, mode='determinate')
		self.progress.grid(row=0,column=0,columnspan=4,padx=10,pady=(25,2))

		tkinter.Label(self, textvariable=self.processtest).grid(row=1,column=0,columnspan=4,padx=10,pady=(2,25))
		labels =["Today", "Total Used", "Upload", "Download", "Service Name", "Total GBs", "Speed", "FUP Speed"]

		c = 0
		
		for n in range(2,int(len(labels)/2)+2):
			for m in [0,2]:
				tkinter.Label(self, text=labels[c]).grid(row=n,column=m,padx=10,pady=10)
				c+=1

		self.Today = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Today.grid(row=2,column=1,padx=10,pady=10)

		self.TotalUsed = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.TotalUsed.grid(row=2,column=3,padx=10,pady=10)

		self.Upload = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Upload.grid(row=3,column=1,padx=10,pady=10)

		self.Download = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Download.grid(row=3,column=3,padx=10,pady=10)

		self.Service = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Service.grid(row=4,column=1,padx=10,pady=10)

		self.Total = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Total.grid(row=4,column=3,padx=10,pady=10)

		self.Speed = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.Speed.grid(row=5,column=1,padx=10,pady=10)

		self.FUP = tkinter.Entry(self, state="disable", disabledforeground="black")
		self.FUP.grid(row=5,column=3,padx=10,pady=10)

		tkinter.Button(self, text="REFRESH", height=2, width=10, command=self.refresh).grid(row=6,column=0, padx=10,pady=20)

		tkinter.Button(self, text="INFO", height=2, width=10, command=INFObox).grid(row=6,column=1, padx=10,pady=20)

		tkinter.Button(self, text="UPDATE", height=2, width=10, command=self.SoftwareUpdate).grid(row=6,column=2, padx=10,pady=20)

		tkinter.Label(self, textvariable=self.isupdateaviable).grid(row=6,column=3, padx=10,pady=20)

		tkinter.Button(self, text="OPEN BILL", height=2, width=10, command=self.open_bill).grid(row=7,column=0,columnspan=4,padx=10,pady=(0,20),sticky=S+W+E+N)


class reglabel(tkinter.Label):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.grid(row=0,column=0,columnspan=2,padx=10,pady=(15,5))
		self.config(font=("TkDefaultFont", 25))

class reglabel1(tkinter.Label):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.grid(row=1,column=0,columnspan=2,pady=(5,10))
		self.config(font=("TkDefaultFont", 12))

if __name__ == '__main__':
	root = main()
	FrameOnTop = frameTOP(root)

	reglabel(FrameOnTop,text="BSNL FTTH Data Usage")
	reglabel1(FrameOnTop,text="Partner: Tech Solution & Gaming (Shubham Kushwaha)")

	FrameOnBOTTOM = frameBOTTOM(root)

	root.mainloop()
