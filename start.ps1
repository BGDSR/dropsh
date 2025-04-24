# start.ps1
Start-Process -FilePath ".\loclx.exe" -ArgumentList "tunnel http --to localhost:5000"
Start-Process -FilePath "python" -ArgumentList "app.py"