import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
from dataloader import csvloader

#export PG_HOME=/Library/PostgreSQL/12 
#export PATH=$PATH:$PG_HOME/bin

#connect to the database
connection = pg.connect("dbname=consumer_complaints user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

engine = create_engine('postgresql://postgres:root@localhost/consumer_complaints')
#dialect+driver://username:password@host:port/database

#refresh tables
#cursor.execute("DROP TABLE bank_account_complaints;")



#create the bank_account_complaints table
cursor.execute("CREATE TABLE IF NOT EXISTS bank_account_complaints (\
 complaint_id text PRIMARY KEY,\
 date_received date,\
 product text,\
 sub_product text,\
 issue text,\
 sub_issue text,\
 consumer_complaint_narrative text,\
 company_public_response text,\
 company text,\
 state text,\
 zip_code text,\
 tags text,\
 consumer_consent_provided text,\
 submitted_via text,\
 date_sent date,\
 company_response_to_consumer text,\
 timely_response text,\
 consumer_disputed text);;")

#create the credit_card_complaints table
cursor.execute("CREATE TABLE IF NOT EXISTS credit_card_complaints (\
 complaint_id text PRIMARY KEY,\
 date_received date,\
 product text,\
 sub_product text,\
 issue text,\
 sub_issue text,\
 consumer_complaint_narrative text,\
 company_public_response text,\
 company text,\
 state text,\
 zip_code text,\
 tags text,\
 consumer_consent_provided text,\
 submitted_via text,\
 date_sent date,\
 company_response_to_consumer text,\
 timely_response text,\
 consumer_disputed text);;")

#initiate loading csv
csvloader(engine, '../datasets/Credit_Card_Complaints.csv', 'credit_card_complaints_df')
csvloader(engine, '../datasets/Bank_Account_or_Service_Complaints.csv', 'bank_account_complaints_df')

#query demos

def run_command(command):
   cursor.execute(command)
   print(cursor.statusmessage)

def run_query(query):
   print(pd.read_sql(query, con=engine))

#EXAMPLE - Count all non null rows
query = 'SELECT count(*) FROM credit_card_complaints_df;'
run_query(query)

#EXAMPLE - Count all non null rows where the consumer_complaint_narrative field exists
query = 'SELECT count(*) FROM credit_card_complaints_df WHERE consumer_complaint_narrative IS NOT NULL;'
run_query(query)

#EXAMPLE - Count all non null rows where the consumer_complaint_narrative field does not exist
query = 'SELECT count(*) FROM credit_card_complaints_df WHERE consumer_complaint_narrative IS NULL;'
run_query(query)

#SECTION - VIEWS - Used for reusability, security and improving performance since we can temporarily filter down parts of the dbs

#EXAMPLE - Create four views for credit card and bank account tables filtering them by consumer_complaint_narrative

command = 'CREATE OR REPLACE VIEW credit_card_df_w_complaints AS SELECT * FROM credit_card_complaints_df WHERE consumer_complaint_narrative IS NOT NULL;'
run_command(command)

command = 'CREATE OR REPLACE VIEW credit_card_df_wo_complaints AS SELECT * FROM credit_card_complaints_df WHERE consumer_complaint_narrative IS NULL;'
run_command(command)

command = 'CREATE OR REPLACE VIEW bank_account_df_w_complaints AS SELECT * FROM bank_account_complaints_df WHERE consumer_complaint_narrative IS NOT NULL;'
run_command(command)

command = 'CREATE OR REPLACE VIEW bank_account_df_wo_complaints AS SELECT * FROM bank_account_complaints_df WHERE consumer_complaint_narrative IS NULL;'
run_command(command)

#make execution changes permanant, otherwise views will not appear
connection.commit()

#In order to preview all columns use this line
#pd.options.display.max_columns = None

#Check each view
query = 'SELECT * FROM credit_card_df_w_complaints LIMIT 5;'
run_query(query)

#SECTION - Unions - Since we have two pairs of views with the same columns and data types, we can create a union view for complaints/no complaints
#Make sure the datatypes in the dataframe are the same! These will need to be done for every non-standardized dataset

command = 'CREATE OR REPLACE VIEW df_w_complaints AS (SELECT * FROM credit_card_df_w_complaints) UNION ALL (SELECT * FROM bank_account_df_w_complaints);'
run_command(command)

command = 'CREATE OR REPLACE VIEW df_wo_complaints AS (SELECT * FROM credit_card_df_wo_complaints) UNION ALL (SELECT * FROM bank_account_df_wo_complaints);'
run_command(command)

#make execution changes permanant, otherwise views will not appear
connection.commit()

#Check example view count
query = 'SELECT count(*) FROM df_w_complaints;'
run_query(query)

#SECTION - Intersect/Except - Intersect will return the rows in the resultant sets of both queries while except returns all rows in the first query but not the second 

#Retrieve the amount of rows for credit_card_df_wo_complaints
query = 'SELECT count(*) FROM credit_card_df_wo_complaints;'
run_query(query)

#Retrieve the intersection between credit_card_df_wo_complaints and df_wo_complaints, it should match
#Adding ppg to the end resolves any alias requests
query = 'SELECT count(*) FROM (SELECT * FROM credit_card_df_wo_complaints INTERSECT SELECT * FROM df_wo_complaints) ppg;'
#run_query(query)

#SECTION - String Concatenation - Used to turn multiple strings fields into one
strconcat = 'complaint_id || \'-\' || product || \'-\' || company || \'-\' || zip_code AS concat'
query = 'SELECT complaint_id, product, company, zip_code, complaint_id, '+strconcat+' FROM df_w_complaints LIMIT 5;'
run_query(query)

#SECTION - Subqueries - Are used to nested queries
subquery = 'SELECT ccc.complaint_id, ccc.product, ccc.company, ccc.zip_code FROM credit_card_complaints_df ccc WHERE zip_code=\'91701\''
query = 'SELECT ccd.complaint_id, ccd.product, ccd.company, ccd.zip_code FROM ('+subquery+') ccd LIMIT 10;'
run_query(query)

#As a finance company we might want to group the complaints by the states with the most complaints and then by zipcode among other metrics
#This will then be repeated for the competitors
subquery = 'SELECT ccc.company, ccc.state, ccc.zip_code, count(ccc.complaint_id) AS complaint_count FROM credit_card_complaints_df ccc \
WHERE state IS NOT NULL \
GROUP BY company, state, zip_code \
ORDER BY complaint_count DESC \
'

#Now use this as a subquery to find the states with the highest complaints
query = 'SELECT ppt.company, ppt.state, max(ppt.complaint_count) AS complaint_count FROM ('+subquery+') ppt \
GROUP BY ppt.company, ppt.state \
ORDER BY complaint_count DESC \
'
subquery = query

innerjoinfirst = 'SELECT company, state, zip_code, count(complaint_id) AS complaint_count FROM credit_card_complaints_df \
WHERE state IS NOT NULL \
GROUP BY company, state, zip_code'

innerjoinsecond = 'SELECT ppx.company,  max(ppx.complaint_count) AS complaint_count FROM ('+subquery+') ppx GROUP BY ppx.company'

query = 'SELECT ens.company, ens.state, ens.zip_code, ens.complaint_count FROM \
('+innerjoinfirst+') ens INNER JOIN ('+innerjoinsecond+') apx \
ON apx.company=ens.company \
AND apx.complaint_count = ens.complaint_count \
ORDER BY 4 DESC \
'
run_query(query)

#SECTION - Data type casting
query = 'SELECT CAST(complaint_id AS float) AS complaint_id \
FROM bank_account_complaints_df \
LIMIT 1; \
'
run_query(query)

newview = 'SELECT CAST(complaint_id AS INT) AS complaint_id, \
product, issue, company, state, zip_code, submitted_via \
FROM bank_account_complaints_df \
   WHERE state=\'CA\' \
      AND company= \'Wells Fargo & Company\''
run_query(newview)

command = 'CREATE OR REPLACE VIEW wells_fargo_complaints AS ('+newview+');'
run_command(command)

#make execution changes permanant
connection.commit()

query = 'SELECT * FROM wells_fargo_complaints LIMIT 15;'
run_query(query)

#Return sorted list of companies by record amounts
query = 'SELECT company, count(company) AS company_amount FROM credit_card_complaints_df GROUP BY company ORDER BY company_amount DESC LIMIT 15;'
run_query(query)

#Return sorted list of companies by record amounts
query = 'SELECT company, count(company) AS company_amount, (SELECT COUNT(*) FROM credit_card_complaints_df) AS TOTAL FROM credit_card_complaints_df GROUP BY company ORDER BY company_amount DESC LIMIT 15;'
run_query(query)

#Add a percentage column
subquery = 'SELECT company, count(company) AS company_amount, (SELECT COUNT(*) FROM credit_card_complaints_df) AS total FROM credit_card_complaints_df GROUP BY company ORDER BY company_amount DESC'
query = 'SELECT ppx.company, ppx.company_amount, ppx.total, ((CAST(ppx.company_amount AS double precision)) / (CAST(ppx.total AS double precision)) * 100) AS percent FROM ('+subquery+') ppx LIMIT 15'
run_query(query)

#tst = cursor.fetchone()
#print(tst)