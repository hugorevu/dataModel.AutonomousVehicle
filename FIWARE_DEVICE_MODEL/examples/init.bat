@echo off

echo Creating AutonomousVehicle...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @autonomousVehicle.json

echo Creating DeviceModel...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelCamera.json

echo Creating Device...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceCamera.json

echo Creating Measurement...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementCamera.json

echo Done.
pause