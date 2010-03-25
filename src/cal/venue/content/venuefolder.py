from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from cal.venue import MsgFact as _
from cal.venue.interfaces import IVenueFolder
from cal.venue.config import PROJECTNAME

VenueFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ))
VenueFolderSchema['title'].storage = atapi.AnnotationStorage()
VenueFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(VenueFolderSchema,
                            folderish=True,
                            moveDiscussion=False)

class VenueFolder(folder.ATFolder):
    # security = ClassSecurityInfo()
    implements(IVenueFolder)

    portal_type = "Venue Folder"
    _at_rename_after_creation = True
    schema = VenueFolderSchema

    # make them behave like python properties
    # see Product.Archetypes.fieldproperty
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(VenueFolder, PROJECTNAME)
