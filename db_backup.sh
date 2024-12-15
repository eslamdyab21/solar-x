#! /bin/bash

# Set the database name to a variable. 
source "$(pwd)/mysql_database/.env"

echo "Pulling Database: This may take a few minutes"


# Set the folder where the database backup will be stored
backupfolder=/home/dyab/backups


sqlfile=$backupfolder/$DATABASE_NAME-$(date +%d-%m-%Y_%H-%M-%S).sql
zipfile=$backupfolder/$DATABASE_NAME-$(date +%d-%m-%Y_%H-%M-%S).gz

# Create a backup

if docker exec -i $DATABASE_HOST mysqldump -uroot -p$DATABASE_PASSWORD $DATABASE_NAME > $sqlfile;
then
    echo 'Sql dump created'
    # Compress backup
    if gzip -c $sqlfile > $zipfile;
    then
	echo 'The backup was successfully compressed'
    else
        echo 'Error compressing backupBackup was not created!'
	exit
    fi
    rm $sqlfile
else
   echo 'mysql return non-zero code No backup was created!'
   exit
fi

# cronjob for scheduling the backup
# # ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                       
# │ │ │ │ │
# │ │ │ │ │
# * * * * *  command_to_execute
# every midnight of everyday
#0 0 * * * /home/dyab/Documents/projects/solar-x/db_backup.sh