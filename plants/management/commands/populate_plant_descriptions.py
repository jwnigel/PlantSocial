import json
from django.core.management.base import BaseCommand
from plants.models import Plant
from plants.utils.gen_plant_info import generate_plant_description


class Command(BaseCommand):
    help = 'Generate descriptions for each plant'

    def handle(self, *args, **kwargs):
        plants = Plant.objects.all()
        updated_count = 0

        for plant in plants:
            plant.description = generate_plant_description(f"{plant.genus} {plant.species}")
            plant.save(update_fields=['description'])
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated descriptions for {updated_count} plants.'))
