#  Agricultural Land Production Planning using Artificial Intelligence

> **Course:** Introduction to Artificial Intelligence  
> **Institution:** Higher National School of Artificial Intelligence (ENSIA)  
> **Project Date:** June 2024

---

##  Overview

Agricultural Land Production Planning is an Artificial Intelligence project designed to optimize crop distribution across Algeria's 48 wilayas. The objective is to improve agricultural productivity and achieve self-sufficiency by intelligently allocating agricultural land according to weather conditions, production capacity, and crop consumption.

The project models the problem as a state-space search problem where each state represents the distribution of crops across the country. Different AI search algorithms are then used to find better agricultural planning strategies.

---

## Objectives

- Optimize agricultural land allocation.
- Increase national crop production.
- Improve food self-sufficiency.
- Consider weather compatibility for each crop.
- Compare multiple Artificial Intelligence search algorithms.
- Evaluate execution time and memory consumption.

---

## Artificial Intelligence Techniques

The project implements several search strategies:

- Depth-First Search (DFS)
- Depth-Limited Search (DLS)
- Iterative Deepening Search (IDS)
- Hill Climbing
- Stochastic Hill Climbing
- Iterative Deepening A* (IDA*)

---

## Dataset

The project relies on several JSON datasets:

### Weather Data
- `wilayasconditions.json`
- `cropsconditions.json`

### Crop Data
Individual JSON files for each crop containing:
- Land size
- Production
- Crop information

Examples include:
- Wheat
- Potato
- Tomato
- Corn
- Olives
- Garlic
- Onion
- Orange
- Apple
- Dates
- and others.

### Additional Data

- Consumption data
- Crop prices
- Wilaya land sizes

---

##  State Representation

Each state represents:

- Algeria divided into 48 wilayas.
- Every wilaya contains multiple crops.
- Each crop has:
  - Production
  - Land size
  - Price
  - Weather requirements

---

##  Available Actions

Three actions are possible during the search:

- Increase crop land size
- Decrease crop land size
- Swap the same crop between two wilayas

These actions generate successor states explored by the search algorithms.

---

## Heuristic

A weather-based heuristic evaluates how well a crop matches the climate of a wilaya.

It compares:

- Temperature
- Precipitation

for selected months:

- February
- June
- August
- December

The heuristic minimizes weather mismatches between crops and regions.

---

## Performance Evaluation

The project compares algorithms using:

- Execution time
- Memory usage
- Search depth
- Solution cost

Results showed that:

- Hill Climbing and Stochastic Hill Climbing are significantly faster.
- DFS and DLS require much more memory and computation time.
- IDA* provides a heuristic-guided search while balancing memory efficiency.

---

## Visualization

The project includes map visualization using:

- Folium
- HTML
- CSS
- JavaScript

Attempts were also made using:

- GeoPandas
- NetworkX

---

## Team Members

- **Ghorab Meriem** 
- **Messahel Hibet Allah**
- **Menadi Mohamed Elamine**

---

## References

The project uses data and concepts from:

- Artificial Intelligence: A Modern Approach (Russell & Norvig, 4th Edition)
- Climate Data
- Weatherbit API
- WeatherAPI
- OpenWeatherMap
- Meteoblue
- Algerian Ministry of Commerce
- Algerian Ministry of Agriculture
- Python Folium Documentation

---

## Future Improvements

- Integrate real-time weather APIs.
- Use satellite imagery for crop monitoring.
- Replace manual data retrieval with a Vector Database (RAG).
- Improve visualization using GIS tools.
- Develop a complete web dashboard.
- Optimize search algorithms for large state spaces.

