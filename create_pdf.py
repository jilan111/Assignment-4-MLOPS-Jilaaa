#!/usr/bin/env python3
"""
Simple text-based report - no external dependencies needed
This will be converted to PDF via alternative method
"""
import os

os.chdir("/Users/jilan/Documents/Assignmnet 3 MLOps")

# For now, just note that the markdown file serves as the detailed bug report
print("✅ Bug report has been created in Markdown format")
print("📄 Location: GitHub_Actions_Bug_Report.md")
print("\nTo convert to PDF on macOS:")
print("  1. Open the .md file in any browser")
print("  2. Or use: open -a 'Google Chrome' GitHub_Actions_Bug_Report.md && Cmd+P to save as PDF")
print("  3. Or use: pandoc GitHub_Actions_Bug_Report.md -o GitHub_Actions_Bug_Report.pdf")
print("\n✅ The workflow file has been created at: .github/workflows/ml-pipeline.yml")
