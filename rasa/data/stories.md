## Greet user, it's polite.
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## test 1 - hello world
## * test_hello
##  - action_hello_world

## test 2 - find and open a text file, print content to user
## * test_file
##  - action_search_files
## * open_file
##  - action_open_file

## test 3 - do test 2 using forms
## * open_file
##  - file_form
##  - action_open_file
##  - utter_slots_file

## Student Studying abroad
* ask_study{"study": "studying abroad"}
  - utter_appreciation
  - utter_appoint_intlexof
* thanked
  - utter_thank

## Give information about related courses, else appoint to someone more appropriate
## Happy ending
* give_course{"course": "social science"}
  - slot{"course": "social science"}
  - utter_thank_course
* ask_issue{"issue": "grades"}
  - slot{"issue": "grades"}
  - action_course_issue
  - utter_did_that_help
* affirm
  - utter_happy
  - action_reset

## Give information about related courses, else appoint to someone more appropriate
## Sad ending
* give_course{"course": "economics"}
  - slot{"course": "economics"}
  - utter_thank_course
* ask_issue{"issue": "entry requirements"}
  - slot{"issue": "entry requirements"}
  - action_course_issue
  - utter_did_that_help
* deny
  - utter_sad
  - action_reset

## extension-medical
* extention + mentalhealth
  - utter_mentalhealth_confirmation
  - utter_ask_extension_length
* duration{"duration": "2 weeks"}
  - slot{"duration": "2 weeks"}
  - action_find_extension_details
* difficulties
  - utter_reassurance

## extension-issue
* extension + issue
  - utter_thank
  - utter_ask_extension_length
* duration{"duration":"5 days"}
  - slot{"duration":"5 days"}
  - utter_thank
  - action_find_extension_details

## physical health statement for good cause
* physicalhealth
  - utter_thank
  - utter_hopeyoufeelbetter
* medical_evidence
  - utter_medical_confirmation
* good_cause
  - utter_good_cause
* course_convenor
  - utter_appoint_courseconvenor

## asking about turnitin
* ask_turnitin_acceptable_rate
  - utter_nothreshold
* turnitin{"turnitin":19}
  - slot{"turnitin":19}
  - utter_reassurance

## want academic resources
* academicsources
  - utter_thank
  - action_academicsources_requirements
* ask_external_academicsources
  - utter_external_academicsources_confirmation

## about essay submissions
* ask_essay_submission
  - utter_appoint_susanna

## want help for essay references
* ask_essay_reference_help
  - action_find_referencehelp

## help regarding enrollment
* ask_enrollment
  - utter_appoint_susanna

## want to approve courses
* course_approval{"course": "PUBPOL3015"}
  - action_course{"course":"PUBPOL3015"}
* ask_books_purchasing
  - utter_aboutpurchasingbooks
