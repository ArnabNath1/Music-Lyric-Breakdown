# Music Lyric Breakdown

An AI-powered tool that analyzes and breaks down song lyrics using LangChain, LlamaIndex, and Gemini Pro.

## Features

- Deep lyrical analysis and interpretation
- Sentiment analysis of lyrics
- Theme and subject matter identification
- Musical elements breakdown
- Contextual and cultural references detection

## Prerequisites

- Python 3.8+
- Google Cloud API key for Gemini Pro
- Required Python packages (specified in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Music-Lyric-Breakdown.git
cd Music-Lyric-Breakdown
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export GOOGLE_API_KEY=your_api_key_here
```

## Usage

```python
python analyze_lyrics.py --song "song_title" --artist "artist_name"
```

## Project Structure

```
Music-Lyric-Breakdown/
├── src/
│   ├── analyzer.py
│   ├── utils.py
│   └── models.py
├── tests/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google's Gemini Pro
- LangChain
- LlamaIndex
