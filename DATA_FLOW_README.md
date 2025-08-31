# Duolingo Data Flow Documentation

## Overview
This document explains how the Duolingo data fetching and synchronization system works in this project.

## Data Fetching Process

### Full History is Pulled Every Time 📊

**Key API Call:**
```python
summary_url = f"{self.base_url}/2017-06-30/users/{user_response_data['id']}/xp_summaries?startDate=1970-01-01"
```

**What this means:**
- **Every single day**, the script fetches your **complete Duolingo history** from January 1, 1970 (Unix epoch) to today
- It's **NOT** just fetching new data - it's pulling your entire XP summary history every time
- The `startDate=1970-01-01` parameter ensures it gets everything from the beginning

### How the Data is Processed 🔄

1. **Full API Call**: Every day at 20:15 GMT+7 (13:15 UTC), the GitHub Action runs and calls the Duolingo API to get your complete history

2. **Smart Synchronization**: The system then uses the `sync_database_with_summaries()` function to:
   - Compare the new full dataset with your existing local database
   - Only update entries that have actually changed
   - Fill in any gaps in your historical data
   - Maintain streak calculations correctly

3. **Efficient Storage**: Even though the full history is fetched, only the changes are actually committed to your repository

### Why This Approach? 🤔

This "fetch everything" approach is used because:

1. **Data Integrity**: Ensures no data is ever lost or missed
2. **Streak Accuracy**: Duolingo's streak calculations can be complex and change retroactively
3. **Historical Corrections**: Duolingo sometimes updates past data (XP corrections, streak adjustments)
4. **Simplicity**: Easier to implement than complex incremental fetching logic

## Automation Schedule ⏰

The script runs automatically:
- **Daily at 20:15 GMT+7** (13:15 UTC) via GitHub Actions
- **Manual trigger** available if needed
- **Commits changes** to your repository with a timestamp
- **Deploys updated website** automatically

## Data Flow Summary 📈

```
Every Day:
1. GitHub Action triggers at 20:15 GMT+7
2. Script fetches COMPLETE Duolingo history (1970-01-01 to today)
3. Compares with existing local database
4. Updates only changed entries
5. Commits changes to repository
6. Deploys updated website
```

## Key Files

- **API Client**: `src/api.py` - Handles Duolingo API calls
- **Synchronizer**: `src/synchronizer.py` - Manages data merging and updates
- **Main Script**: `main.py` - Orchestrates the entire process
- **GitHub Action**: `.github/workflows/run.yml` - Automation configuration

## Data Storage

- **Raw Data**: `data/duolingo-progress.json` - Your complete Duolingo history
- **Statistics**: `data/statistics.json` - Script execution timestamps
- **Website**: `web/` - Static website files that display your data

## Important Notes

- The system fetches your **complete history every day** but only stores changes
- This ensures data completeness and accuracy
- Streak calculations are maintained correctly across all historical data
- The website is automatically updated with the latest data after each run

