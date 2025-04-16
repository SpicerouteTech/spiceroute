#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

echo -e "${BLUE}Setting up Auth Service...${NC}\n"

# Check if Python 3.7+ is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -e .[dev]

# Make verify_setup.py executable
chmod +x verify_setup.py

# Run verification script
echo -e "${BLUE}Running verification...${NC}"
python verify_setup.py

# Check if verification was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Setup completed successfully!${NC}"
    echo -e "\nTo start the development server:"
    echo -e "1. Activate the virtual environment: ${BLUE}source venv/bin/activate${NC}"
    echo -e "2. Start the server: ${BLUE}uvicorn src.main:app --reload${NC}"
else
    echo -e "\n${RED}Setup failed. Please check the errors above.${NC}"
    exit 1
fi 