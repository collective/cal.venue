Introduction
============

Addition to Plone's ATContentTypes's ATEvent to support referenced venues.

So, Content Editors must not type in a venue location each and every time an
event happens but can choose from a list of previously added venues.

New content types:
- Venue: A content type which is used to define new venues/locations
- Venue Folder: A folder where venues are defined

Additions to ATEvent:
- ATEvent.venue: A reference field which references Venues
- ATEvent.venue_notes: A textfield which can be used if there is additional
  information for the venue at the specific event or if creating a new venue for
  just one event is too much overhead.


TODO
====

- Internationalize it
- Write tests
- Bump version to 1.0 after that is done


Author
======

Johannes Raggam <johannes@raggam.co.at>