import openai
import requests
import json
import argparse
import os

api_key = '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'

url = "https://api.openai.com/v1/chat/completions"

def generate_plant_description(plant_name):
    # Define the prompt with the plant name inserted
    prompt = f"""
Generate a concise yet informative description of {plant_name} for a polyculture garden planning app. The description should be 2-3 paragraphs long and cover the following aspects:

Unique Characteristics:

Highlight what makes this plant stand out in polyculture settings
Describe its appearance, growth habit, and any notable features


Ecological Role and Benefits:

Native habitat and preferred growing conditions (soil pH, sunlight, moisture)
Ecosystem services (e.g., nitrogen fixation, pollinator attraction, soil improvement)
Interactions with other plants (companion planting potential, allelopathy)


Human Uses:

Edible parts and culinary uses
Medicinal properties or traditional uses
Other practical applications (e.g., fiber, dye, construction material)


Cultivation and Management:

Ease of propagation and growth rate
Maintenance requirements and potential challenges
Harvesting techniques and optimal timing
Storage methods for harvested parts (if applicable)


Drawbacks or Considerations:

Any potential negative impacts on other plants or the environment
Invasive potential in certain regions
Common pests or diseases, if significantly problematic


Style Guidelines:

Use a conversational yet concise tone
Prioritize specific, quantifiable information over vague generalities
Include numerical data where relevant (e.g., typical height, yield, days to maturity)
Avoid redundant information common to most plants in its category
Emphasize aspects that would influence a gardener's decision to include this plant in a polyculture system

Note: Tailor the content to emphasize the plant's role in diverse, ecologically-minded gardens. Focus on information that would be most valuable to someone planning a polyculture garden.
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": f"{prompt}"}],
        "temperature": 0.1,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Generate a plant description using OpenAI API.")
    parser.add_argument("genus_species", type=str, help="Enter the genus and species, e.g., 'Avellana corylus'")
    args = parser.parse_args()

    generate_plant_description(args.genus_species)

if __name__ == "__main__":
    main()

    