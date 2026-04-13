Smart Data Model for Autonomous Vehicles based on CARLA Simulator.
Compliant with FIWARE NGSI-LD and inspired by the SOSA/SSN ontology.

📖 Overview

This repository provides an initial version of a Smart Data Model designed to represent autonomous vehicles, their onboard sensors, and the observations they generate.

The model focuses on capturing the core elements of an autonomous driving scenario, including:

The vehicle as a platform
Different types of sensors (e.g., RGB cameras, GNSS)
Observations produced by these sensors
The results derived from those observations

🧩 Data Model Structure

The model is organized around the following main entities:

-Platform: Represents the autonomous vehicle
-AutonomousVehicle: Specific autonomous vehicle instance
-Sensor: Generic abstraction of onboard sensors
-CameraRGB / GNSS: Specific sensor implementations
-Observation: Captures sensing events
-Result: Represents the output of observations

📂 Examples

This repository includes example NGSI-LD entities to illustrate how the data model can be used in practice.

You can find them in the examples/ folder.

Available examples include:

-CameraRGB.json: RGB camera entity with resolution and field of view
-GNSS.json: GNSS sensor entity
-Observation.json: Example of a sensor observation
-Result.json: Result associated with an observation
-AutonomousVehicle: Autonomous Vehicle entity

These examples can be used directly with FIWARE Context Brokers such as Stellio, Scorpio or Orion-LD.