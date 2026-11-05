# Farsi Horoscope Calendar

A static page (`index.html`) and an iCalendar feed (`calendar.ics`). No build step, no dependencies.

## Verifying your work

```checks
python3 -I -c "from html.parser import HTMLParser; HTMLParser().feed(open('index.html', encoding='utf-8').read())"
grep -q '^BEGIN:VCALENDAR' calendar.ics
grep -q '^END:VCALENDAR' calendar.ics
```
