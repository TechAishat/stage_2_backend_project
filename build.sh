#!/usr/bin/env bash
# Exit on error
set -o errexit
set -o pipefail
set -o nounset

echo "=== Starting build process ==="

# Set Python to output in unbuffered mode
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (only in Linux environment)
if command -v apt-get &> /dev/null; then
    echo "[1/6] Updating package lists..."
    apt-get update -qq
    
    echo "[2/6] Installing system dependencies..."
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*
fi

# Upgrade pip with retry logic
for i in {1..3}; do
    echo "[3/6] Upgrading pip (attempt $i/3)..."
    if python -m pip install --upgrade pip; then
        break
    elif [ $i -eq 3 ]; then
        echo "Failed to upgrade pip after 3 attempts"
        exit 1
    fi
    sleep 5
done

# Install Python dependencies with retry logic
echo "[4/6] Installing Python dependencies..."
for i in {1..3}; do
    if pip install --no-cache-dir -r requirements.txt; then
        break
    elif [ $i -eq 3 ]; then
        echo "Failed to install dependencies after 3 attempts"
        exit 1
    fi
    echo "Retrying dependency installation..."
    sleep 5
done

# Set Django settings module
export DJANGO_SETTINGS_MODULE=config.settings

# Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "Warning: Static file collection failed"

# Apply database migrations
echo "[6/6] Applying database migrations..."
python manage.py migrate --noinput

# Create cache table
echo "Creating cache table..."
python manage.py createcachetable || echo "Warning: Cache table creation failed"

echo "=== Build completed successfully ==="
exit 0
