app_name = "brewedpos"
app_title = "Brewed POS"
app_publisher = "Software Brewery Inc."
app_description = "Point of Sale"
app_email = "support@softwarebrewery.dev"
app_license = "mit"
# ---------------
# Document Events
# ---------------
# Sync ERP records with the POS database
doc_events = {
    #"Loyalty Manual Entry": {
 	#	"after_insert": "brewedpos.hook_manual_entry.api.validate_entry"
 	#},
    #"Loyalty Card Type": {
 	#	"before_insert": "brewedpos.hook_customer_card.api.validate_account"
 	#}
 	# "Company": {
 	# 	"on_trash": "brewedpos.hook_company.api.company_delete",
    #     "on_update": "brewedpos.hook_company.api.company_update",
 	# 	"after_insert": "brewedpos.hook_company.api.company_update"
 	# },
    # "Branch": {
 	# 	"on_trash": "brewedpos.hook_branch.api.branch_delete",
    #     "on_update": "brewedpos.hook_branch.api.branch_update",
 	# 	"after_insert": "brewedpos.hook_branch.api.branch_update"
 	# },
    # "POS Branch Settings": {
 	# 	"on_trash": "brewedpos.hook_settings.api.settings_delete",
    #     "on_update": "brewedpos.hook_settings.api.settings_update",
 	# 	"after_insert": "brewedpos.hook_settings.api.settings_update"
 	# },
    # "POS Register": {
 	# 	"on_trash": "brewedpos.hook_register.api.register_delete",
    #     "on_update": "brewedpos.hook_register.api.register_update",
 	# 	"after_insert": "brewedpos.hook_register.api.register_update"
 	# },
    #  "POS Credentials": {
    #     "on_update": "brewedpos.hook_user.api.password_update",
 	#  	"after_insert": "brewedpos.hook_user.api.password_update"
 	# }
}

fixtures = ['Customer', 'Loyalty Transaction Type', 'Loyalty Application Type', 'Loyalty Reward Type', 'Loyalty Remap Type', 'Loyalty Attribute Type', 'Loyalty Attribute', 'Loyalty PIN Change Reason', 'Loyalty Deactivate Reasons', 'Loyalty Card Type', 'Loyalty Customer Attribute', 'Loyalty Rewards', 'Loyalty Redemption', 'Loyalty PIN Entry', 'Loyalty Card Replacement', 'Loyalty Account Activation', 'Loyalty Account Deactivation', 'Loyalty Add Points', 'Custom Field', 'Property Setter']