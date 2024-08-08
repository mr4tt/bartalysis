# Bartalysis
Bartalysis is a web application that uses the Bay Area Rapid Transit (BART) API to provide route planning and service information for commuters.

## Database Diagram

<iframe width="700" height="400" src='https://dbdiagram.io/e/668f06759939893dae9aa1cf/66b4fe388b4bb5230e9d5a10'> </iframe>

## System Diagram

<div style="position: relative; width: 75%; height: 0; padding-top: 90.0000%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGLzc3N0gs&#x2F;6N3pEnIH_PEmKmy7Q-brtA&#x2F;view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>

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