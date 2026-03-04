# Company Financial Health Scanner

**Programming for Economists II - Final Project**
**IE University - Bachelor in Economics**

## What It Does

This program reads company financial data from a text file, calculates key financial ratios, assigns health grades (A through F), and generates reports. It works like a simplified credit rating agency.

## Features

1. Leaderboard - Rank all companies by financial health score
2. Company Scanner - Deep-dive into one company ratios and risk alerts
3. Head-to-Head - Compare two companies side by side
4. Sector Analysis - Average health scores grouped by industry
5. Add Company - Interactively enter new company data with input validation
6. Save Report - Export a full report to a text file

## How to Run

1. Make sure companies.txt is in the same folder as the script
2. Run: python company_health_scanner.py
3. Follow the interactive menu (options 1-7)

## Financial Ratios Calculated

- Profit Margin (%) = (Revenue - Costs) / Revenue x 100
- Debt-to-Revenue = Total Debt / Annual Revenue
- Cash Runway (months) = (Cash / Costs) x 12
- Revenue per Employee = Revenue / Number of Employees
- Cost Efficiency (%) = Costs / Revenue x 100

## Grading System

- A (80+): Excellent financial health
- B (65-79): Good with minor concerns
- C (45-64): Fair with some risk areas
- D (25-44): Poor with significant risks
- F (below 25): Critical with multiple red flags

## Python Concepts Used

- Dictionaries (nested): storing company data and ratios
- Tuples: returning grade information (grade, score, alerts)
- Lists: storing rankings and risk alerts
- Files: reading data and writing reports
- Functions: 12 functions, each with docstrings
- Loops: for loops and while loop for menu
- Conditionals: if/elif/else for grading logic
- Try/Except: file error handling and input validation
- Strings: .strip(), .split(), concatenation, slicing

## Team Members

[Add your names here]
