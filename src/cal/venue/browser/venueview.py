from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VenueView(BrowserView):
    __call__ = ViewPageTemplateFile('venueview.pt')
