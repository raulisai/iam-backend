# Test del endpoint PATCH /api/stats/snapshots/update-latest
# Actualiza el snapshot más reciente con datos de salud procesados

$TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmEwMTI3NzctZmRhZi00ZWUxLWI0MWItYjU5ZjQ4Mzc0ZjU5IiwiZW1haWwiOiJkakB4eC5jb20iLCJuYW1lIjoiRGpva2VyIE0iLCJleHAiOjE3NjA3MTg1ODcsImlhdCI6MTc2MDYzMjE4N30.UonZrnr_sZjrdCO5CtTsoat0vCFDkP9cMud06GI5xEA"

Write-Host "=================================================="
Write-Host "Test 1: Datos reales del móvil (DailySummary)"
Write-Host "=================================================="
Write-Host ""
Write-Host "Datos enviados:"
Write-Host "- steps: 94"
Write-Host "- calories: 0.0 (se calculará automáticamente)"
Write-Host "- heart_rate: 67.25"
Write-Host "- sleep: 25200000 ms (7 horas)"
Write-Host ""

$body1 = @{
    snapshot_at = "2025-10-16T16:33:36.947130Z"
    energy = $null
    stamina = $null
    strength = $null
    flexibility = $null
    attention = $null
    score_body = $null
    score_mind = $null
    model_version = "v1.0"
    calories_burned = "0.0"
    steps_daily = "94"
    heart_rate = "67.25"
    sleep_score = "25200000"
    inputs = $null
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/stats/snapshots/update-latest" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body1

Write-Host ""
Write-Host "Resultados esperados:"
Write-Host "✅ calories_burned: '3.76' (calculado: 94 × 0.04)"
Write-Host "✅ steps_daily: '94'"
Write-Host "✅ heart_rate: '67.25'"
Write-Host "✅ sleep_score: '7.0 | bueno' (7 horas = óptimo)"
Write-Host ""

Write-Host "=================================================="
Write-Host "Test 2: Sin heart_rate (debe usar el anterior)"
Write-Host "=================================================="
Write-Host ""

$body2 = @{
    snapshot_at = "2025-10-16T16:40:00.000Z"
    model_version = "v1.0"
    calories_burned = "0.0"
    steps_daily = "150"
    heart_rate = $null
    sleep_score = "21600000"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/stats/snapshots/update-latest" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body2

Write-Host ""
Write-Host "Resultados esperados:"
Write-Host "✅ calories_burned: '6.0' (150 × 0.04)"
Write-Host "✅ steps_daily: '150'"
Write-Host "✅ heart_rate: '67.25' (mantiene el valor anterior)"
Write-Host "✅ sleep_score: '6.0 | estable' (6 horas = aceptable)"
Write-Host ""

Write-Host "=================================================="
Write-Host "Test 3: Mal sueño (<6 horas)"
Write-Host "=================================================="
Write-Host ""

$body3 = @{
    model_version = "v1.0"
    calories_burned = "0.0"
    steps_daily = "5000"
    heart_rate = "72"
    sleep_score = "18000000"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/stats/snapshots/update-latest" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body3

Write-Host ""
Write-Host "Resultados esperados:"
Write-Host "✅ calories_burned: '200.0' (5000 × 0.04)"
Write-Host "✅ steps_daily: '5000'"
Write-Host "✅ heart_rate: '72.0'"
Write-Host "✅ sleep_score: '5.0 | malo' (5 horas = insuficiente)"
Write-Host ""

Write-Host "=================================================="
Write-Host "Test 4: Buen sueño (8 horas)"
Write-Host "=================================================="
Write-Host ""

$body4 = @{
    model_version = "v1.0"
    calories_burned = "0.0"
    steps_daily = "10000"
    heart_rate = "65"
    sleep_score = "28800000"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/stats/snapshots/update-latest" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body4

Write-Host ""
Write-Host "Resultados esperados:"
Write-Host "✅ calories_burned: '400.0' (10000 × 0.04)"
Write-Host "✅ steps_daily: '10000'"
Write-Host "✅ heart_rate: '65.0'"
Write-Host "✅ sleep_score: '8.0 | bueno' (8 horas = óptimo)"
Write-Host ""
