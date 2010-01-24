# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
__author__ = """Johannes Raggam <johannes@raggam.co.at>"""
__docformat__ = 'plaintext'

from zope.component import adapts
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.ATContentTypes.interfaces import IATEvent
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.field import ExtensionField
from cal.venue.interfaces import IEventVenue


class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    """This field is capable of Extending predefined schemas."""

class ATEventExtender(object):
    implements(IOrderableSchemaExtender) # Even if the order is not modified,
                                         # other packages which subclass this
                                         # one should be able to reorder fields
    adapts(IATEvent)

    fields = [
        ReferenceFieldExtender("location",
            required=False,
            relationship='isLocationForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            storage=atapi.AnnotationStorage(),
            vocabulary_display_path_bound=-1, # Avoid silly Archetypes object title magic
            enforceVocabulary=True,
            widget=atapi.ReferenceWidget(
                description = '',
                label = _(u'label_event_location', default=u'Event Location')
                ),
            ),
    ]

    def __init__(self, context):
        ## May not work, because location may exist as an stringfieldproperty

        # from zope.site.hooks import getSite
        # field = context.getField('location')
        # if field:
        #     context.location = field.get(context.__of__(getSite()))
        #     print context.location

        # if 'startDate' in context.__dict__:


        # import pdb;pdb.set_trace()
        # from zope.site.hooks import getSite
        # field = context.getField('location')
        # if field:
        #    context.location = field.get(context.__of__(getSite()))
        # import pdb;pdb.set_trace()
        # if 'location' not in context.__dict__:
        # import pdb;pdb.set_trace()
        # if 'startDate' in context.__dict__:
            # import pdb;pdb.set_trace()
        # print context.getField('location').get(context.__of__(getSite()))
        # context.location = context.getField('location').get(context)
        # print context.location
        # context.location = atapi.ATFieldProperty('location')
        # print context.location
        self.context = context

    def getFields(self):
        if 'startDate' in self.context.__dict__:
            print "startdate do"

            # import pdb;pdb.set_trace()
            from zope.site.hooks import getSite
            field = self.context.getField('location')
            if field:
                self.context.location = field.get(self.context.__of__(getSite()))
                print "SETTING LOC"
                print self.context.location
        else:
            print "startdate NET do"

        return self.fields

    def getOrder(self, order):
        return order

class ATEventModifier(object):
    implements(ISchemaModifier)
    adapts(IATEvent)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['contactName'].widget.visible = {'view': 'hidden',
                                                'edit': 'hidden'}
        schema['contactEmail'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
        schema['contactPhone'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
