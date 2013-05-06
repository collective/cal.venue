from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from plone.memoize import ram
import time
import pycountry


def _fixed_cache_key(method, self, *args, **kwargs):
    # caches for a fixed amount of time
    ts = time.time() // (60*60) # time() in sec. 60sec * 60min = 1h
    return (self.context, ts, args, kwargs)


class VenueView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @ram.cache(_fixed_cache_key)
    def venue_events(self):
        wft = getToolByName(self.context, 'portal_workflow')
        refs = self.context.getBRefs('isVenueForEvent')
        events = []
        now = DateTime()
        for item in refs:
            try:
                wf_state = wft.getInfoFor(item, 'review_state', '')
                if (item.start() > now or item.end() > now)\
                   and wf_state == 'published':
                    events.append(item)
            except:
                pass
        return sorted(events, key=lambda x: (x.start()))

    @property
    def state(self):
        state = pycountry.countries.get(numeric=self.context.state)
        return state.name

    # peel this out into something more generic
    def make_date(self, date):
        if not isinstance(date, DateTime):
            date = DateTime(date)
        return date

    def localized_month(self, date):
        date = self.make_date(date)
        util = getToolByName(self.context, 'translation_service')
        month = util.translate(util.month_msgid(date.month()),
                       domain='plonelocales',
                       context=self.context)
        return month

    def localized_month_abbr(self, date):
        date = self.make_date(date)
        util = getToolByName(self.context, 'translation_service')
        month = util.translate(util.month_msgid(date.month(), 'a'),
                       domain='plonelocales',
                       context=self.context)
        return month

    def localized_day(self, date):
        date = self.make_date(date)
        util = getToolByName(self.context, 'translation_service')
        day = util.translate(util.day_msgid(date.dow()),
                       domain='plonelocales',
                       context=self.context)
        return day

    def day(self, date):
        date = self.make_date(date)
        return date.day()

    def dayz(self, date):
        date = self.make_date(date)
        return date.dd()

    def year(self, date):
        date = self.make_date(date)
        return date.year()

    def time(self, date):
        date = self.make_date(date)
        minute = str(date.minute())
        if len(minute) == 1:
            minute = '0%s' % (minute,)
        return '%s:%s' % (date.hour(), minute)
