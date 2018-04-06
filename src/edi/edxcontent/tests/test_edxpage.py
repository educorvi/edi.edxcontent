# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from edi.edxcontent.interfaces import IEdxpage
from edi.edxcontent.testing import EDI_EDXCONTENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class EdxpageIntegrationTest(unittest.TestCase):

    layer = EDI_EDXCONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Edxpage')
        schema = fti.lookupSchema()
        self.assertEqual(IEdxpage, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Edxpage')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Edxpage')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IEdxpage.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Edxpage',
            id='Edxpage',
        )
        self.assertTrue(IEdxpage.providedBy(obj))
