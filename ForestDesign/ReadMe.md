# 🌿 ForestDesign

A Django-powered plant database and design tool for garden enthusiasts! 

## 🌱 Features
- Plant database with detailed information ℹ️
- Custom tagging 🏷️
- Image management with iNaturalist integration 📸
- LLM generated plant descriptions with user input ⌨️
- Create a user profile or authenticate with Google to leave comments 💬
- Filter and search to find plants 🔎

## 🔜 Upcoming Features
- [ ] Wiki photos and descriptions -- allow users to upload their own photos and edit plant descriptions 
- [ ] LLM summary of user comments -- like Amazon reviews, create short LLM summaries of user experience with plant. Switch to open source LLM.
- [ ] Emoji-based plant tags. Custom django-taggit implementation
- [ ] Add plants to lists -- Favorites, My_Garden, Native_Wetland_Wildflowers, Client_Prairie_Design
- [ ] Drag and drop UI using saved lists. 2-D overhead view.  

## 🚀 Eventually...
- [ ] Mobile integration (iOS because it's what I know) to create maps of real field plantings. Mark plant locations and create map and data using mobile devices (iPhone and Apple Watch first)
- [ ] Dashboards visualizing crowd-sourced planting data. Growth rates, survival, nut/fruit production, etc. 
- [ ] Crowd-sourced restoration data!
- [ ] Crowd-sourced restorative agricultural / permaculture data!

## ⚡️ Quick Start
```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # or `myenv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Import plant data using just 8 example plants for now
python manage.py import_plants path/to/plants_8.json

# Run server
python manage.py runserver
```

## 📸 Image Credits
Plant images are sourced from iNaturalist's public API. See plants/utils/inaturalist_image_api.py

## 📝 Plant Descriptions
Plant descriptions are generated with openai's api. See plants/utils/gen_plant_info.py

---
Created by Nigel Wright

💚 