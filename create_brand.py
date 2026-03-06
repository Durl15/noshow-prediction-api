import os
project_path = r"C:\Projects\NoShowPrediction"
css_path = os.path.join(project_path, "static", "css", "djai-brand.css")
html_path = os.path.join(project_path, "templates", "base.html")

for path in [css_path, html_path]:
    if os.path.exists(path):
        os.remove(path)

css = b'''/* DJ AI Consulting Brand CSS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
:root { --djai-primary: #1e3a8a; --djai-secondary: #d4af37; --djai-dark: #0f172a; --djai-light: #f3f4f6; --djai-gray: #6b7280; }
body { font-family: 'Inter', sans-serif; background: var(--djai-light); color: var(--djai-dark); }
.navbar { background: linear-gradient(135deg, var(--djai-primary) 0%, var(--djai-dark) 100%); }
.navbar-brand { color: white !important; font-weight: 700; }
.navbar-brand span { color: var(--djai-secondary); }
.btn-primary { background: var(--djai-primary); border-color: var(--djai-primary); }
.btn-secondary { background: var(--djai-secondary); border-color: var(--djai-secondary); color: var(--djai-dark); font-weight: 600; }
.footer { background: var(--djai-dark); color: white; padding: 2rem 0; margin-top: 3rem; }
.risk-high { background: #fee2e2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; display: inline-block; }
.risk-medium { background: #fef3c7; color: #d97706; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; display: inline-block; }
.risk-low { background: #d1fae5; color: #16a34a; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; display: inline-block; }
.stat-card { background: white; border-left: 4px solid var(--djai-secondary); padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.stat-card.primary { border-left-color: var(--djai-primary); }
.stat-number { font-size: 2.5rem; font-weight: 700; color: var(--djai-primary); }
'''

html = b'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>No-Show Predictor | DJ AI Consulting</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="/static/css/djai-brand.css">
<style>.navbar-brand span, .footer span { color: #d4af37; }</style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark">
<div class="container">
<a class="navbar-brand" href="/"><strong>DJ AI</strong><span>Consulting</span></a>
<div class="collapse navbar-collapse">
<ul class="navbar-nav ms-auto">
<li class="nav-item"><a class="nav-link" href="/">Dashboard</a></li>
<li class="nav-item"><a class="nav-link" href="/predict">Predict</a></li>
</ul>
</div>
</div>
</nav>
<main class="container my-4">{% block content %}{% endblock %}</main>
<footer class="footer">
<div class="container text-center">
<strong>DJ AI</strong><span>Consulting</span>
<p class="mb-0">&copy; 2026 DJ AI Business Consulting</p>
</div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

with open(css_path, 'wb') as f:
    f.write(css)
print('CSS created')

with open(html_path, 'wb') as f:
    f.write(html)
print('HTML created')
print('Done!')