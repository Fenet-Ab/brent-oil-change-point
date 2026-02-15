# Troubleshooting Guide

## Common Issues and Solutions

### 1. `python` command not found

**Error:**
```
Command 'python' not found, did you mean:
  command 'python3' from deb python3
```

**Solution:**
On Linux systems, use `python3` instead of `python`:

```bash
# Instead of: python app.py
python3 app.py

# Or use the helper script:
cd dashboard/backend
./run.sh
```

### 2. Matplotlib Style Error

**Error:**
```
AttributeError: 'RcParams' object has no attribute '_get'
```

**Solution:**
This is a matplotlib version compatibility issue. The notebook has been updated to handle this automatically by trying different style names. If you still encounter issues:

```bash
# Update matplotlib
pip3 install --upgrade matplotlib

# Or install specific version
pip3 install matplotlib==3.7.0
```

### 3. Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'statsmodels'
```

**Solution:**
Install all required dependencies:

```bash
pip3 install -r requirements.txt
```

If you encounter permission errors:
```bash
pip3 install --user -r requirements.txt
```

### 4. Flask CORS Error

**Error:**
```
Access to fetch at 'http://localhost:5000/prices' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
The Flask backend already has CORS enabled. Make sure:
1. Flask-CORS is installed: `pip3 install flask-cors`
2. The backend is running on port 5000
3. The frontend is running on port 3000

### 5. Node/React Issues

**Error:**
```
npm: command not found
```

**Solution:**
Install Node.js and npm:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install nodejs npm

# Or use nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

### 6. Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
Find and kill the process using the port:
```bash
# For port 5000 (Flask)
lsof -ti:5000 | xargs kill -9

# For port 3000 (React)
lsof -ti:3000 | xargs kill -9
```

### 7. Path Issues in Notebooks

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../data/raw/brent_oil_prices.csv'
```

**Solution:**
Make sure you're running the notebooks from the `notebooks/` directory, or update the paths in the notebook to use absolute paths.

### 8. PyMC Installation Issues

**Error:**
```
ERROR: Could not build wheels for pymc
```

**Solution:**
PyMC requires some system dependencies. On Ubuntu/Debian:
```bash
sudo apt-get install build-essential python3-dev
pip3 install pymc
```

### 9. Jupyter Notebook Not Starting

**Error:**
```
jupyter: command not found
```

**Solution:**
Install Jupyter:
```bash
pip3 install jupyter
# Or
pip3 install --user jupyter

# Add to PATH if needed
export PATH=$PATH:~/.local/bin
```

### 10. Date Format Issues

**Error:**
```
ValueError: time data '20-May-87' does not match format '%Y-%m-%d'
```

**Solution:**
The data loader handles this automatically. If you see this error, make sure you're using the `load_brent_data()` function from `src/data_loader.py`.

## Quick Fixes

### Check Python Version
```bash
python3 --version
# Should be Python 3.8 or higher
```

### Check Installed Packages
```bash
pip3 list | grep -E "(pandas|numpy|matplotlib|pymc|flask)"
```

### Verify Data Files
```bash
ls -la data/raw/brent_oil_prices.csv
ls -la data/processed/key_events.csv
```

### Test Flask Backend
```bash
cd dashboard/backend
python3 app.py
# Then in another terminal:
curl http://localhost:5000/
```

### Test React Frontend
```bash
cd dashboard/frontend
npm install
npm run dev
# Then open http://localhost:3000 in browser
```

## Getting Help

If you encounter other issues:
1. Check the error message carefully
2. Verify all dependencies are installed
3. Make sure you're using Python 3.8+
4. Check that data files exist in the correct locations
5. Review the README.md for setup instructions

