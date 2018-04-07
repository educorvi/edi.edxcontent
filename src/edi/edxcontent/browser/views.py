from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from htmltreediff import diff as pagediff
from bs4 import BeautifulSoup
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

api.templatedir('templates')

class EditorView(api.View):
    api.context(Interface)

    def update(self):
        alsoProvides(self.request, IDisableCSRFProtection)

    def render(self):
        vorlagetext = '<p></p>'
        vorlage = self.request.get('vorlage')
        vorlagebrain = ploneapi.content.find(Webcode=vorlage)
        if vorlagebrain:
            vorlageobject = vorlagebrain[0].getObject()
            vorlagetext = vorlageobject.text.output
        muster = self.request.get('muster')
        alsoProvides(self.request, IDisableCSRFProtection)
        obj = ploneapi.content.create(
            type="Edxpage",
            title="Test aus OPENedX",
            text=vorlagetext,
            muster = muster,
            container=self.context)
        url = obj.absolute_url() + '/edit'
        return self.response.redirect(url)

class LearningView(api.Page):
    api.context(Interface)

    def update(self):
        testhtml = '<html></html>'
        orightml = '<html></html>'
        muster = ploneapi.content.find(Webcode=self.context.muster)
        if muster:
            doc = muster[0].getObject()
            orightml = doc.text.raw

        if self.context.text:
            testhtml = self.context.text.raw

        compare = pagediff(testhtml, orightml)
        soup = BeautifulSoup(compare, 'html.parser')
        dels = soup.find_all('del')
        inss = soup.find_all('ins')

        self.htmldiffs = []
        for i, k in zip(dels, inss):
            self.htmldiffs.append((i, k))
