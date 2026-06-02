#!/bin/bash
set -e

echo "Starting Theatres Dashboard..."

# Source environment if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run health checks and validations
echo "Validating configuration..."
python -c "
from config import Config
Config.setup_logging()
Config.validate()
print('✓ Configuration validated')
"

if [ $? -ne 0 ]; then
    echo "❌ Configuration validation failed"
    exit 1
fi

echo "✓ All checks passed"
echo "Starting Streamlit application..."

# Start Streamlit
exec streamlit run app.py
