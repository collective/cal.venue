from zope.component import adapts
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATEvent
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.field import ExtensionField
from cal.venue import MsgFact as _

class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    """This field is capable of Extending predefined schemas."""

class ATEventExtender(object):
    implements(IOrderableSchemaExtender)
    adapts(IATEvent)

    fields = [
        ReferenceFieldExtender("venue",
            relationship='isVenueForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            # vocabulary_factory=u"cal.venue.venuelist", # Found in venue.py
            vocabulary_display_path_bound=-1, # Avoid silly Archetypes object title magic
            enforceVocabulary=True,
            widget=atapi.ReferenceWidget(label=_(u"Venue of Event"),
                                         description=_(u""))
            ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        # just a test
        # self.context.schema._fields['location'] = self.fields[0]
        return self.fields

    def getOrder(self, order):
        schemata_default = order['default']
        schemata_default.remove('venue')
        schemata_default.insert(6, 'venue')
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
