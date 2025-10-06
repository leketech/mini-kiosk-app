#!/bin/bash
# Check if kiosk app is responding
response=$(curl -s http://localhost:5000/health)

if echo "$response" | grep -q '"status":"ok"'; then
    echo "✅ Kiosk is healthy"
    exit 0
else
    echo "❌ Kiosk is DOWN"
    exit 1
fi
