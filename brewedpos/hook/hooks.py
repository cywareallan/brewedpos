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
    "ConsAllan": {
        "on_update": "brewedpos.hook_consallan.api.ca_update",
 	 	"after_insert": "brewedpos.hook_consallan.api.ca_update"
 	}
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
