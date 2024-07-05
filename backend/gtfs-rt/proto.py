import requests
import subprocess
import os

def generate_proto_python_classes():
    url = "https://gtfs.org/realtime/gtfs-realtime.proto"
    path = "gtfs-realtime.proto"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    subprocess.run(["protoc", "--python_out=.", "gtfs-realtime.proto"])
    os.remove(path)

generate_proto_python_classes()