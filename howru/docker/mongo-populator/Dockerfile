FROM mongo
COPY patients.json /patients.json
COPY doctors.json /doctors.json
#COPY journals.json /journals.json
#COPY configs.json /configs.json

CMD mongoimport --host mongo-dbs --db chatbot_users --collection patients --type json --file /patients.json --jsonArray && \
    mongoimport --host mongo-dbs --db chatbot_users --collection doctors --type json --file /doctors.json --jsonArray
    #mongoimport --host mongo-dbs --db journals --collection patients --type json --file /journals.json --jsonArray --mode=upsert
    #mongoimport --host mongo-dbs --db configs --collection patients --type json --file /configs.json --jsonArray --mode=upsert
