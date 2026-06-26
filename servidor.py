from flask import Flask, request
from datetime import datetime
import json
import ntplib
import time
import threading
import requests
import os
import numpy as np


app = Flask(__name__)

# =========================
# CONFIG EXPERIMENTO
# =========================

experiment_name = input("Nombre del experimento: ")

output_dir1 = f"results/{experiment_name}"
output_dir2 = f"resultsThrouhput/{experiment_name}"
os.makedirs(output_dir1, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)

LATENCY_FILE = f"{output_dir1}/latencies.jsonl"
LATENCY_STATS_FILE = f"{output_dir1}/latency_stats.json"
THROUGHPUT_FILE = f"{output_dir2}/throughput.json"

latencies = []

CONTROL_SERVER = "172.31.232.42:5000"

TEST_DURATION = 60 # segundos
WARMUP_SAMPLES = 100

msg_count = 0
warmup_count = 0

warmup_done = False
experiment_finished = False

def esperar_inicio():
    print("Esperando orden de inicio...")

    while True:
        try:
            r = requests.get(f"http://{CONTROL_SERVER}/status", timeout=1)

            if r.json()["start"]:
                print("Orden recibida. Iniciando experimento...")
                return

        except Exception:
            pass

        time.sleep(0.1)

# =========================
# NTP OFFSET
# =========================
def calcular_offset_local(ip_servidor, puerto=123):
    cliente = ntplib.NTPClient()
    try:
        respuesta = cliente.request(ip_servidor, port=puerto, version=3)
        return respuesta.offset
    except:
        return 0.0

mi_offset = calcular_offset_local("172.31.232.59", 123)
print(f"Offset consumidor: {mi_offset*1000:.3f} ms")

def now():
    return datetime.utcfromtimestamp(time.time() + mi_offset)

def stop_experiment():
    global experiment_finished

    time.sleep(TEST_DURATION)
    experiment_finished = True

    # =====================
    # THROUGHPUT
    # =====================

    throughput = msg_count / TEST_DURATION

    throughput_result = {
        "total_messages": msg_count,
        "duration": TEST_DURATION,
        "throughput_msgs_s": throughput,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(THROUGHPUT_FILE, "w") as f:
        json.dump(throughput_result, f, indent=4)

    # =====================
    # LATENCIA
    # =====================

    if latencies:

        latency_stats = {
            "count": len(latencies),
            "mean": float(np.mean(latencies)),
            "median": float(np.median(latencies)),
            "min": float(np.min(latencies)),
            "max": float(np.max(latencies)),
            "std": float(np.std(latencies)) if len(latencies) > 1 else 0.0,
            "p95": float(np.percentile(latencies, 95)),
            "p99": float(np.percentile(latencies, 99))
        }

        with open(LATENCY_STATS_FILE, "w") as f:
            json.dump(latency_stats, f, indent=4)

    print("\n==============================")
    print("EXPERIMENTO FINALIZADO")
    print(f"Mensajes: {msg_count}")
    print(f"Throughput: {throughput:.2f} msgs/s")

    if latencies:
        print(f"Latencia media: {np.mean(latencies)*1000:.2f} ms")

    os._exit(0)

# =========================
# ENDPOINT
# =========================
@app.route("/notify", methods=["POST"])
def notify():
    global msg_count, warmup_count, warmup_done, start_time, experiment_finished

    if experiment_finished:
        return "", 204

    data = request.json

    try:
        entity = data["data"][0]

        # =========================
        # WARMUP
        # =========================
        if not warmup_done:
            warmup_count += 1

            if warmup_count == 1:
                print("WARMUP iniciado...")

            if warmup_count >= WARMUP_SAMPLES:
                warmup_done = True
                msg_count = 0


                print("WARMUP completado. Iniciando medición...")

                threading.Thread(
                    target=stop_experiment,
                    daemon=True
                ).start()

            return "", 204


        msg_count += 1
        received_at = datetime.utcfromtimestamp(time.time() + mi_offset)

        date_observed = entity.get("dateObserved", {}).get("value")

        if date_observed:

            observed_at = datetime.fromisoformat(
                date_observed.replace("Z", "")
            )

            latency = (
                received_at - observed_at
            ).total_seconds()

            latencies.append(latency)

            record = {
                "entity": entity["id"],
                "dateObserved": observed_at.isoformat() + "Z",
                "receivedAt": received_at.isoformat() + "Z",
                "latency": latency
            }

            with open(LATENCY_FILE, "a") as f:
                json.dump(record, f)
                f.write("\n")

    except Exception as e:
        print("Error:", e)

    return "", 204
# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    esperar_inicio()
    app.run(host="0.0.0.0", port=5001)
