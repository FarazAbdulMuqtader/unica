# Unica

A self-updating portfolio. It pulls my public work from GitHub, builds a clean page from it, and refreshes itself every week with no manual edits.

**Live:** https://farazabdulmuqtader.github.io/unica/

## How it works

```
Sources  ->  data.json  ->  Processors  ->  Renderer
GitHub       (one format)   (coming soon)    index.html
```

1. `autopilot.py` fetches my public repos from the GitHub API.
2. Every item is normalized into one schema: `source, title, description, tags, url, updated`.
3. A Jinja2 template renders the data into `index.html`.
4. A GitHub Actions workflow runs the script every Monday, commits the result, and the site updates.

## Stack

Python, Requests, Jinja2, PyYAML, GitHub Actions, GitHub Pages

## Project structure

```
unica/
├── autopilot.py                  # fetch, normalize, render
├── profile.yaml                  # my details: name, tagline, skills
├── requirements.txt
├── data.json                     # generated
├── index.html                    # generated
└── .github/workflows/update.yml  # weekly automation
```

## Run it locally

```bash
git clone https://github.com/FarazAbdulMuqtader/unica.git
cd unica
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python autopilot.py
```

Then open `index.html` in your browser.

## Design

Every data source returns items in the same format, so new features plug in without changing the core. Adding a source means adding one function to `SOURCES`. Adding a processing step means adding one function to `PROCESSORS`.

## Roadmap

- [ ] Hugging Face and Kaggle as extra sources
- [ ] LLM-written project summaries
- [ ] PDF resume generated from the same data
- [ ] Search chatbot over my projects (RAG)
- [ ] Resume tailored to a job description

## Author

**Faraz**, BS Artificial Intelligence, University of Karachi
[GitHub](https://github.com/FarazAbdulMuqtader) · [Hugging Face](https://huggingface.co/FarazAbdulMuqtader)
