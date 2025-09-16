# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Myers-Briggs Personality Test web application built with Flask. The application presents users with a 10-question personality assessment and calculates their MBTI type based on responses across four personality dimensions (E/I, S/N, T/F, J/P).

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (user prefers 'virtual' name)
source virtual/bin/activate  # macOS/Linux
# OR
virtual\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
# Application runs on http://localhost:8000 in debug mode
```

### Testing
```bash
# Test directory exists but is currently empty
pytest tests/ -v
```

## Architecture

### Core Application Structure
- **Single-file Flask application**: All logic contained in `app.py`
- **Session-based state management**: User responses and results stored in Flask sessions
- **Template inheritance**: Uses Jinja2 templates with base template pattern
- **No database**: All MBTI questions and descriptions hardcoded in application

### Key Components

#### MBTI Assessment Engine (`app.py`)
- **MBTI_QUESTIONS**: 10-question dataset covering all 4 personality dimensions
- **calculate_mbti_type()**: Core algorithm processing user responses to determine personality type
- **MBTI_DESCRIPTIONS**: Complete personality descriptions for all 16 MBTI types

#### Flask Routes Architecture
- `/` - Home page (clears session state)
- `/test` - Question presentation with form handling
- `/submit` - POST endpoint for answer processing and MBTI calculation
- `/results` - Results display with type, description, and dimension scores

#### Template Structure
- **base.html**: Contains all CSS styling and layout (no separate CSS files)
- **index.html**: Landing page with start button
- **test.html**: Question form with radio button interface
- **results.html**: Results display with scoring breakdown

### Data Flow
1. Session cleared on home page visit
2. 10 questions presented via single form
3. Form submission triggers `calculate_mbti_type()` algorithm
4. Results stored in session and user redirected
5. Results page displays personality type with detailed description and dimension scores

## Development Notes

- Virtual environments exist in both `/virtual/` and `/venv/` directories
- Application uses Flask's development server with debug mode enabled
- Background image (13MB) served from `/static/background.jpg`
- All styling embedded in base template
- Session management uses Flask's built-in session handling with random secret key

## Key Files
- `app.py`: Main Flask application (single file contains all logic)
- `requirements.txt`: Only dependency is Flask==2.3.3
- `templates/`: Jinja2 templates with inheritance structure
- `static/`: Contains background image and favicon assets
