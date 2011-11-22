# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
__author__ = """Johannes Raggam <johannes@raggam.co.at>"""
__docformat__ = 'plaintext'

from zope.component import adapts
from zope.interface import implements

try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.ATContentTypes.interfaces import IATEvent
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.field import ExtensionField
from cal.venue.interfaces import IEventVenue

class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    pass

class TextFieldExtender(ExtensionField, atapi.TextField):
    pass

class ATEventExtender(object):
    implements(IOrderableSchemaExtender) # Even if the order is not modified,
                                         # other packages which subclass this
                                         # one should be able to reorder fields
    adapts(IATEvent)

    fields = [
        ReferenceFieldExtender("venue",
            required=False,
            searchable=True,
            languageIndependent=True,
            relationship='isVenueForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            vocabulary_display_path_bound=-1, # Avoid silly Archetypes object title magic
            enforceVocabulary=True,
            widget=atapi.ReferenceWidget(
                description = '',
                label = _(u'label_event_location', default=u'Event Location'),
                checkbox_bound=1, # use selection widget
                ),
            ),
        TextFieldExtender('venue_notes',
            required=False,
            searchable=True,
            default_content_type = 'text/plain',
            allowable_content_types = ('text/plain',),
            widget=atapi.TextAreaWidget(
                label = _(u'label_event_venue_notes',
                          default=u'Alternativer Veranstaltungsort'),
                description = _(u'description_event_venue_notes',
                                default=u'Alternativer Veranstaltungsort oder '\
                                u'Zusatztext zum Veranstaltungsort'),
                rows = 3,
                allow_file_upload=False,
                ),
            ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, order):
        schemata_default = order['default']
        schemata_default.remove('venue')
        schemata_default.remove('venue_notes')

        idx = schemata_default.index('endDate')
        schemata_default.insert(idx+1, 'venue')
        schemata_default.insert(idx+2, 'venue_notes')
        return order

class ATEventModifier(object):
    implements(ISchemaModifier)
    adapts(IATEvent)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['location'].widget.visible = {'view': 'hidden',
                                             'edit': 'hidden'}
        schema['contactName'].widget.visible = {'view': 'hidden',
                                                'edit': 'hidden'}
        schema['contactEmail'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
        schema['contactPhone'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
