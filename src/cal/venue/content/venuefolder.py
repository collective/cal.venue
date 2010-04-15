from zope.interface import implements

try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from cal.venue import MsgFact as _
from cal.venue.interfaces import IVenueFolder
from cal.venue.config import PROJECTNAME

venuefolder_schema = folder.ATFolderSchema.copy()
venuefolder_schema['title'].storage = atapi.AnnotationStorage()
venuefolder_schema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(venuefolder_schema,
                            folderish=True,
                            moveDiscussion=False)

class VenueFolder(folder.ATFolder):
    # security = ClassSecurityInfo()
    implements(IVenueFolder)

    portal_type = "Venue Folder"
    _at_rename_after_creation = True
    schema = venuefolder_schema

    # make them behave like python properties
    # see Product.Archetypes.fieldproperty
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(VenueFolder, PROJECTNAME)