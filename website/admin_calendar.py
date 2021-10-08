from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event


class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events





    def formatday(self, day, weekday, events):
            """
                    Return a day as a table cell.
                    """


            events_per_day = events.filter(day__day=day)
            d =''
            events_html = "<a>"



            for event in events_per_day:
                d += f'<li> {event.notes} </li>'

                events_html +=event.title+"<a>""<p>"+str(event.start_time.strftime("%I:%M %p")+"<br>" + str(event.end_time.strftime("%I:%M %p")) )+"<br>"+ event.notes+ "<br>"



            events_html += "</p>"





            if day == 0:
                return '<td class="noday">&nbsp;</td>'  # day outside month
            else:
                return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(day__month=themonth)

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

