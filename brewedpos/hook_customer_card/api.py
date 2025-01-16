from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
import requests
import json
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  Loyalty Customer Card
#########################################################
def validate_account (doc,event):  
	url = "https://jsonplaceholder.typicode.com/posts"
	# Data to be sent
	data = {
	    "userID": 1,
	    "title": "Making a POST request",
	    "body": "This is the data we created."
	}
	# A POST request to the API
	response = requests.post(url, json=data)
	
	# Print the response
	frappe.throw(f"{json.loads(response.text)['body']}")