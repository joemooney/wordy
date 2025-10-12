#!/bin/bash
# Start the GRE Vocabulary Quiz web application

echo "Starting GRE Vocabulary Quiz..."
echo "================================"
echo ""
echo "The quiz will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment and run the app
source venv/bin/activate
python3 quiz_app.py
