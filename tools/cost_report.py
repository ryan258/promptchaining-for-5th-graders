#!/usr/bin/env python3
"""
💰 Cost Report Tool

Analyzes log files to calculate and display API costs.

Usage:
    python tools/cost_report.py
    python tools/cost_report.py --days 7
    python tools/cost_report.py --verbose
"""

import sys
import os
import argparse
import glob
import re
from datetime import datetime, timedelta

# Setup project root
try:
    from tools.tool_utils import setup_project_root
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from tools.tool_utils import setup_project_root

project_root = setup_project_root(__file__, depth=1)

def parse_cost_from_log(log_path):
    """Extract cost from a markdown log file"""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for cost pattern: "**Total Cost**: $0.000123"
        match = re.search(r'\*\*Total Cost\*\*: \$([\d\.]+)', content)
        if match:
            return float(match.group(1))
        return 0.0
    except Exception:
        return 0.0

def generate_cost_report(days=30, verbose=False):
    """Generate cost report for the last N days"""
    logs_dir = os.path.join(project_root, 'logs')
    
    if not os.path.exists(logs_dir):
        print(f"No logs directory found at {logs_dir}")
        return

    print(f"💰 Cost Report (Last {days} days)")
    print("=" * 60)

    cutoff_date = datetime.now() - timedelta(days=days)
    total_cost = 0.0
    tool_costs = {}
    
    # Find all markdown logs
    log_files = glob.glob(os.path.join(logs_dir, "*.md"))
    
    for log_file in log_files:
        # Check date from filename: YYYY-MM-DD_HH-MM-SS_toolname.md
        filename = os.path.basename(log_file)
        try:
            date_str = filename[:10]
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            if file_date < cutoff_date:
                continue
                
            # Extract tool name
            # Format: YYYY-MM-DD_HH-MM-SS_toolname.md
            parts = filename.split('_', 2)
            if len(parts) > 2:
                tool_name = parts[2].replace('.md', '')
            else:
                tool_name = "unknown"
                
            cost = parse_cost_from_log(log_file)
            
            if cost > 0:
                total_cost += cost
                tool_costs[tool_name] = tool_costs.get(tool_name, 0.0) + cost
                
                if verbose:
                    print(f"  {date_str} {tool_name:<20} ${cost:.6f}")
                    
        except (ValueError, IndexError):
            continue

    print("-" * 60)
    
    # Sort by cost descending
    sorted_tools = sorted(tool_costs.items(), key=lambda x: x[1], reverse=True)
    
    for tool, cost in sorted_tools:
        print(f"{tool:<30} ${cost:.6f}")
        
    print("=" * 60)
    print(f"TOTAL SPEND:{'':<19} ${total_cost:.6f}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Calculate API costs from logs")
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    parser.add_argument('--verbose', action='store_true', help='Show individual log costs')
    
    args = parser.parse_args()
    
    generate_cost_report(args.days, args.verbose)

if __name__ == "__main__":
    main()
