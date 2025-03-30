# 🌿 ForestDesign

A Django-powered plant database and design tool for garden enthusiasts! 

## 🌱 Features
- Plant database with detailed information
- Custom tagging system with emoji categories 🏷️
- Image management with iNaturalist integration 📸
- User comments and interactions 💬
- Zone-based plant filtering 🗺️

## 🛠️ Tech Stack
- Django 5.1.1
- django-taggit (custom implementation)
- SQLite
- Python 3.12

## 🚀 Quick Start
```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # or `myenv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Import plant data
python manage.py import_plants path/to/plants.json

# Run server
python manage.py runserver
```

## 📝 Plant Model Features
- Scientific name (genus & species)
- Common name
- USDA hardiness zones
- Light requirements (full sun, partial shade, shade)
- Moisture needs (xeric, mesic, hydric)
- Growth form & size
- Auto-generated descriptions

## 👥 Contributing
Feel free to open issues and pull requests! We love community contributions.

## 📸 Image Credits
Plant images are sourced from iNaturalist's public API.

---
Made with 💚 by Nigel Wright 