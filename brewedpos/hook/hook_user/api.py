from __future__ import unicode_literals
import frappe
import frappe.model
import frappe.model.document
from frappe import _
from frappe.model.document import Document
import hmac
import hashlib
import base64
#from frappe.integrations.utils import get_checkout_url
#########################################################
#  POS SETTINGS
#########################################################
def password_update (doc,event):
    sql = ""
    try:
      #  get the user
      user = frappe.db.get_value('POS Credentials', doc.name, fieldname="*", as_dict=1)

      key = "pjgabcarcis"
      b = bytearray()
      b.extend(map(ord, key))
      passw = base64.b64encode(user.passwd)
      digest = hmac.new(b, msg=passw, digestmod=hashlib.sha256).digest()
      #signature = base64.b64encode(digest).decode()

      #  SQL update
      sql  = "update `tabPOS Credentials` set "
      sql += f"encpass = '{digest}' "
      sql += f" where name = '{doc.name}'";

      #  Save it
      frappe.db.sql(sql, as_dict=0)
      frappe.db.commit()
    except Exception as dberr:
       #  Display the SQL statement and the error
       frappe.throw (f"{sql} ==> {dberr}")
