# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from edi.edxcontent.testing import EDI_EDXCONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that edi.edxcontent is properly installed."""

    layer = EDI_EDXCONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if edi.edxcontent is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'edi.edxcontent'))

    def test_browserlayer(self):
        """Test that IEdiEdxcontentLayer is registered."""
        from edi.edxcontent.interfaces import (
            IEdiEdxcontentLayer)
        from plone.browserlayer import utils
        self.assertIn(IEdiEdxcontentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EDI_EDXCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['edi.edxcontent'])

    def test_product_uninstalled(self):
        """Test if edi.edxcontent is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'edi.edxcontent'))

    def test_browserlayer_removed(self):
        """Test that IEdiEdxcontentLayer is removed."""
        from edi.edxcontent.interfaces import \
            IEdiEdxcontentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IEdiEdxcontentLayer, utils.registered_layers())
