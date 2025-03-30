from django.core.management.base import BaseCommand
from plants.models import Plant

class Command(BaseCommand):
    help = 'Populates the slug field for all Plant objects'

    def handle(self, *args, **options):
        plants = Plant.objects.all()
        for plant in plants:
            plant.slug = plant.genus + '-' + plant.species
            plant.save()
        self.stdout.write('Slugs populated successfully!')