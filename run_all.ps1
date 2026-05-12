Write-Host "`n=== Step 1: Generate Synthetic Data ===" -ForegroundColor Cyan
& .\venv\Scripts\python.exe src/generate_data.py
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n=== Step 2: Run ETL Pipeline ===" -ForegroundColor Cyan
& .\venv\Scripts\python.exe src/etl.py
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n=== Step 3: Run Tests ===" -ForegroundColor Cyan
& .\venv\Scripts\python.exe -m pytest -q
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n=== All steps passed! ===" -ForegroundColor Green
