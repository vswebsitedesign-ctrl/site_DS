#!/bin/bash
LABEL=${1:-"snapshot"}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DIR="/home/chubert/omni-builder/sites/site_DS/snapshots/${TIMESTAMP}_${LABEL}"
mkdir -p "$SNAPSHOT_DIR"
cp /home/chubert/omni-builder/sites/site_DS/Master_Report.json "$SNAPSHOT_DIR/"
cp /home/chubert/omni-builder/sites/site_DS/data/pages.json "$SNAPSHOT_DIR/"
cp /home/chubert/omni-builder/sites/site_DS/theme/base.html "$SNAPSHOT_DIR/"
cp /home/chubert/omni-builder/sites/site_DS/build.py "$SNAPSHOT_DIR/"
echo "✅ Snapshot saved: $SNAPSHOT_DIR"
