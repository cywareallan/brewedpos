from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  BRANCH
#########################################################
def branch_update (doc,event):  
    sql = ""
    try:
      #  get the Branch fields
      branch = frappe.db.get_value('Branch', doc.name, 
                                   ['custom_address_1', 
                                   'custom_address_2', 
                                   'custom_city', 
                                   'custom_province', 
                                   'custom_tax_id_number', 
                                   'custom_permit_number', 
                                   'custom_bir_issue_date', 
                                   'custom_bir_expire_date', 
                                   'custom_bir_number', 
                                   'custom_header_message_1', 
                                   'custom_header_message_2', 
                                   'custom_header_message_3',
                                   'custom_cost_center'], as_dict=1)
            
      issueDate = str(branch.custom_bir_issue_date).replace('-', '')
      expireDate = str(branch.custom_bir_expire_date).replace('-', '')
      #  get the Branch Cost Center
      costCenter = frappe.db.get_value('Cost Center', branch.custom_cost_center,
                                      ['company',
                                      'cost_center_name', 
                                      'cost_center_number'], as_dict=1)

      #  get doctype Company Code
      company = frappe.db.get_value('Company', costCenter.company, 
                                   ['custom_company_code'], as_dict=1)      
      
      #  Check if the branch already exists
      sql  = "select count(*) as recs from cy_location "
      sql += f" where company_code = '{company.custom_company_code}' and location_code = '{costCenter.cost_center_number}'";
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        recs = data[0][0]
      else:
        recs = "0"

      nrecs = int (recs)  
      if (0 == nrecs):
        #  SQL insert                             
        sql  = "insert into cy_location (company_code, location_code, loc_type_code, description, "
        sql += "addr1, addr2, city_code, state_code, tin, permitno, bir_num, bir_issue, bir_expire, "
        sql += "hdrmsg1, hdrmsg2, hdrmsg3) values ("
        sql += f"'{company.custom_company_code}', '{costCenter.cost_center_number}', 'ST', "
        sql += f"'{doc.name}', '{branch.custom_address_1}', '{branch.custom_address_2}', '{branch.custom_city}', "
        sql += f"'{branch.custom_province}', '{branch.custom_tax_id_number}', '{branch.custom_permit_number}', "
        sql += f"'{branch.custom_bir_number}', '{issueDate}', '{expireDate}', "
        sql += f"'{branch.custom_header_message_1}', '{branch.custom_header_message_2}', '{branch.custom_header_message_3}') "
      else:
        #  SQL update
        sql  = "update cy_location set "
        sql += f"description = '{doc.name}', "
        sql += f"addr1 = '{branch.custom_address_1}', "
        sql += f"addr2 = '{branch.custom_address_2}', "
        sql += f"city_code = '{branch.custom_city}', "
        sql += f"state_code = '{branch.custom_province}', "
        sql += f"tin = '{branch.custom_tax_id_number}', "
        sql += f"permitno = '{branch.custom_permit_number}', "
        sql += f"bir_num = '{branch.custom_bir_number}', "
        sql += f"bir_issue = '{issueDate}', "
        sql += f"bir_expire = '{expireDate}', "
        sql += f"hdrmsg1 = '{branch.custom_header_message_1}', "
        sql += f"hdrmsg2 = '{branch.custom_header_message_2}', "
        sql += f"hdrmsg3 = '{branch.custom_header_message_3}' "
        sql += f" where company_code = '{company.custom_company_code}' and location_code = '{costCenter.cost_center_number}'";
      
      #  Save it
      frappe.db.sql(sql, as_dict=0)    
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")  

def branch_delete (doc,event):  
    try:
      sql = ""
      #  get the Branch fields
      branch = frappe.db.get_value('Branch', doc.name, 
                                   ['custom_cost_center'], as_dict=1)
      #  get the Branch Cost Center
      costCenter = frappe.db.get_value('Cost Center', branch.custom_cost_center,
                                      ['company',
                                      'cost_center_name', 
                                      'cost_center_number'], as_dict=1)
      #  get doctype Company Code
      company = frappe.db.get_value('Company', costCenter.company, 
                                   ['custom_company_code'], as_dict=1)      
      
      #  Remove the branch
      sql  = "delete from cy_location "
      sql += f" where company_code = '{company.custom_company_code}' and location_code = '{costCenter.cost_center_number}'";
      #  Save it
      data = frappe.db.sql(sql, as_dict=0)    
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")        
