# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.edxcontent -t test_edxpage.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.edxcontent.testing.EDI_EDXCONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_edxpage.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Edxpage
  Given a logged-in site administrator
    and an add edxpage form
   When I type 'My Edxpage' into the title field
    and I submit the form
   Then a edxpage with the title 'My Edxpage' has been created

Scenario: As a site administrator I can view a Edxpage
  Given a logged-in site administrator
    and a edxpage 'My Edxpage'
   When I go to the edxpage view
   Then I can see the edxpage title 'My Edxpage'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add edxpage form
  Go To  ${PLONE_URL}/++add++Edxpage

a edxpage 'My Edxpage'
  Create content  type=Edxpage  id=my-edxpage  title=My Edxpage


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the edxpage view
  Go To  ${PLONE_URL}/my-edxpage
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a edxpage with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the edxpage title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
