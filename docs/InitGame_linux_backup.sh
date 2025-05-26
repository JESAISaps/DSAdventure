#!/bin/bash

VENV_DIR="venv"

sudo apt install python3.12-venv

# Step 1: Create virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Step 2: Activate venv and install dependencies
echo "Installing dependencies..."
source $VENV_DIR/bin/activate
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi
deactivate

# Step 3: Create launcher script
echo "Creating launcher script..."
cat << EOF > run_main.sh
#!/bin/bash
source $VENV_DIR/bin/activate
sudo venv/bin/python3 sources/main.py
deactivate
EOF
chmod +x run_main.sh

# Step 4: Delete this setup script
echo "Cleaning up setup script..."
rm -- "InitGame_linux.sh"
