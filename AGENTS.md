# PUBG Circle Analyzer Agent Guide

## Setup
- Requires Python 3.9 (not 3.10+)
- Clone repo
- Create and activate virtual environment:
  - `python -m venv venv`
  - `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Install deps: `pip install -r requirements.txt`
- Download map assets: https://github.com/pubg/api-assets/tree/master/Assets/Maps -> assets/ folder
  - Rename exactly: baltic_main.png (Erangel), desert_main.png (Miramar), dihorotok_main.png (Vikendi), kiki_main.png (Deston), neon_main.png (Rondo), tiger_main.png (Taego)
- Set PUBG API key in config/pubg_api_config.py: `API_KEY = "your_key"`
- Initialize: `python main.py -i` (creates DB and folders)
- Docker setup: `docker compose up -d` (requires fixing requests version in requirements.txt first)

## Common Tasks
- Fetch tournaments: `python main.py -t [--date DD-MM-YY]`
- Extract circle data: `python main.py -e [-server esport|live|both] [-maps <map>]`
- Generate heatmaps: `python main.py -c [-server esport|live|both] [-maps <map>]`
- Predict circles: `python main.py -p -maps <single_map> [-zone 4|8] [-mode SVC|KNN]`
- Generate histograms: `python main.py -hist [-server esport|live|both]`
- Specify player IDs: `-pl player1 player2 ...`
- Manual tournament IDs: `-t_ids id1 id2 ...`

## Important Notes
- Follow existing code style and patterns
- Show changes before implementing
- Prefer existing code over new implementations
- Database uses MySQL via Peewee ORM (config in config/db_config.py)
- Map assets must match exact filenames as listed above
- Virtual environment recommended but not required
- Test commands work from project root directory
- Dockerfile requires libgl1 instead of libgl1-mesa-glx for Ubuntu/Debian
- Requests version in requirements.txt must be compatible with Python 3.9 (use 2.31.0)