#!/bin/bash

# Test del endpoint PATCH /api/stats/snapshots/update-latest
# Actualiza el snapshot más reciente con datos de salud procesados

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmEwMTI3NzctZmRhZi00ZWUxLWI0MWItYjU5ZjQ4Mzc0ZjU5IiwiZW1haWwiOiJkakB4eC5jb20iLCJuYW1lIjoiRGpva2VyIE0iLCJleHAiOjE3NjA3MTg1ODcsImlhdCI6MTc2MDYzMjE4N30.UonZrnr_sZjrdCO5CtTsoat0vCFDkP9cMud06GI5xEA"

echo "=================================================="
echo "Test 1: Datos reales del móvil (DailySummary)"
echo "=================================================="
echo ""
echo "Datos enviados:"
echo "- steps: 94"
echo "- calories: 0.0 (se calculará automáticamente)"
echo "- heart_rate: 67.25"
echo "- sleep: 25200000 ms (7 horas)"
echo ""

curl -X POST "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T16:33:36.947130Z",
    "energy": null,
    "stamina": null,
    "strength": null,
    "flexibility": null,
    "attention": null,
    "score_body": null,
    "score_mind": null,
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "94",
    "heart_rate": "67.25",
    "sleep_score": "25200000",
    "inputs": null
  }'

echo -e "\n\n"
echo "Resultados esperados:"
echo "✅ calories_burned: '3.76' (calculado: 94 × 0.04)"
echo "✅ steps_daily: '94'"
echo "✅ heart_rate: '67.25'"
echo "✅ sleep_score: '7.0 | bueno' (7 horas = óptimo)"
echo ""

echo "=================================================="
echo "Test 2: Sin heart_rate (debe usar el anterior)"
echo "=================================================="
echo ""

curl -X POST "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_at": "2025-10-16T16:40:00.000Z",
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "150",
    "heart_rate": null,
    "sleep_score": "21600000"
  }'

echo -e "\n\n"
echo "Resultados esperados:"
echo "✅ calories_burned: '6.0' (150 × 0.04)"
echo "✅ steps_daily: '150'"
echo "✅ heart_rate: '67.25' (mantiene el valor anterior)"
echo "✅ sleep_score: '6.0 | estable' (6 horas = aceptable)"
echo ""

echo "=================================================="
echo "Test 3: Mal sueño (<6 horas)"
echo "=================================================="
echo ""

curl -X POST "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "5000",
    "heart_rate": "72",
    "sleep_score": "18000000"
  }'

echo -e "\n\n"
echo "Resultados esperados:"
echo "✅ calories_burned: '200.0' (5000 × 0.04)"
echo "✅ steps_daily: '5000'"
echo "✅ heart_rate: '72.0'"
echo "✅ sleep_score: '5.0 | malo' (5 horas = insuficiente)"
echo ""

echo "=================================================="
echo "Test 4: Buen sueño (8 horas)"
echo "=================================================="
echo ""

curl -X POST "http://localhost:5000/api/stats/snapshots/update-latest" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_version": "v1.0",
    "calories_burned": "0.0",
    "steps_daily": "10000",
    "heart_rate": "65",
    "sleep_score": "28800000"
  }'

echo -e "\n\n"
echo "Resultados esperados:"
echo "✅ calories_burned: '400.0' (10000 × 0.04)"
echo "✅ steps_daily: '10000'"
echo "✅ heart_rate: '65.0'"
echo "✅ sleep_score: '8.0 | bueno' (8 horas = óptimo)"
echo ""
