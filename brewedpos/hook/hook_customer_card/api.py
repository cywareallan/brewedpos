from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  Loyalty Customer Card
#########################################################
def validate_account (doc,event):  
    sql = ""
    try:
      #  get the Branch fields
      customer_card = frappe.db.get_value('Loyalty Customer Card', doc.name, 
                                   ['card_number'], as_dict=1)
      frappe.throw (f"'{customer_card.card_number}'")
      #  Check if the branch already exists
      sql  = "select count(*) as recs from `tabLoyalty Customer Card` "
      sql += f" where card_number = '{customer_card.card_number}'";

      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        recs = data[0][0]
      else:
        recs = "0"

      nrecs = int (recs)  
      if (nrecs > 0):
        frappe.throw (f"Card Number already exists.")  

