import os
import os.path as osp
import requests
import tarfile
import zipfile
from scipy.fft import dst
from pathlib import Path

from tqdm import tqdm
import connexion

from pplabel.config import data_base_dir

sample_projects = {
    "classification": "https://bj.bcebos.com/paddlex/datasets/vegetables_cls.tar.gz",
    "detection": "https://bj.bcebos.com/paddlex/datasets/insect_det.tar.gz",
    "semanticSegmentation": "https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz",
    "instanceSegmentation": "",  # todo
    "keypointDetection": "",
}


sample_projects = {
    "classification": "http://localhost:1111/vegetables_cls.tar.gz",
    "detection": "http://localhost:1111/insect_det.tar.gz",
    "semanticSegmentation": "http://localhost:1111/optic_disc_seg.tar.gz",
    "instanceSegmentation": "",  # todo
    "keypointDetection": "",
}


def download_file(url, dst_path, chunk_size=8192):
    local_size = 0
    if osp.exists(dst_path):
        local_size = osp.getsize(dst_path)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        if int(r.headers["Content-Length"]) == local_size:
            print(f"File {osp.basename(dst_path)} already exists, skipping.")
            return
        with open(dst_path, "wb") as f:
            for chunk in tqdm(
                r.iter_content(chunk_size=chunk_size),
                desc="Downloading",
                total=int(r.headers["Content-Length"]) // chunk_size + 1,
            ):
                f.write(chunk)


def extract(archive, dst_fdr):
    archive = str(archive)
    if archive.endswith((".tar.gz", ".tar")):
        f = tarfile.open(archive)
    elif archive.endswith(".zip"):
        f = zipfile.open(archive)
    f.extractall(path=dst_fdr)
    f.close()


def load_sample():
    task_category = connexion.request.json.get("task_category")
    print(task_category)

    sample_folder = Path(data_base_dir) / "sample_dataset"
    sample_folder.mkdir(exist_ok=True)
    url = sample_projects[task_category]
    archive_path = sample_folder / url.split("/")[-1]

    download_file(url, archive_path)

    extract(archive_path, sample_folder)

    extract_path = sample_folder.parent / archive_path.name.split(".")[0]
    print(extract_path)

    # TODO: import dataset