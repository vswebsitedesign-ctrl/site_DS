#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: bash restore.sh snapshots/SNAPSHOT_DIR"
  exit 1
fi
SNAPSHOT_DIR="$1"
cp "$SNAPSHOT_DIR/Master_Report_clean.json" /home/chubert/omni-builder/sites/site_DS/
cp "$SNAPSHOT_DIR/pages.json" /home/chubert/omni-builder/sites/site_DS/data/
cp "$SNAPSHOT_DIR/base.html" /home/chubert/omni-builder/sites/site_DS/theme/
cp "$SNAPSHOT_DIR/build.py" /home/chubert/omni-builder/sites/site_DS/
echo "✅ Restored from: $SNAPSHOT_DIR"
