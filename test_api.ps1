# Script de Prueba - IA Tutora
# Ejecuta: .\test_api.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  PRUEBA DE API - IA TUTORA" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:5000"
$userId = "test-user-$(Get-Date -Format 'yyyyMMddHHmmss')"

Write-Host "Usuario de prueba: $userId" -ForegroundColor Yellow
Write-Host ""

# Test 1: Iniciar clase
Write-Host "1. Iniciando clase..." -ForegroundColor Green
try {
    $body1 = @{
        user_id = $userId
    } | ConvertTo-Json

    $response1 = Invoke-WebRequest -Uri "$baseUrl/api/ia/start" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body1 `
        -ErrorAction Stop

    $result1 = $response1.Content | ConvertFrom-Json
    
    Write-Host "✅ Clase iniciada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Respuesta del tutor:" -ForegroundColor Cyan
    Write-Host $result1.response -ForegroundColor White
    Write-Host ""
    Write-Host "================================" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "❌ Error al iniciar clase:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "¿Está el servidor corriendo? Ejecuta: python run.py" -ForegroundColor Yellow
    exit
}

# Esperar un momento
Start-Sleep -Seconds 2

# Test 2: Hacer una pregunta
Write-Host "2. Haciendo pregunta al tutor..." -ForegroundColor Green
try {
    $body2 = @{
        user_id = $userId
        message = "¿Qué diferencia hay entre IaaS, PaaS y SaaS?"
    } | ConvertTo-Json

    $response2 = Invoke-WebRequest -Uri "$baseUrl/api/ia/ask" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body2 `
        -ErrorAction Stop

    $result2 = $response2.Content | ConvertFrom-Json
    
    Write-Host "✅ Pregunta respondida exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Respuesta del tutor:" -ForegroundColor Cyan
    Write-Host $result2.response -ForegroundColor White
    Write-Host ""
    Write-Host "================================" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "❌ Error al hacer pregunta:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit
}

# Test 3: Otra pregunta
Write-Host "3. Haciendo segunda pregunta..." -ForegroundColor Green
try {
    $body3 = @{
        user_id = $userId
        message = "Dame un ejemplo práctico de cada modelo"
    } | ConvertTo-Json

    $response3 = Invoke-WebRequest -Uri "$baseUrl/api/ia/ask" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body3 `
        -ErrorAction Stop

    $result3 = $response3.Content | ConvertFrom-Json
    
    Write-Host "✅ Segunda pregunta respondida!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Respuesta del tutor:" -ForegroundColor Cyan
    Write-Host $result3.response -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host "❌ Error:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verifica MongoDB Atlas:" -ForegroundColor Yellow
Write-Host "  1. Ve a https://cloud.mongodb.com" -ForegroundColor White
Write-Host "  2. Database -> Browse Collections" -ForegroundColor White
Write-Host "  3. Busca el usuario: $userId" -ForegroundColor White
Write-Host ""
