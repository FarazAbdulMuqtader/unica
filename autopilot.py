import os, time, json
import requests, yaml
from jinja2 import Template

# ---------- SOURCES: each returns a list of normalized items ----------
def github_source(cfg):
    url = f"https://api.github.com/users/{cfg['github']}/repos?per_page=100"
    headers = {}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            repos = resp.json()
            break
        except requests.RequestException as e:
            print(f"GitHub attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    else:
        raise SystemExit("GitHub API failed after 3 tries")

    return [{
        "source": "github",
        "title": r["name"],
        "description": r["description"] or "",
        "tags": [r["language"]] if r["language"] else [],
        "url": r["html_url"],
        "updated": r["updated_at"],
    } for r in repos if not r["fork"]]

SOURCES = [github_source]          # add new sources here later

# ---------- PROCESSORS: take items, return items ----------
PROCESSORS = []                    # LLM summaries, ranking, etc. go here later

# ---------- RENDERER ----------
PAGE = Template("""
<h1>{{ cfg.name }}</h1><p>{{ cfg.tagline }}</p>
<p>Skills: {{ cfg.skills | join(', ') }}</p>
<h2>Projects</h2>
<ul>{% for i in items %}
  <li><a href="{{ i.url }}">{{ i.title }}</a> - {{ i.description }}</li>
{% endfor %}</ul>
""")

def main():
    cfg = yaml.safe_load(open("profile.yaml"))
    items = [i for src in SOURCES for i in src(cfg)]
    for proc in PROCESSORS:
        items = proc(items, cfg)
    items.sort(key=lambda i: i["updated"], reverse=True)
    json.dump(items, open("data.json", "w"), indent=2)
    open("index.html", "w").write(PAGE.render(cfg=cfg, items=items))

if __name__ == "__main__":
    main()
