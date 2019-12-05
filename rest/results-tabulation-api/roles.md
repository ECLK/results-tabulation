# Roles

Following roles are defined and assigned to users in the identity server 

| Roles                              	| role_name            	| role_claim                   	|
|------------------------------------	|----------------------	|------------------------------	|
| Admin                              	| tab_admin            	| area_assign_admin            	|
| Data Editor                        	| tab_data_editor      	| area_assign_data_editor      	|
| Polling Division Report Viewer     	| tab_pol_div_rep_view 	| area_assign_pol_div_rep_view 	|
| Polling Division Report Verifier   	| tab_pol_div_rep_verf 	| area_assign_pol_div_rep_verf 	|
| Electoral District Report Viewer   	| tab_elc_dis_rep_view 	| area_assign_elc_dis_rep_view 	|
| Electoral District Report Verifier 	| tab_elc_dis_rep_verf 	| area_assign_elc_dis_rep_verf 	|
| National Report Viewer             	| tab_nat_dis_rep_view 	| area_assign_nat_dis_rep_view 	|
| National Report Verifier           	| tab_nat_dis_rep_verf 	| area_assign_nat_dis_rep_verf 	|
| EC Leadership                      	| tab_ec_leadership    	| area_assign_ec_leadership    	|

These come to the api via the JWT token in following format.

```
{
 "http://wso2.org/claims/role": [
  "tab_admin",
  "tab_data_editor",
  "tab_pol_div_rep_view",
  "tab_pol_div_rep_verf",
  "tab_elc_dis_rep_view",
  "tab_elc_dis_rep_verf",
  "tab_nat_dis_rep_view",
  "tab_nat_dis_rep_verf",
  "tab_ec_leadership"
 ],
 "http://wso2.org/claims/username": "dinuka",
 "http://wso2.org/claims/area_assign_admin": "[]",
 "http://wso2.org/claims/area_assign_data_editor": "[{'areaId': 2, 'areaName': '01 - Colombo'}]",
 "http://wso2.org/claims/area_assign_pol_div_rep_view": "[{'areaId': 2, 'areaName': '01 - Colombo'}]",
 "http://wso2.org/claims/area_assign_pol_div_rep_verf": "[{'areaId': 2, 'areaName': '01 - Colombo'}]",
 "http://wso2.org/claims/area_assign_elc_dis_rep_view": "[{'areaId': 2, 'areaName': '01 - Colombo'}]",
 "http://wso2.org/claims/area_assign_elc_dis_rep_verf": "[{'areaId': 2, 'areaName': '01 - Colombo'}]",
 "http://wso2.org/claims/area_assign_nat_dis_rep_view": "[{'areaId': 1, 'areaName': 'Sri Lanka'}]",
 "http://wso2.org/claims/area_assign_nat_dis_rep_verf": "[{'areaId': 1, 'areaName': 'Sri Lanka'}]",
 "http://wso2.org/claims/area_assign_ec_leadership": "[{'areaId': 1, 'areaName': 'Sri Lanka'}]"
}
```

