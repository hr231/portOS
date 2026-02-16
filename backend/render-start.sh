#!/bin/bash
# Render start command for the FastAPI backend
# This script is called by Render's free web service

cd "$(dirname "$0")/.."
exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
