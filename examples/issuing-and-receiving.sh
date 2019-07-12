#############################################################################################
#####     Create an Invoice                                                             #####
#############################################################################################

curl -X POST http://localhost:5000/invoice \
    -H 'Content-Type: application/json' \
    -d '{
        "electionId": 1,
        "issuedTo": 2,
        "issuingOfficeId": 3,
        "receivingOfficeId": 4
    }'

#    {
#        "confirmed": false,
#        "electionId": 1,
#        "invoiceId": 1,
#        "issuedAt": "2019-07-12T05:51:20.533473+00:00",
#        "issuedBy": 2,
#        "issuedTo": 2,
#        "issuingOfficeId": 3,
#        "receivingOfficeId": 4
#    }


#############################################################################################
#####     Add Stationary to the Invoice                                                 #####
#############################################################################################

curl -X POST \
    http://localhost:5000/invoice/1/stationary-item \
    -H 'Content-Type: application/json' \
    -d '{
        "stationaryItemId": 1
    }'

#    {
#        "invoiceId": 1,
#        "received": false,
#        "receivedAt": null,
#        "receivedBy": null,
#        "receivedFrom": null,
#        "receivedOfficeId": null,
#        "stationaryItem": {
#            "stationaryItemId": 1,
#            "stationaryItemType": "Ballot"
#        },
#        "stationaryItemId": 1
#    }


curl -X POST \
    http://localhost:5000/invoice/1/stationary-item \
    -H 'Content-Type: application/json' \
    -d '{
        "stationaryItemId": 2
    }'

#    {
#        "invoiceId": 1,
#        "received": false,
#        "receivedAt": null,
#        "receivedBy": null,
#        "receivedFrom": null,
#        "receivedOfficeId": null,
#        "stationaryItem": {
#            "stationaryItemId": 2,
#            "stationaryItemType": "Ballot"
#        },
#        "stationaryItemId": 2
#    }


curl -X POST \
    http://localhost:5000/invoice/1/stationary-item \
    -H 'Content-Type: application/json' \
    -d '{
        "stationaryItemId": 3
    }'

#    {
#        "invoiceId": 1,
#        "received": false,
#        "receivedAt": null,
#        "receivedBy": null,
#        "receivedFrom": null,
#        "receivedOfficeId": null,
#        "stationaryItem": {
#            "stationaryItemId": 3,
#            "stationaryItemType": "Ballot"
#        },
#        "stationaryItemId": 3
#    }



#############################################################################################
#####     Confirm the Invoice                                                           #####
#############################################################################################

curl -X PUT http://localhost:5000/invoice/1/confirm

#    {
#        "confirmed": true,
#        "electionId": 1,
#        "invoiceId": 1,
#        "issuedAt": "2019-07-12T05:45:43.804664+00:00",
#        "issuedBy": 2,
#        "issuedTo": 2,
#        "issuingOfficeId": 3,
#        "receivingOfficeId": 4
#    }


#############################################################################################
#####     Retrieve Invoices                                                             #####
#############################################################################################

curl -X GET http://localhost:5000/invoice?limit=2&offset=0&electionId=1&receivingOfficeId=4

#    [
#        {
#            "confirmed": false,
#            "electionId": 1,
#            "invoiceId": 1,
#            "issuedAt": "2019-07-11T11:16:51.718014+00:00",
#            "issuedBy": 2,
#            "issuedTo": 2,
#            "issuingOfficeId": 3,
#            "receivingOfficeId": 4
#        },
#        {
#            "confirmed": false,
#            "electionId": 1,
#            "invoiceId": 2,
#            "issuedAt": "2019-07-11T11:16:54.613369+00:00",
#            "issuedBy": 2,
#            "issuedTo": 2,
#            "issuingOfficeId": 3,
#            "receivingOfficeId": 4
#        }
#    ]



#############################################################################################
#####     Retrieve Stationary Items of an Invoice                                       #####
#############################################################################################

curl -X GET http://localhost:5000/invoice/1/stationary-item?limit=20&offset=0

#    [
#        {
#            "invoiceId": 1,
#            "received": false,
#            "receivedAt": null,
#            "receivedBy": null,
#            "receivedFrom": null,
#            "receivedOffice": null,
#            "stationaryItem": {
#                "stationaryItemId": 1,
#                "stationaryItemType": "Ballot"
#            },
#            "stationaryItemId": 1
#        },
#        {
#            "invoiceId": 1,
#            "received": false,
#            "receivedAt": null,
#            "receivedBy": null,
#            "receivedFrom": null,
#            "receivedOffice": null,
#            "stationaryItem": {
#                "stationaryItemId": 2,
#                "stationaryItemType": "Ballot"
#            },
#            "stationaryItemId": 2
#        },
#        {
#            "invoiceId": 1,
#            "received": false,
#            "receivedAt": null,
#            "receivedBy": null,
#            "receivedFrom": null,
#            "receivedOffice": null,
#            "stationaryItem": {
#                "stationaryItemId": 3,
#                "stationaryItemType": "Ballot"
#            },
#            "stationaryItemId": 3
#        }
#    ]
#


#############################################################################################
#####     Retrieve Stationary Items of an Invoice                                       #####
#############################################################################################

curl -X PUT http://localhost:5000/invoice/1/stationary-item/1/received \
    -H 'Content-Type: application/json' \
    -d '{
        "receivedFrom": 1,
        "receivedOfficeId": 1
    }'


#    {
#        "invoiceId": 1,
#        "received": true,
#        "receivedAt": null,
#        "receivedBy": null,
#        "receivedFrom": null,
#        "receivedOffice": null,
#        "stationaryItem": {
#            "stationaryItemId": 1,
#            "stationaryItemType": "Ballot"
#        },
#        "stationaryItemId": 1
#    }
