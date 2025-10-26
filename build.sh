#!/usr/bin/env bash
# Exit on error
set -o errexit
set -o pipefail
set -o nounset

echo "=== Starting build process ==="

# Install system dependencies (only in Linux environment)
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies..."
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
fi

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Set environment variables
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=config.settings

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create cache table
echo "Creating cache table..."
python manage.py createcachetable

echo "=== Build completed successfully ==="
