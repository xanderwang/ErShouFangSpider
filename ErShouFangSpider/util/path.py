# !/usr/bin/env python3
import os

ROOT_PATH: str = ""
DATA_PATH: str = ""


def _get_root_path():
    """
    获取 root path
    """
    file_path = os.path.realpath(__file__)
    util_path = os.path.dirname(file_path)
    project_path = os.path.dirname(util_path)
    root_path = os.path.dirname(project_path)
    return root_path


def _init_path():
    """
    初始化 path
    """
    global ROOT_PATH, DATA_PATH
    ROOT_PATH = _get_root_path()
    DATA_PATH = os.path.join(ROOT_PATH, "data")
    make_dir(DATA_PATH)


def make_dir(file_path: str, make_parent: bool = True):
    """
    如果不存在父文件夹，就创建父文件夹
    """
    dir_path = file_path
    if make_parent:
        dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


_init_path()

if __name__ == "__main__":
    data = {
        "ROOT_PATH": ROOT_PATH,
        "DATA_PATH": DATA_PATH
    }
    print("path:", data)
