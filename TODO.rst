TODO artsprint 2011
===================

- on fresh install, creating an event - timezones can not be selected but are
  mandatory. at least a default timezone has to be selected in the
  event-settings configlet. that should be set at install time.

- archetypes.datetimewidget, collective.z3cform.datetimewidget -> merge into
  plone.formwidget.datetime

- "no end date" option -> change boolean field "all_day" to list field "date_options" containing all_day and no_end_date

- [X] recurrence field goes after end date.
  [ ] hide text area with css display:none
  [X] remove schemata recurrence
  [ ] provide checkbox "this date recurrs ..." and toggle textarea then

OK - datetimewidget calendar images missing...

- calendar starting year, calendar future years options in datetimewidget

- calendar portlet should use jquery tools calendar. maybe construct portlet, so that a viewlet can also use calendar via metal:macros.

- document TZ behavior with examples

OK - new TZ field on ATEvent. store all dates in UTC timezone. store TZ extra. display dates in user's timezone (via TZ fetcher utility). use getter and setter to calculate timezones (get: UTC-userTZ set: userTZ->UTC).
- allow no TZ setting on content context at all - this solves "world plone day" problem (event in different timezones, whole day in every timezone)

- provide plone.formwidget.timezone widget for TZ field described above

OK- provide configlet to configure portal's TZ. use dropdown for default_timezone and in-out-widget for allowed_timezones (which then are used to filter tz's with elephantvocabulary)

- eventually provide configlet to configure TZ per user

OK- plone.event -> TZ vocabulary
OK- plone.app.event -> TZ vocabulary based on elephantvocabulary filter
    get filtered items or display items from plone.registry

OK- TZ fetcher utility
  OK - plone.event: OS TZ
  OK- plone.app.event portal TZ
  - context, user, portal TZ

- recurrence widget

- error when submitting random data to recurrence field. catch dateutil's error and raise validation error. display error as error message.

- complete the benchmark products.daterecurringindex
  sync with hanno's changes to dateindex


migration steps
---------------
- default timezone - set via event-settings configlet
- migration from old ATEvent

