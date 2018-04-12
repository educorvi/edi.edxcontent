import difflib
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from htmltreediff import diff as pagediff
from lxml.html.diff import htmldiff
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

    def mydiff(self, html_1, html_2):
	diff_html = ""
	theDiffs = difflib.ndiff(html_1.splitlines(), html_2.splitlines())
	for eachDiff in theDiffs:
	    if (eachDiff[0] == "-"):
		diff_html += "<del>%s</del>" % eachDiff[1:].strip()
	    elif (eachDiff[0] == "+"):
		diff_html += "<ins>%s</ins>" % eachDiff[1:].strip()
        return diff_html


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
       
        self.comments = []
        if not self.htmldiffs:
            commentdict = {'table': u'Bitte schauen Sie sich die Tabellenkonfiguration an.',
                           'thead': u'Bitte schauen Sie sich die Konfiguration der Kopfzeile an.',
                           'th': u'Bitte schauen Sie sich die Konfiguration der Kopfzellen an.'}
            elements = {}
            elements['table'] = False
            elements['thead'] = False
            elements['th'] = False
            compare = self.mydiff(testhtml, orightml)
            soup = BeautifulSoup(compare, 'html.parser')
            dels = soup.find_all('del')
            inss = soup.find_all('ins')
            diffs = dels + inss
            for i in diffs:
                if 'table' in str(i):
                    elements['table'] = True
                if 'thead' in str(i):
                    elements['thead'] = True
                if 'th' in str(i):
                    elements['th'] = True

            for i in elements:
                if elements[i]:
                    self.comments.append(commentdict[i])
