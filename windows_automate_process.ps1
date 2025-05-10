# === CONFIGURATION ===
$repoUrl = "https://github.com/MdSamsuzzohaShayon/sponsor-reach.git"
$projectName = "sponsor-reach"
$venvName = ".venv"

# === Clone the GitHub repository ===
Write-Host "Cloning repository..."
git clone $repoUrl $projectName

# === Navigate into the project directory ===
Set-Location $projectName

# === Create virtual environment ===
Write-Host "Creating virtual environment..."
python -m venv $venvName

# === Activate virtual environment ===
Write-Host "Activating virtual environment..."
& ".\$venvName\Scripts\Activate.ps1"

# === Install dependencies if requirements.txt exists ===
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
} else {
    Write-Host "No requirements.txt found."
}

# === Run the Python project (assuming main.py is the entry point) ===
Write-Host "Running the project..."
python main.py

# === End message ===
Write-Host "`n✔️  Project setup and execution complete."
