# === CONFIGURATION ===
$projectName = "sponsor-reach"
$repoUrl = "https://github.com/MdSamsuzzohaShayon/$projectName.git"
$venvName = ".venv"

function Show-Error($message) {
    Write-Host "`n❌ ERROR: $message" -ForegroundColor Red
    exit 1
}

# === Clone the GitHub repository ===
if (-not (Test-Path $projectName)) {
    Write-Host "📦 Cloning repository..."
    git clone $repoUrl $projectName
    if ($LASTEXITCODE -ne 0) { Show-Error "Failed to clone the repository." }
} else {
    Write-Host "📁 Repository folder '$projectName' already exists. Skipping clone."
}

# === Navigate into the project directory ===
$currentDir = Get-Location
if ((Split-Path $currentDir -Leaf) -ne $projectName) {
    Write-Host "📂 Entering project directory..."
    Set-Location $projectName
}

# === Create virtual environment ===
if (-not (Test-Path $venvName)) {
    Write-Host "🔧 Creating virtual environment..."
    python -m venv $venvName
    if ($LASTEXITCODE -ne 0) { Show-Error "Failed to create virtual environment." }
} else {
    Write-Host "✅ Virtual environment already exists. Skipping creation."
}

# === Activate virtual environment ===
if (-not (Get-Command "python" | Out-String).Contains("$venvName")) {
    Write-Host "⚡ Activating virtual environment..."
    try {
        & ".\$venvName\Scripts\Activate.ps1"
    } catch {
        Show-Error "Failed to activate the virtual environment."
    }
} else {
    Write-Host "✅ Virtual environment is already active."
}

# === Install dependencies if requirements.txt exists ===
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Show-Error "Failed to install dependencies." }
} else {
    Write-Host "⚠️  No requirements.txt found. Skipping dependency installation."
}

# === Check for .env file ===
if (-not (Test-Path ".env")) {
    Show-Error "'.env' file is missing. Please create it before running the project."
}

# === Run the Python project (assuming main.py is the entry point) ===
if (Test-Path "main.py") {
    Write-Host "🚀 Running the project..."
    python main.py
    if ($LASTEXITCODE -ne 0) { Show-Error "Project execution failed." }
} else {
    Show-Error "'main.py' not found."
}

# === End message ===
Write-Host "`n✔️  Project setup and execution complete." -ForegroundColor Green

