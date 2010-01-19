PROJECTNAME = "cal.venue"
DEFAULT_COUNTRY = "040" # Austria
ADD_PERMISSIONS = {
    "Venue Folder" : "cal.venue: Add Venue Folder",
    "Venue"        : "cal.venue: Add Venue",
}

from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Owner', 'Contributor'))