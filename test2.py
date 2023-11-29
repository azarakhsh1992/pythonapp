import time
import datetime

x=datetime.datetime.now()
x=str(x)
x= datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
js = {"time":x}
print(js)
print(x, type(x))
