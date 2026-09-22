from pathlib import Path
from subprocess import Popen, PIPE
import threading

BASE_DIR = Path(__file__).resolve().parent
SERVER_PATH = BASE_DIR / "minecraft-servers" / "survival"
JAR_NAME = "paper-26.2-128.jar"

processes = {}


def read_output(server_id, process):
    for line in process.stdout:
        print(f"[{server_id}] {line}", end="")


def start_server():
    if "survival" in processes:
        print("Le serveur est déjà lancé.")
        return False

    jar_path = SERVER_PATH / JAR_NAME

    if not SERVER_PATH.exists():
        print(f"Dossier introuvable : {SERVER_PATH}")
        return False

    if not jar_path.exists():
        print(f"Fichier JAR introuvable : {jar_path}")
        return False

    process = Popen(
        [
            "java",
            "-Xms1G",
            "-Xmx2G",
            "-jar",
            JAR_NAME,
            "nogui"
        ],
        cwd=str(SERVER_PATH),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        bufsize=1
    )

    processes["survival"] = process

    threading.Thread(
        target=read_output,
        args=("survival", process),
        daemon=True
    ).start()

    print("Serveur démarré.")
    return True


def stop_server():
    process = processes.get("survival")

    if process is None:
        print("Le serveur n'est pas lancé.")
        return False

    if process.stdin:
        process.stdin.write("stop\n")
        process.stdin.flush()

    process.wait(timeout=30)
    processes.pop("survival", None)

    print("Serveur arrêté.")
    return True
