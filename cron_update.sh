#!/bin/bash
set -e

echo "Running weekly stats update..."

# 1. Run update script
python update_data.py

# 2. Add JSON file to git
git add data/stats.json

# 3. Commit (ignore if no changes)
git commit -m "Weekly stats update" || true

# 4. Push back to GitHub
git push