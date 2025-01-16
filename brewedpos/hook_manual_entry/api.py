from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  Loyalty Manual Entry
#########################################################
def validate_entry (doc,event):  
    sql = ""
    manual_entry = frappe.db.get_value('Loyalty Manual Entry', doc.name, 
                                    ['transaction_code', 
                                     'branch', 
                                     'trans_date', 
                                     'register_number', 
                                     'transnum', 
                                     'total_points'], as_dict=1)
                                     
    
      
    #  Check if record already exists
    sql = ""
    sql += f"select count(*) as recs from `tabLoyalty Manual Entry` "
    sql += f" where transaction_code = '{manual_entry.transaction_code}' ";
    sql += f" and register_number = '{manual_entry.register_number}' ";
    sql += f" and transnum = '{manual_entry.transnum}' ";
    sql += f" and branch = '{manual_entry.branch}' ";
    data = frappe.db.sql(sql, as_dict=0)

    if data and data[0]:
        recs = data[0][0]
    else:
        recs = "0"

    nrecs = int (recs)  
    if (nrecs > 1):
        frappe.throw (f"Duplicate Transaction Found.")  

