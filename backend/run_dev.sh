#!/bin/bash
# Development server startup script
cd "$(dirname "$0")"
conda activate base
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=dev-secret-key-change-in-production
python app.py





