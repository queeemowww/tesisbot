import datetime

date = datetime.date.today()

date+= datetime.timedelta(days=1)

print(date.strftime('%d-%m-%y'))