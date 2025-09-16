# Myers-Briggs Personality Test

A Flask web application that provides an interactive Myers-Briggs Type Indicator (MBTI) personality test. Users can take a 10-question assessment and receive their personality type along with detailed descriptions.

## Features

- **Interactive Quiz**: 10 carefully crafted questions covering all four MBTI dimensions
- **Real-time Results**: Instant personality type calculation and display
- **Detailed Descriptions**: Comprehensive personality type descriptions for all 16 MBTI types
- **Clean UI**: Modern, responsive web interface
- **Session Management**: Secure session handling for test results

## MBTI Dimensions Tested

- **Extraversion (E) vs Introversion (I)**: Social energy and interaction preferences
- **Sensing (S) vs Intuition (N)**: Information processing and learning styles
- **Thinking (T) vs Feeling (F)**: Decision-making approaches
- **Judging (J) vs Perceiving (P)**: Structure and flexibility preferences

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd myers-briggs
   ```

2. **Create and activate virtual environment**
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:8000`

## Usage

1. Navigate to the home page
2. Click "Start Test" to begin the personality assessment
3. Answer all 10 questions honestly
4. View your MBTI type and detailed personality description
5. Results are saved in your session for the duration of your visit

## Project Structure

```
myers-briggs/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── test.html      # Quiz page
│   └── results.html   # Results page
├── static/            # Static assets
│   ├── background.jpg
│   ├── favicon.ico
│   └── favicon.png
└── README.md
```

## Dependencies

- **Flask 2.3.3**: Web framework
- **Python 3.7+**: Required for Flask compatibility

## Development

The application runs in debug mode by default. To disable debug mode, modify `app.run(debug=True)` in `app.py`.

## License

This project is open source and available under the MIT License.

