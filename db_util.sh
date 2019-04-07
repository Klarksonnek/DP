#!/usr/bin/env bash

ACTION=$1
read -p "DB username: " DB_USERNAME
read -s -p "DB password: " DB_PASSWORD
echo ""

DOMAIN="db-env.mienkofax.eu"
DB_NAME="statistiky"
TABLE_NAMES=(
    "measured_klarka"
    "measured_klarka_reduced"
    "measured_klarka_shower"
    "measured_klarka_shower_reduced"
    "measured_peto"
    "measured_peto_reduced"
    "measured_klarka_iqhome"
    "measured_klarka_iqhome_reduced"
    "measured_filtered_peto"
    "measured_filtered_peto_reduced"
    "measured_david"
    "measured_david_reduced"
)

EXPORT_DIR="tables"

if [[ ${ACTION} == "import" ]] ; then
    echo "import tables"

    for table in "${TABLE_NAMES[@]}"
    do
        rm -f ${table}.sql.tar.gz* ${table}.sql*

        wget ${DOMAIN}/${table}.sql.tar.gz -q --show-progress --progress=bar:force 2>&1
        tar -xvzf ${table}.sql.tar.gz

        mysql -u ${DB_USERNAME} -p ${DB_NAME} --password=${DB_PASSWORD} < ${table}.sql
        rm -f ${table}.sql.tar.gz* ${table}.sql*
    done
elif [[ ${ACTION} == "export" ]] ; then
    echo "export tables"
    rm -rf ${EXPORT_DIR}
    mkdir ${EXPORT_DIR}
    cd ${EXPORT_DIR}

    for table in "${TABLE_NAMES[@]}"
    do
        mysqldump -u ${DB_USERNAME} -p ${DB_NAME} --password=${DB_PASSWORD} ${table} > ${table}.sql
        tar -zcvf ${table}.sql.tar.gz ${table}.sql
        rm -rf ${table}.sql
    done
fi
