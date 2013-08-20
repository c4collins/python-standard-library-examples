import time

## 4.1.1 Wall Clock Time
print "The time is now:", time.time()
print "The time is now:", time.ctime()
print "The time in 15 seconds will be:", time.ctime(time.time()+15)

## 4.1.2 Processor Clock Time
import hashlib

# Data to use to calculate md5 checksums
data = open(__file__, 'rt').read()

for i in range(5):
	h = hashlib.sha1()
	print time.ctime(), ': %0.3f %0.3f' % (time.time(), time.clock())
	for i in range(300000):
		h.update(data)
	cksum = h.digest()

# calling sleep() yields control from the current thread and asks it to wait for the system to wake it back up
# If a program has only one thread this effectively blocks the app and it does no work.
for i in range(6, 1, -1):
	print 'Sleeping', i, 'seconds @', '%s : %0.2f %0.2f' % (time.ctime(), time.time(), time.clock())
	time.sleep(i)

## 4.1.3 Time Components
## the time module defines struct_Time for holding date and time values with components broken out so they are easy to access.
## Several functions work with struct time values instead of floats

def show_struct(s):
	print ' tm_year :', s.tm_year
	print ' tm_mon  :', s.tm_mon
	print ' tm_mday :', s.tm_mday
	print ' tm_hour :', s.tm_hour
	print ' tm_min  :', s.tm_min
	print ' tm_sec  :', s.tm_sec
	print ' tm_wday :', s.tm_wday
	print ' tm_yday :', s.tm_yday
	print ' tm_isdst:', s.tm_isdst
	return True

print 'gmtime:\n', show_struct(time.gmtime())
print '\nlocaltime:\n', show_struct(time.localtime())
print '\nmktime:\n', time.mktime(time.localtime())

## 4.1.4 Working with Time Zones
## Chaging the time zone doesn't change the actual time, just the way it's presented 
## or, rather, how the program represents time as different from the system time zone

# to set the time zone, set the environment variable TZ, then cal l tzset()

import time, os

def show_zone_info():
    print '  TZ     :', os.environ.get('TZ', "(not set)")
    print '  tzname:', time.tzname
    print '  Zone  : %d (%d)' % (time.timezone, time.timezone/3600)
    print '  DST   :', time.daylight
    print '  Time  :', time.ctime()
    
print 'Default :'
show_zone_info()
 
ZONES = ['GMT', 'Europe/Amsterdam',]
 
for zone in ZONES:
    os.environ['TZ'] = zone
    time.tzset()
    print  zone, ":"
    show_zone_info()
    
## 4.1.5 Parsing and Formatting Times
## strptime() and strftime() convert between struct_time and string representations of dates.

now = time.ctime()
print '\nNow:', now
parsed = time.strptime(now)
print '\nParsed:', show_struct(parsed)
print "Formatted:", time.strftime("%a %b %d %H:%M:%S %Y", parsed)