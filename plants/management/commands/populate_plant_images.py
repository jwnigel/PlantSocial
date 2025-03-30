from django.core.management.base import BaseCommand
from plants.models import Plant, Image
from plants.utils.inaturalist_image_api import get_inaturalist_image_urls
from django.core.files.base import ContentFile
import requests

class Command(BaseCommand):
    help = 'Populates images for all plants'

    def handle(self, *args, **options):
        plants = Plant.objects.all()
        for plant in plants:
            if not plant.images.exists():
                image_url = get_inaturalist_image_urls(plant.genus, plant.species)
                if image_url:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image = Image(plant=plant, url=image_url)
                        image.image.save(f"{plant.genus}_{plant.species}.jpg", ContentFile(response.content), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully added image for {plant.genus} {plant.species}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No image found for {plant.genus} {plant.species}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Image already exists for {plant.genus} {plant.species}'))