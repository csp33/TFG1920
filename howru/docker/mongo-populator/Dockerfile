FROM mongo
COPY patients.json /patients.json
COPY doctors.json /doctors.json
COPY pending_questions.json /pending_questions.json
COPY answered_questions.json /answered_questions.json
COPY questions.json /questions.json

CMD mongoimport --host mongo-dbs --db users --collection patients --type json --file /patients.json --jsonArray && \
    mongoimport --host mongo-dbs --db users --collection doctors --type json --file /doctors.json --jsonArray && \
    mongoimport --host mongo-dbs --db journal --collection pending_questions --type json --file /pending_questions.json --jsonArray --mode=upsert && \
    mongoimport --host mongo-dbs --db journal --collection answered_questions --type json --file /answered_questions.json --jsonArray --mode=upsert && \
    mongoimport --host mongo-dbs --db questions --collection questions --type json --file /questions.json --jsonArray --mode=upsert
