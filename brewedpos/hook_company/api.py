from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  COMPANY
#########################################################
def company_delete (doc,event):  
    try:
      #  get doctype Company's fields
      company = frappe.db.get_value('Company', doc.name, 
                                  ['custom_company_code', 
                                   'company_name',
                                   'abbr',
                                   'default_currency',
                                   'country'], as_dict=1)
      #  SQL insert                             
      sql = f" delete from cy_company where company_code = '{company.custom_company_code}'"
      #  Save it
      data = frappe.db.sql(sql, as_dict=0)    
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")  	   

def company_update (doc,event):  
    try:
      #  get doctype Company's fields
      company = frappe.db.get_value('Company', doc.name, 
                                  ['custom_company_code', 
                                   'company_name',
                                   'abbr',
                                   'default_currency',
                                   'country'], as_dict=1)
      #  See if the POS company exists
      sql = "select count(*) as recs from cy_company where company_code = "; 
      values = f"'{company.custom_company_code}'";
      sql += values
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        recs = data[0][0]
      else:
        recs = "0"

      nrecs = int (recs)  
      if (0 == nrecs):
        #  SQL insert                             
        sql = "insert into cy_company (company_code, description, currency_code) values (";
        values = f"'{company.custom_company_code}', '{company.company_name}', '{company.default_currency}')"
        sql += values
      else:
        #  SQL insert                             
        sql = "update cy_company set currency_code = "
        values = f"'{company.default_currency}' where company_code = '{company.custom_company_code}' "
        sql += values


      #  Save it
      frappe.db.sql(sql, as_dict=0)    
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")      
    

