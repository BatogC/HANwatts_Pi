now=$(date +%F)
cp /mnt/dav/Data/modbusData.db /mnt/dav/Data/$now.modbusData.db
sqlite3 /mnt/dav/Data/modbusData.db <<'END_SQL'
.timeout 2000
DELETE FROM Battery;
DELETE FROM Demonstration;
DELETE FROM Grid;
DELETE FROM PV;
DELETE FROM Reserve;
DELETE FROM sqlite_sequence;
END_SQL
cp /mnt/dav/Data/usertable.sqlite3 /mnt/dav/Data/$now.usertable.sqlite3
sqlite3 /mnt/dav/Data/usertable.sqlite3 <<'END_SQL'
.timeout 2000
DELETE FROM measurements;
END_SQL

cp /media/DATABASE/modbusData.db /media/DATABASE/$now.modbusData.db
sqlite3 /media/DATABASE/modbusData.db <<'END_SQL'
.timeout 2000
DELETE FROM Battery;
DELETE FROM Demonstration;
DELETE FROM Grid;
DELETE FROM PV;
DELETE FROM Reserve;
DELETE FROM sqlite_sequence;
END_SQL
cp /media/DATABASE/usertable.sqlite3 /media/DATABASE/$now.usertable.sqlite3
sqlite3 /media/DATABASE/usertable.sqlite3 <<'END_SQL'
.timeout 2000
DELETE FROM measurements;
END_SQL

exit 0