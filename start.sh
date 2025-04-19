#!/bin/bash

#  Ensure Poetry is installed
if ! command -v poetry &> /dev/null
then
  echo "Poetry is not installed. Please install it first."
  exit 1
fi

#  Ensure SuperCollider is installed
if ! command -v sclang &> /dev/null
then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # Continue if MacOS
    echo "SuperCollider install not detected."
  else
    echo "SuperCollider is not installed. Please install it first."
    exit 1
  fi
fi

#  Ensure Python is installed
if ! command -v python &> /dev/null
then
  echo "Python is not installed. Please install it first."
  exit 1
fi

#  Ensure Node.js is installed
if ! command -v node &> /dev/null
then
  echo "Node.js is not installed. Please install it first."
  exit 1
fi

echo "Starting services..."
cd app

# Use or install env for API
cd python
poetry env use 3.9.0
poetry install
# Start API
poetry run python api.py &

# Use or install env for SuperCollider
cd ../sc
poetry env use 3.10
poetry install
# Start SuperCollider
sclang sampler.scd &

# Start loader
python loader.py &

# Start web server
cd ../web
npm install
npm run dev &

echo "All services started."
