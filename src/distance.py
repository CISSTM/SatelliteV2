import datetime
now = datetime.datetime.now()
afternow = datetime.datetime.now()
print (now)
print (afternow)
diff = afternow - now
print (diff.microseconds)
