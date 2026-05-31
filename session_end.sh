#!/bin/bash
cd /home/chubert/omni-builder/sites/site_DS
git add -A
git commit -m "session: $(date '+%Y-%m-%d %H:%M') — $1"
git push
echo "PUSHED TO GITHUB"
