import json
from django.core.management.base import BaseCommand
from plants.models import Plant
from plants.utils.gen_plant_info import generate_plant_description

class Command(BaseCommand):
    help = 'Import plant data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing plant data')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        # Open and read the JSON file
        with open(json_file_path, 'r') as file:
            all_plant_data = json.load(file)

        # Process each plant data dictionary
        for plant_data in all_plant_data:
            # Convert zones from string representation of a list to a list of integers
            if isinstance(plant_data.get('zones'), str):
                plant_data['zones'] = json.loads(plant_data['zones'])

            # Create or update the Plant object
            Plant.objects.update_or_create(
                genus=plant_data['genus'],
                species=plant_data['species'],
                common_name=plant_data['common_name'],
                family=plant_data['family'],
                defaults={
                    'zones': plant_data['zones'],
                    'light': plant_data['light'],
                    'moisture': plant_data['moisture'],
                    'form': plant_data['form'],
                    'form_size': plant_data['form_size'],
                    'min_h': plant_data['min_h'],
                    'max_h': plant_data['max_h'],
                    'min_w': plant_data['min_w'],
                    'max_w': plant_data['max_w'],
                    'description': generate_plant_description(f"{plant_data['genus']} {plant_data['species']}"),
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported plant data'))
