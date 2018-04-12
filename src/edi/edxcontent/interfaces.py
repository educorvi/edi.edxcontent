# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from edi.edxcontent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.textfield import RichText

class IEdiEdxcontentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEdxpage(Interface):

    title = schema.TextLine(
        title=_(u'Titel'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Kurzbeschreibung'),
        required=False,
    )

    text = RichText(
        title=u'Haupttext',
        required=True,
    )

    muster = schema.TextLine(
        title=u'Vorlage',
        required=True,
    )
