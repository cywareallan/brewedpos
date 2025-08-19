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
def process_redeem (doc,event):
    sql = ""
    try:
      #  get the Register fields
      reg = frappe.db.get_value('Loyalty Redemption', doc.name, fieldname="*", as_dict=1)
      
      reference = reg.name
      customer_id = reg.customer_id

      #  Check if the branch settings already exists
      sql  = "select  points, item from `tabLoyalty Rewards`";
      sql += f" where reward_type_code = '{reg.reward_type_code}' ";
      sql += f" and   reward_code = '{reg.reward_code}' ";
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        reward_points = data[0][0]
        item_code = data[0][1]
      else:
        frappe.throw ("unable to fetch reward points")
        
      sql  = "select  points_balance from `tabCustomer`";
      sql += f" where name = '{reg.customer_id}' ";
      data = frappe.db.sql(sql, as_dict=0)

      if data and data[0]:
        points_balance = data[0][0]
      else:
        frappe.throw ("unable to fetch customer balance")
      
      total_points = float(reward_points)*reg.quantity
      str_total_points = str(total_points)
      
      if (total_points > float(points_balance)): 
        frappe.throw ("insufficient balance")
      
      if (len(item_code) > 0):
          sql  = "select uom, price_list_rate from `tabItem Price` ";
          sql += f"where item_code = '{item_code}' and valid_from <= current_date";
          data = frappe.db.sql(sql, as_dict=0)
          
          if data and data[0]:
            uom = data[0][0]
            price_list_rate = data[0][1]
          else:
            frappe.throw ("unable to fetch unit price")
            
          sql  = "select description from `tabItem` ";
          sql += f"where item_code = '{item_code}'";
          data = frappe.db.sql(sql, as_dict=0)
          
          if data and data[0]:
            item_description = data[0][0]
          else:
            frappe.throw ("unable to fetch unit price")
            
          sql  = f"select qty_after_transaction, qty_after_transaction-{reg.quantity}, ";
          sql += f"{reg.quantity}*{price_list_rate}*-1, (qty_after_transaction-{reg.quantity})*{price_list_rate}, year(current_date) ";
          sql += f"from `tabStock Ledger Entry` ";
          sql += f"where item_code = '{item_code}' ";
          sql += f"and   warehouse = 'Stores - JT' order by creation desc";
          data = frappe.db.sql(sql, as_dict=0)
          
          if data and data[0]:
            stock_qty = data[0][0]
            new_qty = data[0][1]
            item_cost = data[0][2]
            total_cost = data[0][3]
            fiscal_year = data[0][4]
          else:
            frappe.throw ("unable to fetch unit price")
            
          #frappe.throw (f"{stock_qty},{new_qty},{item_cost},{total_cost},{fiscal_year}")
            
          sql = "insert into `tabStock Entry` (name, creation, modified, modified_by, owner, docstatus, ";
          sql += "idx, naming_series, stock_entry_type, purpose, add_to_transit, company, posting_date, ";
          sql += "posting_time, set_posting_time, inspection_required, apply_putaway_rule, from_bom, ";
          sql += "use_multi_level_bom, fg_completed_qty, process_loss_percentage, process_loss_qty, ";
          sql += "total_outgoing_value, total_incoming_value, value_difference, total_additional_costs, ";
          sql += "is_opening, per_transferred, total_amount, is_return) values (";
          sql += f"'REDEEM-{reference}', now(), now(), 'Administrator','Administrator','1','2','REDEEM-',";
          sql += f"'Test','Send to Subcontractor','0','Joel`s Place', current_date, current_time, ";
          sql += f"'0', '0', '0', '0', '1', '0', '0', '0', {price_list_rate}*{reg.quantity}, ";
          sql += f"{price_list_rate}*{reg.quantity}, 0, 0, 'No', '0', {price_list_rate}*{reg.quantity}, '0')";
          frappe.db.sql(sql, as_dict=0)

          sql = "insert into `tabStock Entry Detail`(name, creation, modified, modified_by, owner, ";
          sql += "docstatus, idx, has_item_scanned, s_warehouse, t_warehouse, item_code, item_name, ";
          sql += "is_finished_item, is_scrap_item, description, item_group, qty, transfer_qty, ";
          sql += "retain_sample, uom, stock_uom, conversion_factor, sample_quantity, basic_rate, ";
          sql += "additional_cost, valuation_rate, allow_zero_valuation_rate, set_basic_rate_manually, ";
          sql += "basic_amount, amount, use_serial_batch_fields, expense_account, cost_center, ";
          sql += "actual_qty, transferred_qty, allow_alternative_item, parent, parentfield, parenttype) ";
          sql += f"values ('{item_code}-{reference}', now(), now(), 'Administrator', 'Administrator', '1', ";
          sql += f"'1', '0', 'Stores - JT', 'Goods In Transit - JT', '{item_code}', '{item_code}', ";
          sql += f"'0', '0', '{item_description}', 'Rewards', '{reg.quantity}', '{reg.quantity}', '0', '{uom}', ";
          sql += f"'{uom}', '1', '0', '{price_list_rate}', '0', '{price_list_rate}', '0', '0', ";
          sql += f"{price_list_rate}*{reg.quantity}, {price_list_rate}*{reg.quantity}, ";
          sql += f"'1', 'Stock Adjustment - JT', 'Main - JT', '{stock_qty}', '0', '0', 'REDEEM-{reference}', 'items', 'Stock Entry')";
          frappe.db.sql(sql, as_dict=0)
          
          sql = "insert into `tabStock Ledger Entry` (name, creation, modified, modified_by, owner, docstatus, ";
          sql += "idx, item_code, warehouse, posting_date, posting_time, posting_datetime, is_adjustment_entry, ";
          sql += "auto_created_serial_and_batch_bundle, voucher_type, voucher_no, voucher_detail_no, ";
          sql += "dependant_sle_voucher_detail_no, recalculate_rate, actual_qty, qty_after_transaction, ";
          sql += "incoming_rate, outgoing_rate, valuation_rate, stock_value, stock_value_difference, ";
          sql += "stock_queue, company, stock_uom, fiscal_year, has_batch_no, has_serial_no, is_cancelled, ";
          sql += "to_rename) values (";
          sql += f"'{item_code}-{reference}', now(), now(), 'Administrator', 'Administrator', '1', '0', ";
          sql += f"'{item_code}', 'Stores - JT', current_date, current_time, now(), '0', '0', 'Stock Entry', ";
          sql += f"'REDEEM-{reference}', '{item_code}-{reference}', '{item_code}-{reference}', '0', '-{reg.quantity}', ";
          sql += f"{new_qty}, '0', '0', {price_list_rate}, {total_cost},{item_cost},'[[{new_qty}, {price_list_rate}]]', ";
          sql += f"'Joel`s Place','{uom}','{fiscal_year}','0','0','0','1')";
          frappe.db.sql(sql, as_dict=0)
      else:
          sql = "wala"

      sql = "update `tabCustomer` set total_redeemed = total_redeemed + ";
      sql += f"{str_total_points}, points_balance = points_balance - {str_total_points} ";
      sql += f"where name = '{reg.customer_id}'";
      frappe.db.sql(sql, as_dict=0)
      
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")

