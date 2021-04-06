#System Under Test - Description:

##Introduction

The system under test (SUT) is a simplified Customer Care system for call center operators where they can access and modify customers details, such as personal information (name, adress, nationailty and more) and device information (phone, tablet, and other devices).

The primary interface for an operator is via the webb GUI. 
The webb GUI in turn communicates via a REST API, which in turn communicates and stores information in an underlying database. 

##Features

###Add, modify, and delete customer
The system allows an operator to add new customers into the system, modify their information, and subsequently delete customers from the records.

###Add, modify, and delete equipment
A customer can also have equipment, for example a phone, tablet or other equipment.
The operator has the option to add pre-defined equipment to a customer which will have information such as equipment (type, model, IMEI) and SIM card if applicable (MSISDN, IMSI).

Currently the only way to add new products or add/change equipment into the system is via direct REST API calls.

##Ways of access

###Webb GUI
The primary way of access for an operator is via the webb interface, which will be located under: 

[http://localhost/](http://localhost/)

![](https://res.cloudinary.com/northern-test-consulting-ab/image/upload/v1553094835/customer_care_screenshot_yiewsb.png) 

###REST API

But it is also possible to access the system via REST API calls directly, see corresponding document for REST API documentation: **rest_api_documentation.pdf**
Base URL for REST API is:

[http://localhost:6399/](http://localhost:6399/)

###Database

Finally the information in the system is stored and modified inside a database (SQLite3) which can be accessed as a file under:

/home/pft/restapi/point-of-sale/pos.db 

![](https://res.cloudinary.com/northern-test-consulting-ab/image/upload/v1553073376/db_design_vw3up7.png) 