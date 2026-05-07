# DocGen - Smart Documentation Generator

## What is DocGen?

DocGen is an AI-powered documentation generator. Upload your code files or analyze GitHub repositories and get professional documentation in seconds.

## Features

- Upload multiple code files (Python, JavaScript, HTML, CSS, JSON, etc.)
- Analyze individual files or merge all into one documentation
- GitHub repository analysis
- Generate README, API Docs, Wiki, and Changelog
- Export to Markdown, HTML, PDF, ZIP
- Copy to clipboard
- PWA support (install on mobile)
- 59 AI models via OpenRouter

## Installation

```bash
git clone https://github.com/assmm123/Dokle.git
cd Dokle
pip install -r requirements.txt
```

Quick Start

```bash
python main.py
```

Open: http://127.0.0.1:5000

CLI Usage

```bash
# Analyze a file
python cli.py analyze app.py

# Generate documentation for a folder
python cli.py generate src/ --merge

# Analyze a GitHub repository
python cli.py github psf/requests
```

Requirements

· Python 3.11+
· Flask, httpx, markdown, fpdf2, requests

License

MIT
