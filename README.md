# Business_Analytics
A Comprehensive Sales and Order Management Database
https://www.kaggle.com/datasets/himelsarder/business-database
This is a relational database schema for a sales and order management system, designed to track customers, employees, products, orders, and payments. 

#**Stage 1 - dataset preprocessing.**
# MySQL → PostgreSQL Migration(pgAdmin)
---
I installed pgloader which is a migration tool and then ran this command on the terminal:

pgloader mysql://user:password@host/source_db postgresql://pguser:pgpass@host/target_db

this one just transforms the MySQL code to PostgreSQL.

#**Dataset completion**
I encountered the problem that dataset is not huge enough for further research. So i decided to write a script which fulfills the entire dataset. 
Script.py is the one which does it.
