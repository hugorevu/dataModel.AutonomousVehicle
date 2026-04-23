@echo off

echo Creating AutonomousVehicle...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @autonomousVehicle.json

echo Creating Device...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceCamera.json

echo Creating DeviceModel...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelCamera.json

echo Creating Measurement...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementCamera.json

echo Creating Device for GNSS...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceGNSS.json

echo Creating DeviceModel for GNSS...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelGNSS.json

echo Creating Measurement for GNSS...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementGNSS.json

echo Done.
pause