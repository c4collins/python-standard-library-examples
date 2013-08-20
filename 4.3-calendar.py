## 4.3 Calendar
# The calendar class encapsulates calculatons for values such as dates of the week.
# Also includes the TextCalendar and HTMLCalendar classes which are useful for output
import calendar, pprint

## 4.3.1 Formatting Examples
# prmonth prints formatted text showing a month
c = calendar.TextCalendar(calendar.SUNDAY)
c.prmonth(2013, 8)
print
# HTMLCalendar will produce similar results, but contained in HTML markup
c = calendar.HTMLCalendar(calendar.SUNDAY)
print c.formatmonth(2013, 8)
print

cal = calendar.Calendar(calendar.SUNDAY)
cal_data = cal.yeardays2calendar(2013,3)
print 'len(cal_data)    :', len(cal_data)
top_months = cal_data[0]
print 'len(top_months)  :', len(top_months)
first_month = top_months[0]
print 'len(first_month) :', len(first_month)
print 'first_month:', pprint.pprint(first_month)

cal2 = calendar.TextCalendar(calendar.SUNDAY)
print "\n", cal2.formatyear(2013, 2, 1, 1, 3)

## 4.3.2 Calculating Dates
pprint.pprint(calendar.monthcalendar(2013,8))

# Determining the second Thursday in each month
for month in xrange(1, 13):
    # Compute the dates for each week that overlaps the month
    c = calendar.monthcalendar(2013, month)
    first_week = c[0]
    second_week=c[1]
    third_week = c[2]
    # if there is a Thursday in the first week, the second Thursday is in the second week
    # Otherwise it must be in the third week
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]
    
    print '%3s: %2s' % (calendar.month_abbr[month], meeting_date)