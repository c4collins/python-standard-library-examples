## 4.2 Datetime
# The datetime module contains tools for working with dates and/or times.
import datetime, time

## 4.2.1 Times
# Times are represented by hours, minutes, seconds, and microseconds in the time class
t = datetime.time(1, 2, 3)
print t
print 'Hour       :', t.hour
print 'Minute     :', t.minute
print 'Second     :', t.second
print 'Microsecond:', t.microsecond
print 'TZ-info    :', t.tzinfo

print '\nEarliest   :', datetime.time.min
print 'Latest     :', datetime.time.max
print 'Resolution :', datetime.time.resolution
print
# the resolution is limited to whole microseconds
for m in [1, 0, 0.1, 0.6]:
    try:
        print '%02.1f :' % m, datetime.time(0,0,0,microsecond=m)
    except TypeError, err:
        print 'ERROR:', err
print
## 4.2.2 Dates
# Calendar dates are represented with year, month, and day in the date class

today = datetime.date.today()
print today
print 'ctime :', today.ctime()
tt = today.timetuple()
print 'tuple : tm_year  =', tt.tm_year
print '        tm_mon   =', tt.tm_mon
print '        tm_mday  =', tt.tm_mday
print '        tm_hour  =', tt.tm_hour
print '        tm_min   =', tt.tm_min
print '        tm_sec   =', tt.tm_sec
print '        tm_wday  =', tt.tm_wday
print '        tm_yday  =', tt.tm_yday
print '        tm_isdst =', tt.tm_isdst
print '\nOrdinal:', today.toordinal()
print 'Year   :', today.year
print 'Month  :', today.month
print 'Day    :', today.day
print
# Reformatting dates
o = 733114
print 'o               :', o
print 'fromordinal(o)  :', datetime.date.fromordinal(o)
t = time.time()
print 't               :', t
print 'fromtimestamp(t):', datetime.date.fromtimestamp(t)

# Range of available date values
print '\nEarliest   :', datetime.date.min
print 'Latest     :', datetime.date.max
print 'Resolution :', datetime.date.resolution
# resolution is 1 day

# It is easy to update dates to create new ones
d1 = datetime.date.fromordinal(o+16)
print '\nd1:', d1.ctime()
d2 = d1.replace(year=2013)
print 'd2:', d2.ctime()

## 4.2.3 timedeltas
# Future and past dates can be calculated using basic arithmetic on two datetime objects
# or by combining a datetime with a timedelta.
# Subtracting dates returns a timedelta, and a timedelta can be added to 
# or subtracted from a date to produce another date.
# Timedeltas are stored internally as days, seconds, and microseconds.

print '\nmicroseconds:', datetime.timedelta(microseconds=1)
print 'milliseconds:', datetime.timedelta(milliseconds=1)
print '     seconds:', datetime.timedelta(seconds=1)
print '     minutes:', datetime.timedelta(minutes=1)
print '       hours:', datetime.timedelta(hours=1)
print '        days:', datetime.timedelta(days=1)
print '       weeks:', datetime.timedelta(weeks=1)
print

for delta in [ datetime.timedelta(microseconds=1), 
                datetime.timedelta(milliseconds=1), 
                datetime.timedelta(seconds=1), 
                datetime.timedelta(minutes=1), 
                datetime.timedelta(hours=1), 
                datetime.timedelta(days=1), 
                datetime.timedelta(weeks=1)]        :
    print '%15s = %s seconds' % (delta, delta.total_seconds())

## 4.2.4 Date Arithmetic
# Standard arithmetic operators work on dates
print '\nToday    :' ,today
one_day = datetime.timedelta(days=1)
print 'One Day  :', one_day
print 'Yesterday:', today - one_day
print 'Tomorrow :', today + one_day
print '\nyesterday - tomorrow:', (today - one_day) - (today + one_day)
print 'tomorrow - yesterday:', (today + one_day) - (today - one_day)

## 4.2.5 Comparing Values
# Standard comparison operators also work on dates
print 't\nTimes:'
t1 =datetime.time(12,55,0)
print ' t1:', t1
t2 = datetime.time(13,5,0)
print ' t2:', t2
print ' t1 < t2:', t1 < t2

print '\nDates:'
d1 = datetime.date.today()
print ' d1:', d1
d2 = datetime.date.today() + datetime.timedelta(days=1)
print ' d2:', d2
print ' d1 > d2:', d1 > d2

## 4.2.6 Combining Dates and Times
# The datetime class holds values with both date and time components

print '\nNow    :', datetime.datetime.now()
print 'Today  :', datetime.datetime.today()
print 'UTC Now:', datetime.datetime.utcnow()
print

FIELDS = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond',]
d = datetime.datetime.now()
for attr in FIELDS:
    print '%15s: %s' % (attr, getattr(d, attr))
    
t= datetime.time(1,2,3)
print '\nt :', t
d = datetime.date.today()
print 'd :', d
dt = datetime.datetime.combine(d,t)
print 'dt:', dt

## 4.2.7 Formatting and Parsing
# ISO-8601 date format is YYYY-MM-DDTHH:MM:SS.mmmmmm, alternate formats can be generated with strftime()
format = "%a %b %d %H:%M:%S %Y"
print "\nISO     :", today
s =  today.strftime(format)
print 'strftime:', s
d = datetime.datetime.strptime(s, format)
print 'strptime:', d.strftime(format)


## 4.2.8 time Zones
# Within datetime, time zones are represented by subclasses of tzinfo.
# but datetime doesn't include a useful implementation