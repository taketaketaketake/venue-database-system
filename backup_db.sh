

#!/bin/bash
cd /Users/Zach/Github_Projects/airbnb-event-system
mkdir -p data/backups
TIMESTAMP=$(date +%F_%H-%M-%S)
cp data/venues.db data/backups/venues_backup_${TIMESTAMP}.db
echo "Backup created: data/backups/venues_backup_${TIMESTAMP}.db" >> data/logs/backup.log
# Keep only the last 7 backups
ls -t data/backups/venues_backup_*.db | tail -n +8 | xargs -I {} rm -- {} 2>/dev/null
