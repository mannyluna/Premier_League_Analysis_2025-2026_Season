# ⚽ Soccer Analytics Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange.svg)
![mplsoccer](https://img.shields.io/badge/mplsoccer-Football%20Analytics-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python-based soccer analytics platform designed to transform raw football data into actionable insights through advanced visualizations, player comparisons, team analysis, and custom statistical models.

---

## 📖 Table of Contents

- [Features](#-features)
- [Visualizations](#-visualizations)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Metric Framework](#-metric-framework)
- [Technology Stack](#-technology-stack)
- [Performance Enhancements](#-performance-enhancements)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Features

### Player Analysis

- Position-specific player evaluation
- Radar chart comparisons
- Season performance summaries
- Per-90 and season percentage calculations 
- Team-adjusted performance metrics

### Team Analysis

- Team comparison dashboards
- Home vs. away goal performance tracking
- Offensive and defensive efficiency metrics
- Goal-scoring analysis
- Possession and passing metrics

### Shot Analysis

- Penalty area vs. outside-box analysis
- Shot-on-target percentage tracking
- Team finishing efficiency
- Custom pitch heatmaps
- Expected Goal (xG) visualizations

### Automated Calculations

- Season percentage recalculations
- Per-90 normalization
- Dynamic metric selection
- Build DataFame with performance metrics by position

---

## 📊 Visualizations

### Radar Charts

Compare players across multiple performance dimensions.

**Examples:**

- Defender Comparison
- Midfielder Comparison
- Attacker Comparison
- Goalkeeper Comparison

### Scatter Plots

Identify player and team strengths through quadrant-based analysis.

**Examples:**

- xG vs xGA
- Goals vs Goals Conceded
- Possession vs Defensive Actions

### Team Dashboards

Comprehensive team-level performance evaluations.

### Shot Maps

Visualize:

- Shot locations
- Shot quality
- Penalty area efficiency
- Shot-on-target percentage

---

## 📁 Project Structure

```text
soccer-analytics/
│
├── analysis/
│   ├── player_analyzer.py
│   ├── team_seasonranker.py
│   └── team_statistics.py
│
├── data/
│   ├── build_datasets.py
│   ├── data_loader.py
│   └── EPL_datadownload.py
│
├── visuals/
│   ├── radar_charts.py 
│   ├── animation_season.py
│   └── pitch_visuals.py
│
├── logos/
│   ├── logo_loader.py
│
├── requirements.txt
├── player_analysis.ipynb
├── season_analysis.ipynb
└── README.md
```

## 🏃 Usage

### Build Datasets

```python
from data.build_datasets import build_dataset

dataset = build_dataset()
```

### Create Player Comparison Radar

```python

fig, ax = plt.subplots(figsize=(6, 6))
mid_comparison = plyr_analysis.build_comparison("Bruno Fernandes","Rodrigo Rodri Hernandez", 'Midfielder', MID_METRICS)
radar.plot_radar(ax = ax, comparison = mid_comparison, colors  = default_pairs[2], logo_manager = lm)

```
<img width="491" height="528" alt="example" src="https://github.com/user-attachments/assets/b92dd562-3596-4ab9-995d-daff004081aa" />



### Team Ranking Animation for each Gameweek

```python
from visuals.animation_season import LeagueTableAnimation

animation = LeagueTableAnimation(fixture_analysis, team_colors)
fig, ani = animation.create_animation()
```
[visuals/output/league_table_animation.gif
](https://raw.githubusercontent.com/mannyluna/Premier_League_Analysis_2025-2026_Season/master/visuals/output/league_table_animation.gif)

---

## 📈 Metric Framework

### Percentage Metrics

Metrics ending with `_percent` are recalculated using season totals rather than averaging individual match percentages.

#### Examples

```python
accurate_passes_percent
accurate_crosses_percent
accurate_long_balls_percent
ground_duels_won_percent
aerial_duels_won_percent
```

#### Season Formula

```python
season_percent =
(total_successful_events / total_attempts) * 100
```

---

### Per-90 Metrics

Per-90 metrics are normalized using minutes played.

#### Examples

```python
goals
assists
shots
xg
xa
interceptions
tackles

```

#### Formula

```python
(metric_total / minutes_played) * 90
```

---

## 🛠 Technology Stack

### Data Processing

- Pandas
- NumPy

### Visualization

- Matplotlib
- mplsoccer
- Pillow

### Development

- Python 3.11+
- Object-Oriented Design
- Modular Analytics Framework

---

## ⚡ Performance Enhancements

Current optimizations include:

- Vectorized Pandas operations
- Dynamic metric generation
- Reusable chart components
- Position-specific metric mappings
- Automatic percentage recalculations
- Reduced DataFrame duplication
- Centralized configuration management
- Cached dataset processing

---

## 🔮 Roadmap

### In Progress

- [ ] Expected Threat (xT)
- [ ] Passing Networks
- [ ] Advanced Team Dashboards
- [ ] Enhanced Shot Analysis

### Future Features

- [ ] Interactive Dashboards
- [ ] Streamlit Web Application
- [ ] Player Similarity Engine
- [ ] Match Simulation Models
- [ ] Automated Report Generation
- [ ] Machine Learning Projections<img width="491" height="528" alt="example" src="https://github.com/user-attachments/assets/729added-6965-49a0-a2db-7b31ddfe49a9" />

---

## 🤝 Contributing

Contributions, suggestions, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request


## 👤 Author

### Hector Lopez

Soccer Analytics • Data Visualization • Python Development

Passionate about leveraging data science and visualization techniques to evaluate players, analyze team performance, and uncover meaningful football insights.

---

⭐ If you find this project useful, consider starring the repository.
