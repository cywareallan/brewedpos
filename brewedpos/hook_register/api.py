from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  POS SETTINGS
#########################################################
def register_update (doc,event):
    sql = ""
    try:
      #  get the Register fields
      reg = frappe.db.get_value('POS Register', doc.name, fieldname="*", as_dict=1)

      issueDate = str(reg.permit_start).replace('-', '')
      expireDate = str(reg.permit_expire).replace('-', '')
      lastSysdate = str(reg.last_sysdate).replace('-', '')
      #  get the Branch details
      branch = frappe.db.get_value('Branch', reg.branch,
                                   ['custom_branch_code'], as_dict=1)

      #  Check if the branch settings already exists
      sql  = "select  count(*) as recs from pos_register "
      sql += f" where location_code = '{branch.custom_branch_code}' ";
      sql += f" and   register_num = {reg.register_num} ";
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        recs = data[0][0]
      else:
        recs = 0
      nrecs = int (recs)

      if (0 == nrecs):
        #  SQL insert
        sql  = "insert into pos_register (location_code, trade_name, szmsg01, szmsg02, szmsg03, szmsg04, szmsg05, "
        sql += "nxreadcopy, nzreadcopy, xread_order_list, enablefsp, nfundcopy, "
        sql += "nsuspendcopies,  ntakeoutcopies) values ("
        sql += f"'{branch.custom_branch_code}', '{reg.trade_name}', '{reg.receipt_message_1}', "
        sql += f"'{reg.receipt_message_2}', '{reg.receipt_message_3}', '{reg.receipt_message_4}', "
        sql += f"'{reg.receipt_message_5}', {reg.xread_copies}, {reg.zread_copies}, {reg.display_fnb_orders}, "
        sql += f"{reg.enable_fsp}, {reg.cashfund_copies}, {reg.suspend_copies}, {reg.cashtakeout_copies}) "
      else:
        #  SQL update
        sql  = "update pos_settings set "
        sql += f"trade_name = '{reg.trade_name}', "
        sql += f"szmsg01 = '{reg.receipt_message_1}', "
        sql += f"szmsg02 = '{reg.receipt_message_2}', "
        sql += f"szmsg03 = '{reg.receipt_message_3}', "
        sql += f"szmsg04 = '{reg.receipt_message_4}', "
        sql += f"szmsg05 = '{reg.receipt_message_5}', "
        sql += f"nxreadcopy = {reg.xread_copies}, "
        sql += f"nzreadcopy = {reg.zread_copies}, "
        sql += f"xread_order_list = {reg.display_fnb_orders}, "
        sql += f"enablefsp = {reg.enable_fsp}, "
        sql += f"nfundcopy = {reg.cashfund_copies}, "
        sql += f"nsuspendcopies = {reg.suspend_copies}, "
        sql += f"ntakeoutcopies = {reg.cashtakeout_copies} "
        sql += f" where location_code = '{branch.custom_branch_code}'";

      #  Save it
      frappe.db.sql(sql, as_dict=0)
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")

def register_delete (doc,event):
    try:
      sql = ""
#  get the Branch fields
      reg = frappe.db.get_value('POS Branch Setttings', doc.name,
                                ['branch_name'], as_dict=1)

      #  get the Branch details
      branch = frappe.db.get_value('Branch', reg.branch_name,
                                   ['custom_branch_code'], as_dict=1)

      #  Remove the branch
      sql  = "delete from pos_settings "
      sql += f" where location_code = '{branch.custom_branch_code}'";
      #  Save it
      data = frappe.db.sql(sql, as_dict=0)
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")
