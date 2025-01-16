import os
import subprocess
import shutil
import time

from Version import VERSION_STR

PY_FILE = "game.py"
TARGET_NAME = "Checkers Blitz"
TARGET_DIR = "dist"

if __name__ == '__main__':
    print("[ Building Checkers Blitz ]")
    start = time.time()
    deploy_cmd = f"cxfreeze --script {PY_FILE} --target-name=\"{TARGET_NAME}\" --target-dir {TARGET_DIR} --base-name=gui"
    deploy_cmd += f" --icon=resources/imgs/icon.ico"
    print(deploy_cmd)
    subprocess.run(deploy_cmd, shell=True)
    shutil.copytree("resources", f"{TARGET_DIR}/resources")
    print("== Build Complete ==")
    elapsed = time.time() - start
    print(f"  Build Time: {elapsed} ms")
    print(f"  Dist: {TARGET_DIR}/")
