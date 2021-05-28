# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import sys

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import os
import sys


#Global variables
files_path = os.path.join(os.path.realpath(os.getcwd()), "files")


import refactoredSearch as rs

class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Hello World!")

         return []


from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction   

# Test:   Action object that searches for files locally
# Author: 2391564v - Charles
class ActionSearchFiles(Action):
    def name(self) -> Text:
        return "action_search_files"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Searching for files...")
       
        # Look for files in specified directory (can be changed later)
        files_list = os.listdir(files_path)
        
        if len(files_list) > 0:
            dispatcher.utter_message("Found " + str(len(files_list)) + " files.")
            
            # Print file names with an associated number
            for f in files_list:
                dispatcher.utter_message(f)
            dispatcher.utter_message("Select a file")
    
            print("files: " + str(files_list))
        else:
            dispatcher.utter_message("Unable to find any files.")
        
        return [SlotSet("files", files_list)]

# Test:     Action object that opens a file and prints it's content
# Author:   2391564v - Charles
class ActionOpenFile(Action):
    def name(self) -> Text:
        return "action_open_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        try:
            # Open file
            dispatcher.utter_message("Opening file...")
            
            path = os.path.join(files_path, tracker.get_slot("file")) 
            with open(path, "r") as f:
                content = f.read()
                # Testing purposes, print file content
                dispatcher.utter_message(content)

        except:
            dispatcher.utter_message("Unable to open file...")
        
        return
       
# Test:     Form object that collects file name information from user for processing
# Author:   2391564v - Charles
class FileForm(FormAction):
    def name(self):
        return "file_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        # return a list of required slots to be filled by form,
        # can have multiple return paths depending on context of form
        return ["file"]
    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # define what the form should do once it's filled the required slots
        dispatcher.utter_template("utter_submit", tracker)
        return []

    
# Form:     Collect data needed to handle a course issue query
# Author:   2391564v - Charles
class CourseIssueForm(FormAction):
    def name(self):
        return "course_issue_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        # return a list of required slots to be filled by form,
        # can have multiple return paths depending on context of form
        return ["course", "issue"]
    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # define what the form should do once it's filled the required slots
        dispatcher.utter_template("utter_submit", tracker)
        return []


# Action:   Search source text for course information in the context of user issue
# Author:   Charles - 2391564v
class ActionCourseIssue(Action):
    def name(self) -> Text:
        return "action_course_issue"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            print("Before script: {}, {}".format(tracker.get_slot("course"), tracker.get_slot("issue")))
            answer = rs.searchfile(tracker.get_slot("course"), *(tracker.get_slot("issue")))
            print("got an answer")
            dispatcher.utter_message(str(answer))
        except: 
            dispatcher.utter_message("I'm sorry but I didn't understand your query! Could you please try again?")
        return []

    
# Action:   Search source text for course information in the context of deadline extentions details
# Author:   Charles - 2391564v
class ActionFindExtensionDetails(Action):
    def name(self) -> Text:
        return "action_find_extension_details"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            print("Before script: {}, {}".format(tracker.get_slot("course"), tracker.get_slot("duration")))
            answer = rs.searchfile(tracker.get_slot("course"), tracker.get_slot("duration"), "extention", "duration")
            print("got an answer")
            dispatcher.utter_message(answer)
        except: 
            dispatcher.utter_message("I'm sorry but I didn't understand your query! Could you please try again?")
        return []
    

# Action:   Search source text for find information about academic source requirements
# Author:   Charles - 2391564v
class ActionAcademicsourcesRequirements(Action):
    def name(self) -> Text:
        return "action_academicsources_requirements"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # There are no slots to pass to this action.
        answer = rs.searchfile("academic", "source", "requirements")
        print("got an answer")
        dispatcher.utter_message(answer)
            
        return []


# Action:   Search source text for find information about reference help
# Author:   Charles - 2391564v
class ActionFindReferencehelp(Action):
    def name(self) -> Text:
        return "action_find_referencehelp"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # There are no slots to pass to this action.
        answer = rs.searchfile("find", "reference", "help")
        print("got an answer")
        dispatcher.utter_message(answer)
            
        return []


# Action:   Search source text for find course information in the context of approval
# Author:   Charles - 2391564v
class ActionCourse(Action):
    def name(self) -> Text:
        return "action_course"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            print("Before script: {}".format(tracker.get_slot("course")))
            answer = rs.searchfile(tracker.get_slot("course"), "approval")
            print("got an answer")
            dispatcher.utter_message(answer)
        except: 
            dispatcher.utter_message("I'm sorry but I didn't understand your query! Could you please try again?")
        return []
    
    
# Action:   Reset slots for next conversation
# Author:   Charles - 2391564v
class ActionReset(Action):
	def name(self) -> Text:
		return "action_reset"

	def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		return [SlotSet("course", None), SlotSet("issue", None), SlotSet("duration", None), SlotSet("turnitin", None)]
    
    
