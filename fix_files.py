import os

project_path = r"C:\Projects\NoShowPrediction"

# CSS content
css = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
  --djai-primary: #1e3a8a;
  --djai-secondary: #d4af37;
  --djai-dark: #0f172a;
  --djai-light: #f3f4f6;
  --djai-gray: #6b7280;
  --djai-white: #ffffff;
}

body {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background-color: var(--djai-light);
  color: var(--djai-dark);
  line-height: 1.6;
}

.navbar {
  background: linear-gradient(135deg, var(--djai-primary) 0%, var(--djai-dark) 100%);
  box-shadow: 0 2px 10px rgba(30, 58, 138, 0.3);
  padding: 1rem 0;
}

.navbar-brand {
  color: var(--djai-white) !important;
  font-weight: 700;
  font-size: 1.5rem;
  text-decoration: none;
}

.navbar-brand span {
  color: var(--djai-secondary);
}

.btn-primary {
  background-color: var(--djai-primary);
  border-color: var(--djai-primary);
  color: var(--djai-white);
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: var(--djai-dark);
  border-color: var(--djai-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
}

.btn-secondary {
  background-color: var(--djai-secondary);
  border-color: var(--djai-secondary);
  color: var(--djai-dark);
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #f0d878;
  border-color: #f0d878;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

.card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border: none;
  overflow: hidden;
}

.card-header {
  background-color: var(--djai-primary);
  color: white;
  font-weight: 600;
  padding: 1.25rem;
}

.footer {
  background-color: var(--djai-dark);
  color: white;
  padding: 2rem 0;
  margin-top: 3rem;
}

.risk-high {
  background: #fee2e2;
  color: #dc2626;
  border: 2px solid #fecaca;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
}

.risk-medium {
  background: #fef3c7;
  color: #d97706;
  border: 2px solid #fcd34d;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
}

.risk-low {
  background: #d1fae5;
  color: #16a34a;
  border: 2px solid #86efac;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
}

.stat-card {
  background: white;
  border-left: 4px solid var(--djai-secondary);
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.stat-card.primary {
  border-left-color: var(--djai-primary);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--djai-primary);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: var(--djai-gray);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.table thead th {
  background-color: var(--djai-primary);
  color: white;
  font-weight: 600;
  border: none;
  padding: 1rem;
}

.table tbody td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}
"""

# HTML content
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No-Show Predictor | DJ AI Consulting</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/djai-brand.css">
    <style>
        .navbar-brand span { color: #d4af37; }
        .footer span { color: #d4af37; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <strong>DJ AI</strong><span>Consulting</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="/predict">Predict</a></li>
                    <li class="nav-item"><a class="nav-link" href="/patients">Patients</a></li>
                    <li class="nav-item"><a class="nav-link" href="/analytics">Analytics</a></li>
                </ul>
            </div>
        </div>
    </nav>
    
    <main class="container my-4">
        <!-- Content goes here -->
    </main>
    
    <footer class="footer">
        <div class="container text-center">
            <strong>DJ AI</strong><span>Consulting</span>
            <p class="mb-0">&copy; 2026 DJ AI Business Consulting</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

# Delete old files
css_path = os.path.join(project_path, "static", "css", "djai-brand.css")
html_path = os.path.join(project_path, "templates", "base.html")

for path in [css_path, html_path]:
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {path}")

# Write new files
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print(f"Created: {css_path}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Created: {html_path}")

print("\n" + "="*50)
print("SUCCESS! Files created correctly.")
print("="*50)