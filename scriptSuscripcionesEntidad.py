import requests

BROKER = "http://172.31.232.59:1026/ngsi-ld/v1/subscriptions"

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

def create_subscription(entity_id):
    sub = {
        "@context": CONTEXT,
        "type": "Subscription",
        "entities": [{
            "id": entity_id,
            "type": "DeviceMeasurement"
        }],
        "notification": {
            "endpoint": {
                "uri": "http://172.31.232.59:5001/notify",
                "accept": "application/json"
            }
        }
    }

    res = requests.post(BROKER, headers=HEADERS, json=sub)

    print(f"{entity_id}: {res.status_code}")
    if res.status_code != 201:
        print(res.text)

# =========================
# CREAR TODAS
# =========================

sensors = [
    "Camera",
    "GNSS",
    "IMU",
    "LiDAR",
    "Radar"
]

for sensor in sensors:
    for i in range(0, 51):
        entity_id = f"urn:ngsi-ld:DeviceMeasurement{sensor}:{i:03d}"
        create_subscription(entity_id)
