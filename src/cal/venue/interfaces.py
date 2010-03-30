# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
from zope.interface import Interface

class IVenueFolder(Interface):
    """ Marker interface for VenueFolders
    """

class IVenue(Interface):
    """ Marker interface for Venues
    """

class IEventVenue(Interface):
    """ Marker interface for ATEvents to provide venue information
    """