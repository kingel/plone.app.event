from zope.component import getUtility, getMultiAdapter
from zope.site.hooks import setHooks, setSite

from Products.GenericSetup.utils import _getDottedName

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from DateTime import DateTime
from plone.app.event.portlets import calendar

import unittest2 as unittest
from plone.app.event.testing import PAEvent_INTEGRATION_TESTING
from plone.app.event.at.testing import PAEventAT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class PortletTest(unittest.TestCase):
    layer = PAEvent_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        setHooks()
        setSite(portal)

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.Calendar')
        self.assertEquals(portlet.addview, 'portlets.Calendar')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.Calendar')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
          'plone.app.portlets.interfaces.IDashboard'],
          registered_interfaces)

    def testInterfaces(self):
        portlet = calendar.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='portlets.Calendar')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # This is a NullAddForm - calling it does the work
        addview()

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], calendar.Assignment))

    def testRenderer(self):
        context = self.portal
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = calendar.Assignment()

        renderer = getMultiAdapter((context, self.request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, calendar.Renderer))


class RendererTest(unittest.TestCase):
    layer = PAEventAT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        setHooks()
        setSite(portal)

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or context.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or calendar.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_event_created_last_day_of_month_invalidate_cache(self):
        # First render the calendar portlet when there's no events
        r = self.renderer(assignment=calendar.Assignment())
        html = r.render()

        # Now let's add a new event in the last day of the current month
        year, month = r.getYearAndMonthToDisplay()
        year, month = r.getNextMonth(year, month)
        last_day_month = DateTime('%s/%s/1' % (year, month)) - 1
        hour = 1 / 24.0
        # Event starts at 23:00 and ends at 23:30
        self.portal.invokeFactory('Event', 'e1',
                                  startDate=last_day_month + 23*hour,
                                  endDate=last_day_month + 23.5*hour)

        # Make sure to publish this event
        self.portal.portal_workflow.doActionFor(self.portal.e1, 'publish')

        # Try to render the calendar portlet again, it must be different now
        r = self.renderer(assignment=calendar.Assignment())
        self.assertNotEqual(html, r.render(), "Cache key wasn't invalidated")
