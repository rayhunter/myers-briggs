# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Myers-Briggs Personality Test web application built with Flask. The application presents users with a 10-question personality assessment and calculates their MBTI type based on their responses.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
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
pytest -q
# Note: Test directory exists but may be empty
```

## Architecture

### Core Application Structure
- **Single-file Flask app**: All application logic is contained in `app.py`
- **Template-based UI**: Uses Jinja2 templates with a base template pattern
- **Session-based state**: User responses and results are stored in Flask sessions
- **Static assets**: Background image and favicon in `/static/`

### Key Components

#### MBTI Assessment Logic (`app.py:8-79`)
- **MBTI_QUESTIONS**: 10-question dataset covering 4 personality dimensions (E/I, S/N, T/F, J/P)
- **calculate_mbti_type()**: Core algorithm that processes user responses and determines MBTI type
- **MBTI_DESCRIPTIONS**: Personality type descriptions for all 16 MBTI types

#### Flask Routes
- `/` - Home page, clears session
- `/test` - Question presentation page
- `/submit` - Processes form submission and calculates results
- `/results` - Displays MBTI type and scores

#### Template Structure
- **base.html**: Contains all CSS styling and layout structure
- **index.html**: Landing page
- **test.html**: Question form with radio button options
- **results.html**: Results display with type, description, and dimension scores

### Data Flow
1. User starts test → session cleared
2. Questions presented → user selections stored in form
3. Form submitted → answers processed by `calculate_mbti_type()`
4. Results stored in session → redirect to results page
5. Results displayed with type, description, and scoring breakdown

## Development Notes

- Virtual environments are in both `/virtual/` and `/venv/` directories
- The application uses Flask's built-in development server with debug mode
- All styling is embedded in the base template (no separate CSS files)
- Background image is large (13MB) and loaded from static assets
- No database - all data is hardcoded in the application