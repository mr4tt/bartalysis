# Bartalysis
Bartalysis is a web application that uses the Bay Area Rapid Transit (BART) API to provide route planning and service information for commuters.

[View Database Diagram](https://dbdiagram.io/e/668f06759939893dae9aa1cf/66b4fe388b4bb5230e9d5a10)

[View System Diagram](https://www.canva.com/design/DAGLzc3N0gs/6N3pEnIH_PEmKmy7Q-brtA/view?embed)

## Tech Stack

- React
- TypeScript
- TailwindCSS
- Python
- Django
- SQLite

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

Go to http://localhost:5173/ to access the webpage

## Building the Backend

### Update and Install Packages

```
sudo apt-get update
pip install -r requirements.txt
```

### Create Protoc Compiler

Install proto-buf.

```
sudo apt-get install -y protobuf-compiler
```

Run the proto.py file.

```
python proto.py
```

Ensure the gtfs_realtime_pb2.py file is located in the gtfs-rt directory. This is required to pull data from GTFS-RT.

### Build the Database

Create the django user database.

```
python manage.py migrate
```

Create the BART database.

```
python manage.py migrate --database=bart
```