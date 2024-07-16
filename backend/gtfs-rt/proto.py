import requests
import subprocess
import os
import tempfile

def generate_proto_python_classes():
    url = "https://gtfs.org/realtime/gtfs-realtime.proto"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "gtfs-realtime.proto")
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        subprocess.run(["protoc", "--proto_path=" + temp_dir, "--python_out=.", path])

generate_proto_python_classes()