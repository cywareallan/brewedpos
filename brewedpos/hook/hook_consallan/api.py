from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  CONS ALLAN
#########################################################
def ca_update (doc,event):
    try:
      #  get doctype ConsAllan fields
      company = frappe.db.get_value('ConsAllan', doc.name,
                                    ['family_type_cd', 'family_desc'], as_dict=1)


      #frappe.throw (str(company.family_type_cd))
      sql = "update `tabRobert` set issync = "
      values = f"{company.family_type_cd} "
      #where company_code = '{company.custom_company_code}' "
      sql += values


      #  Save it
      frappe.db.sql(sql, as_dict=0)
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")


