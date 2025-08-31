# 🦉 Duolingo Activity Dashboard

An interactive dashboard to visualize your Duolingo learning progress over time. This project fetches data from unofficial Duolingo APIs and creates beautiful, interactive visualizations to track your language learning journey.

> **Note**: This repository is a fork and significant enhancement of [lauslim12/japanese-duolingo-visualizer](https://github.com/lauslim12/japanese-duolingo-visualizer). While the original focused on Japanese learning with static visualizations, this version provides a comprehensive, interactive dashboard supporting all languages with real-time data fetching and advanced analytics.

## 🌟 Features

### Enhanced from Original Repository
- **📊 Interactive Dashboard**: Beautiful web-based dashboard with multiple visualization types (enhanced from static charts)
- **📈 Progress Tracking**: Daily XP, cumulative progress, and streak analysis with advanced metrics
- **🗓️ Study Patterns**: Heatmap visualization of study consistency
- **🌍 Multi-Language Support**: Progress tracking for all languages (not just Japanese)
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔄 Real-time Updates**: Refresh data and see updated visualizations instantly
- **📋 Key Statistics**: Important metrics at a glance with detailed breakdowns
- **🎯 Sample Data Mode**: Demo mode with realistic sample data for testing
- **⚡ Easy Setup**: Simple command-line interface with multiple data source options
- **🔒 Privacy-First**: Local data processing with optional password-free data fetching

## 🚀 Quick Start

### Option 1: Easy Setup with Shell Script

```bash
# Make the script executable and run it
chmod +x start_dashboard.sh
./start_dashboard.sh
```

The script will guide you through the setup process with an interactive menu.

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Run with Sample Data (Recommended for Testing)

```bash
python main.py --username your_username --sample --dashboard
```

#### 3. Run with Real Data

```bash
# Using DuoJSON API (no password required - safer option)
python main.py --username your_duolingo_username --fetch --dashboard

# Using unofficial API (password required for more detailed data)
python main.py --username your_username --password your_password --fetch --dashboard
```

#### 4. View Dashboard

Open your browser and go to: [http://127.0.0.1:8050](http://127.0.0.1:8050)

## 📋 Available Commands

```bash
# Fetch data and run dashboard
python main.py --username USERNAME --fetch --dashboard

# Generate sample data and run dashboard
python main.py --username USERNAME --sample --dashboard

# Run dashboard with existing data
python main.py --dashboard

# Check data status
python main.py --status

# Get help
python main.py --help
```

## 📊 Dashboard Components

### Key Statistics Cards
- **Total XP**: Cumulative experience points earned
- **Current Streak**: Current consecutive days of study
- **Longest Streak**: Best streak achieved
- **Average Daily XP**: Mean XP earned per day
- **Study Frequency**: Percentage of days studied
- **Days Studied**: Total number of active study days

### Visualizations
1. **Daily XP Progress**: Bar chart showing daily XP with 7-day moving average
2. **Cumulative XP**: Line chart tracking total XP growth over time
3. **Study Consistency Heatmap**: Calendar-style heatmap showing study patterns
4. **Language Progress**: Comparison of XP across different languages

## 🔧 Technical Details

### Key Improvements from Original Repository

| Feature | Original Repository | This Enhanced Version |
|---------|-------------------|----------------------|
| **Visualization** | Static HTML/CSS/JS charts | Interactive Plotly/Dash dashboard |
| **Language Support** | Japanese only | All Duolingo languages |
| **Data Sources** | Single unofficial API | Multiple APIs (DuoJSON + unofficial) |
| **Setup** | GitHub Actions automation | Local interactive setup |
| **Data Processing** | Basic JSON storage | Advanced CSV + JSON processing |
| **User Interface** | Static website | Real-time interactive dashboard |
| **Privacy** | Required password | Optional password-free option |

### Data Sources

1. **DuoJSON API** (`https://duojson.com/USERNAME/profile.json`)
   - Public API, no authentication required
   - Provides basic profile information
   - Limited data availability but privacy-friendly

2. **Unofficial Duolingo API** (`duolingo-api` Python package)
   - Requires username and password
   - More comprehensive data including daily activity
   - May break if Duolingo changes their internal APIs

### Data Storage

- **Raw Data**: Stored as JSON in `data/raw_duolingo_data.json`
- **Processed Data**: CSV files for easy analysis
  - `data/daily_stats.csv`: Daily XP and streak information
  - `data/language_progress.csv`: Progress by language
  - `data/processed_duolingo_data.json`: Metadata and statistics

### Architecture

```
duolingo_data_fetcher.py    # Enhanced data fetching from multiple APIs
data_storage.py             # Advanced data processing and storage
dashboard.py               # Interactive Plotly/Dash dashboard creation
main.py                   # Main orchestration script with CLI
start_dashboard.sh        # User-friendly setup script
```

## ⚠️ Important Notes

### Privacy and Security
- **Never share your Duolingo password** with untrusted sources
- This project runs locally on your machine - no data is sent to external servers
- Consider using the DuoJSON API option (no password required) for basic tracking

### API Limitations
- These are **unofficial APIs** that may stop working if Duolingo changes their systems
- Rate limiting may apply - the script includes delays to be respectful
- Some data may not be available depending on your account settings

### Terms of Service
- Ensure you comply with Duolingo's Terms of Service when using these APIs
- This tool is for personal use and educational purposes

## 🛠️ Development

### Project Structure
```
├── main.py                     # Main orchestration script
├── duolingo_data_fetcher.py   # Data fetching module
├── data_storage.py            # Data processing and storage
├── dashboard.py               # Dashboard creation
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── data/                     # Data storage directory
    ├── raw_duolingo_data.json
    ├── daily_stats.csv
    ├── language_progress.csv
    └── processed_duolingo_data.json
```

### Adding New Visualizations

1. Create a new chart function in `dashboard.py`
2. Add the chart to the app layout
3. Update the callback function if needed

### Extending Data Sources

1. Add new fetch methods to `DuolingoDataFetcher`
2. Update data processing in `data_storage.py`
3. Modify dashboard to display new data types

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is for educational purposes. Please respect Duolingo's Terms of Service and use responsibly.

## 🙏 Acknowledgments

### Original Repository
This project is a fork and significant enhancement of **[lauslim12/japanese-duolingo-visualizer](https://github.com/lauslim12/japanese-duolingo-visualizer)** by [lauslim12](https://github.com/lauslim12). The original repository provided the foundational concept and inspiration for this enhanced version.

**Key contributions from the original repository:**
- Initial concept and motivation for Duolingo progress visualization
- Basic data fetching architecture
- Foundation for tracking language learning progress
- Inspiration for the overall project structure

### Additional Credits
- **Duolingo** for creating an amazing language learning platform
- **Community developers** who created unofficial APIs and the `duolingo-api` Python package
- **Plotly and Dash teams** for excellent interactive visualization tools
- **Kartik Talwar** for the Unofficial Duolingo API that inspired the original project
- **Satella** and **Freedomofkeima** for additional inspiration mentioned in the original repository

### What's New in This Version
This enhanced version transforms the original static Japanese-focused visualizer into a comprehensive, interactive dashboard that:
- Supports all Duolingo languages (not just Japanese)
- Provides real-time interactive visualizations
- Offers multiple data source options for better privacy
- Includes sample data mode for easy testing
- Features a user-friendly command-line interface
- Maintains local data processing for privacy

---

**Happy Learning! 🎉📚**