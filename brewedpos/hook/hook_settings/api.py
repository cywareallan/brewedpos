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
def settings_update (doc,event):
    sql = ""
    try:
      #  get the Branch fields
      set = frappe.db.get_value('POS Branch Settings', doc.name,
                                   ['trade_name',
                                   'display_fnb_orders',
                                   'xread_copies',
                                   'zread_copies',
                                   'suspend_copies',
                                   'cashfund_copies',
                                   'cashtakeout_copies',
                                   'enable_fsp',
                                   'receipt_message_1',
                                   'receipt_message_2',
                                   'receipt_message_3',
                                   'receipt_message_4',
                                   'receipt_message_5',
                                   'company_name',
                                   'branch_name'], as_dict=1)

      #  get the Branch details
      branch = frappe.db.get_value('Branch', set.branch_name,
                                   ['custom_branch_code'], as_dict=1)

      #  Check if the branch settings already exists
      sql  = "select  count(*) as recs from pos_settings "
      sql += f" where location_code = '{branch.custom_branch_code}' ";
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        recs = data[0][0]
      else:
        recs = 0
      nrecs = int (recs)

      #  default values
      if set.enable_fsp < 1:
           set.enable_fsp = 0
      if set.xread_copies < 1:
           set.xread_copies = 1
      if set.zread_copies < 1:
           set.zread_copies = 1
      if set.suspend_copies < 1:
           set.suspend_copies = 1
      if set.cashfund_copies < 1:
           set.cashfund_copies = 1
      if set.cashtakeout_copies < 1:
           set.cashtakeout_copies = 1

      if (0 == nrecs):
        #  SQL insert
        sql  = "insert into pos_settings (location_code, trade_name, szmsg01, szmsg02, szmsg03, szmsg04, szmsg05, "
        sql += "nxreadcopy, nzreadcopy, xread_order_list, enablefsp, nfundcopy, "
        sql += "nsuspendcopies,  ntakeoutcopies) values ("
        sql += f"'{branch.custom_branch_code}', '{set.trade_name}', '{set.receipt_message_1}', "
        sql += f"'{set.receipt_message_2}', '{set.receipt_message_3}', '{set.receipt_message_4}', "
        sql += f"'{set.receipt_message_5}', {set.xread_copies}, {set.zread_copies}, {set.display_fnb_orders}, "
        sql += f"{set.enable_fsp}, {set.cashfund_copies}, {set.suspend_copies}, {set.cashtakeout_copies}) "
      else:
        #  SQL update
        sql  = "update pos_settings set "
        sql += f"trade_name = '{set.trade_name}', "
        sql += f"szmsg01 = '{set.receipt_message_1}', "
        sql += f"szmsg02 = '{set.receipt_message_2}', "
        sql += f"szmsg03 = '{set.receipt_message_3}', "
        sql += f"szmsg04 = '{set.receipt_message_4}', "
        sql += f"szmsg05 = '{set.receipt_message_5}', "
        sql += f"nxreadcopy = {set.xread_copies}, "
        sql += f"nzreadcopy = {set.zread_copies}, "
        sql += f"xread_order_list = {set.display_fnb_orders}, "
        sql += f"enablefsp = {set.enable_fsp}, "
        sql += f"nfundcopy = {set.cashfund_copies}, "
        sql += f"nsuspendcopies = {set.suspend_copies}, "
        sql += f"ntakeoutcopies = {set.cashtakeout_copies} "
        sql += f" where location_code = '{branch.custom_branch_code}'";

      #  Save it
      frappe.db.sql(sql, as_dict=0)
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")

def settings_delete (doc,event):
    try:
      sql = ""
#  get the Branch fields
      set = frappe.db.get_value('POS Branch Setttings', doc.name,
                                ['branch_name'], as_dict=1)

      #  get the Branch details
      branch = frappe.db.get_value('Branch', set.branch_name,
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
