# bartalysis

# Build Instructions

## Tech Stack

- React
- TypeScript
- TailwindCSS

## Building the Frontend

First clone the project

```
git clone <githuburl>
```

Next change directory into the frontend directory

```
cd bartalysis
cd frontend
```

Then install dependencies and run server:

```
npm install
npm run dev
```

## Building the Backend

### Update Packages
```
sudo apt-get update
```

### Install SQLite3
```
sudo apt-get install sqlite3
```

### Install Protoc Compiler
First install the protoc package.
```
pip install protobuf==3.20.0
apt install -y protobuf-compiler
```
Then run the proto.py file. 
```
python backend/gtfs-rt/proto.py
```
This is required to pull data from GTFS-RT.

### Build the Database
Create the django user database.
```
python manage.py migrate
```
Create the BART database.
```
python manage.py migrate --database=bart
```