from zope.interface import implements
from Products.ATContentTypes.content import folder
from Products.Archetypes import atapi

from cal.venue.interfaces import IVenueFolder
from cal.venue.config import PROJECTNAME

VenueFolderSchema = folder.ATFolderSchema.copy()
VenueFolderSchema['title'].storage = atapi.AnnotationStorage()
VenueFolderSchema['description'].storage = atapi.AnnotationStorage()

class VenueFolder(folder.ATFolder):
    implements(IVenueFolder)

    portal_type = "Venue Folder"
    _at_rename_after_creation = True
    schema = VenueFolderSchema

    # make them behave like python properties
    # see Product.Archetypes.fieldproperty
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(VenueFolder, PROJECTNAME)
