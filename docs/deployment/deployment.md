# How to do a clean deployment

Create an empty database

`create database elections character set utf8mb4 collate utf8mb4_unicode_ci;`

SSH into backend server and execute following

`python manage.py db upgrade`

## Create a new election

Send POST request to /election endpoint

Headers

  * Content-Type - application/x-www-form-urlencoded
  * Authorization - Bearer bearer-token-of-an-admin-user

Body Parameters

  Texts

    electionName
    electionTemplateName

  CSV Files

    invalidVoteCategoriesDataset
    partyCandidatesDataset
    pollingStationsDataset
    postalCountingCentresDataset
    numberOfSeatsDataset

## Create Users

Get election root token by calling `/election/{electionId}/root-token` endpoint

Decode JWT token recieved and note down AreaID value for each district.

Create a ***Tab Seperated File - TSV***  of users with relevant AreaIDs

|NIC/ SLIN | Name w/ initials |	Mobile Number|	FName |	LName |	User Name |	Password  |	otpBackupCodes  |	role  |	area_assign_data_editor |	area_assign_admin |	area_assign_pol_div_rep_view  |	area_assign_pol_div_rep_verf  |	area_assign_elc_dis_rep_view  |	area_assign_elc_dis_rep_verf  |	area_assign_nat_dis_rep_view  |	area_assign_nat_dis_rep_verf  |	area_assign_ec_leadership |	Areas |	Role Description  |
| -------- | ---------------- | -----------  |  ----- | ----- | --------- | --------  |  -------------- | ----  | ----------------------- | ----------------- | ----------------------------  |  -------------------------- |  ---------------------------- |  ---------------------------- |  ---------------------------- |  ---------------------------- |  -------------------------  | ----- | ----------------  |
|123456789V| T Mendis |	777777777 |	Tom |	Mendis  |	test-username-1 |	test-password-1  |	177078, 172208  |	tab_data_editor |	[{'areaId':121212,'areaName':'Colombo'}] | | | | | | | | |	Colombo |	Data Editor & Verifier for Colombo  |
|123456789V |P Pan |	777777777 |	Peter |	Pan  |	test-username-2 |	test-password-2  |	186804, 124068  |	tab_pol_div_rep_view | | |  [{'areaId':121212,'areaName':'Colombo'}] | | | | | | |	Colombo |	Polling Division Report Viewer for Colombo  |


Open [AddSuperTenantUsers.jmx](AddSuperTenantUsers.jmx) using Apache Jmeter

Add relevant argumants.

get ***adminCredentials*** by base64 encoding admin username and password as ***username:password***

upload .tsv file into jmeter and execute the script.