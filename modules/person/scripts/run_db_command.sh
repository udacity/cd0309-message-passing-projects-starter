# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=person
export CT_DB_NAME=person-db


cat ./db/ddl.sql | kubectl exec postgres-person-db-6786975574-2zs6q -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ./db/data.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"



cat ./db/ddl.sql | kubectl exec postgres-person-db-6786975574-2zs6q -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"