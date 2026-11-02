"""Publica la versión actual del índice en Zenodo, Hugging Face y Kaggle.

Descarga los ficheros vigentes de metlabs.io a `out/` y solo actúa si el CSV
ha cambiado desde la última versión de Zenodo (checksum MD5). Si publica,
escribe `out/published` para que el workflow cree la release de GitHub. Sin
dependencias:
Zenodo y Hugging Face por HTTP; Kaggle con su CLI oficial (lo instala el
workflow).

Variables: ZENODO_TOKEN, ZENODO_RECORD (cualquier versión del registro),
HF_TOKEN, HF_REPO, KAGGLE_DATASET (owner/slug). Kaggle usa KAGGLE_USERNAME y
KAGGLE_API_TOKEN del entorno.
"""

import base64
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import urllib.request

SOURCE = "https://metlabs.io/data"
NAMES = ["blockchain-regulation-index.csv", "blockchain-regulation-index.json"]
FILES = [os.path.join("out", name) for name in NAMES]
ZENODO = "https://zenodo.org/api"


def request(method, url, token, data=None, content_type="application/json"):
    body = data if isinstance(data, (bytes, type(None))) else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if body is not None:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req) as res:
        raw = res.read()
        return json.loads(raw) if raw else None


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def zenodo(token, record):
    latest = request("GET", f"{ZENODO}/records/{record}/versions/latest", token)
    remote = {f["key"]: f["checksum"].split(":")[-1] for f in latest["files"]}
    if remote.get("blockchain-regulation-index.csv") == md5(FILES[0]):
        print("Zenodo: sin cambios")
        return False
    draft = request("POST", f"{ZENODO}/deposit/depositions/{latest['id']}/actions/newversion", token)
    draft = request("GET", draft["links"]["latest_draft"], token)
    for f in draft["files"]:
        request("DELETE", f"{ZENODO}/deposit/depositions/{draft['id']}/files/{f['id']}", token)
    bucket = draft["links"]["bucket"]
    for path in FILES + ["README.md"]:
        name = os.path.basename(path)
        request("PUT", f"{bucket}/{name}", token, open(path, "rb").read(), "application/octet-stream")
    today = datetime.date.today().isoformat()
    metadata = draft["metadata"]
    metadata.update({"publication_date": today, "version": today.replace("-", ".")})
    metadata.pop("doi", None)
    request("PUT", f"{ZENODO}/deposit/depositions/{draft['id']}", token, {"metadata": metadata})
    done = request("POST", f"{ZENODO}/deposit/depositions/{draft['id']}/actions/publish", token)
    print("Zenodo:", done["doi"])
    return True


def huggingface(token, repo):
    lines = [json.dumps({"key": "header", "value": {"summary": f"Data refresh {datetime.date.today()}"}})]
    for path in FILES:
        content = base64.b64encode(open(path, "rb").read()).decode()
        lines.append(json.dumps({"key": "file", "value": {"content": content, "path": os.path.basename(path), "encoding": "base64"}}))
    request("POST", f"https://huggingface.co/api/datasets/{repo}/commit/main", token,
            "\n".join(lines).encode(), "application/x-ndjson")
    print("Hugging Face: actualizado")


def kaggle(dataset):
    folder = tempfile.mkdtemp()
    for path in FILES:
        shutil.copy(path, folder)
    json.dump({"id": dataset}, open(os.path.join(folder, "dataset-metadata.json"), "w"))
    subprocess.run(["kaggle", "datasets", "version", "-p", folder, "-m",
                    f"Data refresh {datetime.date.today()}"], check=True)
    print("Kaggle: nueva versión")


def download():
    os.makedirs("out", exist_ok=True)
    for name, path in zip(NAMES, FILES):
        urllib.request.urlretrieve(f"{SOURCE}/{name}", path)


if __name__ == "__main__":
    download()
    if zenodo(os.environ["ZENODO_TOKEN"], os.environ["ZENODO_RECORD"]):
        huggingface(os.environ["HF_TOKEN"], os.environ["HF_REPO"])
        kaggle(os.environ["KAGGLE_DATASET"])
        open(os.path.join("out", "published"), "w").write(datetime.date.today().isoformat())
