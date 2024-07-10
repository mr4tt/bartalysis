# bartalysis

# Build Instructions

## Building the Backend

### Update Packages
```
sudo apt-get update
```

### Install SQLite3
```
sudo apt-get install sqlite3
```

### Pulling GTFS-RT Data
Install the protobuf compiler in order to create the file required to parse GTFS-RT data.
```
apt install -y protobuf-compiler
```
Create the parsing file.
```
python backend/gtfs-rt/proto.py
```
###