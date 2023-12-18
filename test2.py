import time
import datetime

x=datetime.datetime.now()
day= x.day
month = x.month
year= x.year
hour= x.hour
minute = x.minute



current_time=datetime.datetime.now()
last_hour = current_time - datetime.timedelta(hours=1)


start_of_week = current_time.replace(hour=0,minute=0,second=0,microsecond=0) - datetime.timedelta(days=current_time.weekday())
end_of_week = start_of_week + datetime.timedelta(days=6)
end_of_week=end_of_week.replace(hour=23,minute=59,second=59,microsecond=999999)
print(start_of_week)
print(end_of_week,type(end_of_week))


# current_time = datetime.datetime.now()
# start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# end_of_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1)
# filtered_values = TemperatureSensorValue.objects.filter(
#     temperaturesensor=sensor,
#     time__range=[start_of_month, end_of_month]
# )