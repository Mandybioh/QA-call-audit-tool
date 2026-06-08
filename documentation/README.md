# QA Audio Call Selector & Dashboard

A comprehensive Streamlit application suite for conducting QA audits on audio call recordings with real-time statistics and analytics.

## 📋 Features

### **tool.py - QA Call Selector**
- 🎧 Browse and load audio files (MP3, WAV, M4A)
- 🎲 Two sampling methods:
  - **Pure Random**: Randomly select calls from all recordings
  - **Stratified by Agent**: Ensure representation from each agent
- ⭐ Rate calls on a 1-10 quality scale
- 💬 Add detailed comments and feedback
- 📊 View immediate statistics after each audit
- 💾 Save audit results to Excel with timestamps
- 📈 Automatic agent and date extraction from filenames

### **dashboard.py - Analytics Dashboard**
- 📊 Load and visualize all historical audit logs
- 🔍 Multi-filter interface:
  - Date range selector
  - Agent multi-select filter
  - QA score range slider
- 📈 Five analytics tabs:
  - **Overview**: Score distribution, average gauge
  - **Agent Performance**: Agent rankings, call counts
  - **Timeline**: Trends over time, audit volume
  - **Comments**: Searchable feedback by score
  - **Raw Data**: Full dataset with CSV export

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
cd "c:\Users\a.biomarfo\Documents\dashboards\QA call audit tool"
pip install -r requirements.txt
```

### 2. Run the QA Selector Tool
```powershell
streamlit run tool.py
```
Then:
1. Enter the path to your folder containing audio files
2. Choose sampling type and number of calls
3. Click "Select Random Calls"
4. Rate each call (1-10) and add comments
5. Click "Save Audit Log" to export to Excel

### 3. Run the Analytics Dashboard
```powershell
streamlit run dashboard.py
```
Then:
1. Use filters in the sidebar to explore data
2. Switch between tabs for different views
3. Download filtered data as CSV if needed

## 📁 File Naming Convention

For best results, name your audio files with this format:
```
AgentName_CallID_YYYY-MM-DD_OtherInfo.mp3
```

Examples:
- `john_smith_12345_2024-02-18_customer_service.mp3`
- `alice_johnson_67890_20240218_tech_support.wav`

Supported date formats:
- `YYYY-MM-DD`
- `YYYYMMDD`
- `DD-MM-YYYY`

## 📊 Output Files

Audit logs are saved as:
```
audit_log_YYYY-MM-DD_HH-MM-SS.xlsx
```

Contains columns:
- File_Name
- Agent
- Date
- QA_Score (1-10)
- QA_Comments
- Audit_Timestamp

## ⚙️ System Requirements

- Python 3.8+
- 100MB+ disk space
- Audio playback capable browser
- Working directory permissions

## 🐛 Troubleshooting

**"Audio file not found" error**
- Verify the folder path is correct
- Ensure audio files have .mp3, .wav, or .m4a extension
- Check file permissions

**"No audit logs found" in dashboard**
- Ensure you've run at least one audit with tool.py
- Dashboard looks for files named `audit_log_*.xlsx` in current directory
- Move audit files to the same directory as dashboard.py if needed

**Import errors when running**
- Run: `pip install -r requirements.txt`
- If issues persist, try: `pip install --upgrade streamlit pandas plotly openpyxl`

## 📝 Tips & Best Practices

1. **Stratified Sampling**: Use this for representative audits across all agents
2. **Consistent Feedback**: Establish scoring guidelines for your team
3. **Regular Reviews**: Export dashboard data weekly for trend analysis
4. **Backup Audit Logs**: Save Excel files to cloud storage for backup
5. **Agent Names**: Extract agent name from filename format for automatic grouping

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all files remain in the same directory
3. Ensure dependencies are installed: `pip list | findstr streamlit`

---

**Version**: 1.0  
**Last Updated**: February 18, 2026
