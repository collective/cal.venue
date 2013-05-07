from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from plone.memoize import instance
import pycountry

from cal.venue.interfaces import IVenue
from cal.venue.config import PROJECTNAME, DEFAULT_COUNTRY
from cal.venue import MsgFact as _

VenueSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField('street1',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Street 1"),
            description=_(u""),
        ),
    ),
    atapi.StringField('street2',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Street 2"),
            description=_(u""),
        ),
    ),
    atapi.StringField('zipCode',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Zip code"),
            description=_(u""),
        ),
    ),
    atapi.StringField('city',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"City"),
            description=_(u""),
        ),
    ),
    atapi.StringField('state',
        required=False,
        searchable=True,
        languageIndependent=True,
        vocabulary_factory=u"cal.venue.CountryVocabulary",
        enforceVocabulary=True,
        default=DEFAULT_COUNTRY,
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"State"),
            description=_(u"Select the Country the venue is located in"),
        ),
    ),

    atapi.StringField('contactName',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Contact person name"),
            description=_(u""),
        ),
    ),
    atapi.StringField('contactEmail',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        validators=("isEmail"),
        widget=atapi.StringWidget(
            label=_(u"Contact Email"),
            description=_(u""),
        ),
    ),
    atapi.StringField('contactPhone',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Contact phone"),
            description=_(u""),
        ),
    ),
    atapi.StringField('url',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        validators=("isURL"),
        widget=atapi.StringWidget(
            label=_(u"Url"),
            description=_(u"Use the form http://WEBSITE.TLD/"),
        ),
    ),
    atapi.TextField('cityMap',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        default_content_type='text/html',
        default_output_type='text/html',
        widget=atapi.TextAreaWidget(
            label=_(u"City Map HTML Code"),
            description=_(u"Iframe HTML Code for Google Map, "
                          u"OpenStreetMap or the like"),
        ),
    ),
    atapi.TextField('text',
        required=False,
        searchable=True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Additional notes"),
            rows=5,
            allow_file_upload=False,
        ),
    ),
))


VenueSchema['title'].storage = atapi.AnnotationStorage()
VenueSchema['title'].widget.label = _(u"Venue name")
VenueSchema['title'].widget.description = _(u"")

VenueSchema['description'].storage = atapi.AnnotationStorage()
VenueSchema['description'].widget.visible = {'view': 'invisible',
                                             'edit': 'invisible'}

VenueSchema['location'].widget.visible = {'view': 'hidden',
                                          'edit': 'hidden'}

schemata.finalizeATCTSchema(VenueSchema,
                            folderish=False,
                            moveDiscussion=False)


class Venue(base.ATCTContent):
    # security = ClassSecurityInfo()
    implements(IVenue)

    portal_type = "Venue"
    _at_rename_after_creation = True
    schema = VenueSchema

    # make them behave like python properties
    # see Product.Archetypes.fieldproperty
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    street_1 = atapi.ATFieldProperty('street1')
    street_2 = atapi.ATFieldProperty('street2')
    zip_code = atapi.ATFieldProperty('zipCode')
    city = atapi.ATFieldProperty('city')
    state = atapi.ATFieldProperty('state')
    contact_name = atapi.ATFieldProperty('contactName')
    contact_email = atapi.ATFieldProperty('contactEmail')
    contact_phone = atapi.ATFieldProperty('contactPhone')
    url = atapi.ATFieldProperty('url')
    city_map = atapi.ATFieldProperty('cityMap')
    text = atapi.ATFieldProperty('text')

    def __str__(self):
        #txt = '%s %s %s %s %s' % (self.title, self.street_1, self.street_2,
        #                          self.zip_code, self.city)
        txt = self.title
        txt += txt and self.street_1 and str(', ' + self.street_1)
        txt += txt and self.street_2 and str(', ' + self.street_2)
        txt += txt and (self.zip_code or self.city) and\
                str(', ' + self.zip_code + ' ' + self.city)
        return txt  # .decode('utf-8')

    def get_venue_address(self):
        txt = self.street_1
        txt += txt and self.street_2 and str(', ' + self.street_2)
        txt += txt and (self.zip_code or self.city) and\
                str(', ' + self.zip_code + ' ' + self.city)
        return txt  # .decode('utf-8')

atapi.registerType(Venue, PROJECTNAME)


@instance.memoize
def CountryVocabulary(context):
    """Vocabulary factory for countries regarding to ISO3166
    """
    items = [(r.name.encode('utf-8'), r.numeric)
             for r in pycountry.countries]
    return SimpleVocabulary.fromItems(items)
directlyProvides(CountryVocabulary, IVocabularyFactory)
