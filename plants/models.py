from django.db import models
from django.core.validators import RegexValidator
import requests
from django.utils.text import slugify
from django.utils import timezone
from .utils.inaturalist_image_api import get_inaturalist_image_urls
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import logging
import uuid
from account.models import Profile
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItemBase


class PlantTagCategory(models.Model):
    """
    Categorizes tags with emojis and colors for better visual organization
    """
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=8)  # For storing the emoji character
    color = models.CharField(max_length=20, default='#6c757d')  # Default to a neutral gray
    
    def __str__(self):
        return f"{self.emoji} {self.name}"


class PlantTag(Tag):
    """
    Extended Tag model that adds categories
    """
    category = models.ForeignKey(PlantTagCategory, 
                                on_delete=models.SET_NULL, 
                                null=True, 
                                blank=True,
                                related_name='tags')
    
    class Meta:
        db_table = 'plants_planttag'

    def __str__(self):
        return f"{self.name} {self.category.emoji if self.category else ''}"


class PlantTaggedItem(TaggedItemBase):
    """
    Custom through model to use with PlantTag
    Connects the custom tag to the model being tagged
    """
    content_object = models.ForeignKey(
        'plants.Plant', 
        on_delete=models.CASCADE
    )
    
    tag = models.ForeignKey(
        'plants.PlantTag', 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_items"
    )


class Plant(models.Model):
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    slug = models.SlugField(max_length=120, unique=False)

    common_name = models.CharField(max_length=100)
    family = models.CharField(max_length=30)
    zones = models.JSONField(blank=True, default=list)
    light = models.CharField(
        max_length=3,
        validators=[RegexValidator(regex='^[fds]{1,3}$')],    
    )
    moisture = models.CharField(
        max_length=3,
        validators=[RegexValidator(regex='^[xmh]{1,3}$')],
    )
    form = models.CharField(
        max_length=10,
        choices=[('Herb', 'Herb'),
        ('Shrub', 'Shrub'),
        ('Tree', 'Tree'),
        ('Bamboo', 'Bamboo'),
        ('Vine', 'Vine')],
    )
    form_size = models.CharField(max_length=5)
    min_h = models.FloatField()
    max_h = models.FloatField()
    min_w = models.FloatField()
    max_w = models.FloatField()

    description = models.TextField(null=True, blank=True) 

    tags = TaggableManager(through=PlantTaggedItem)

    class Meta:
        ordering = ['genus', 'species']
        indexes = [
            models.Index(fields=['genus', 'species'], name='latin_name_idx')
        ]

    def save(self, *args, **kwargs):
        # Generate slug if it doesn't exist
        if not self.slug:
            self.slug = slugify(f"{self.genus}-{self.species}")

        super().save(*args, **kwargs) 


    def __str__(self):
        latin_name = f"{self.genus} {self.species}"
        return latin_name
    
    def delete_photos(self):
        for image in self.images.all():
            image.delete()

    def load_photos(self):
        self.delete_photos()
        photo_urls = get_inaturalist_image_urls(genus=self.genus, species=self.species)
        for url in photo_urls:
            Image.objects.get_or_create(plant=self, url=url, defaults={'slug': None})


class Image(models.Model):
    plant = models.ForeignKey(Plant, related_name='images', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, null=True, blank=True)  # Make nullable
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='plant_images/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f"Image for {self.plant.genus} {self.plant.species}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.plant.genus}-{self.plant.species}-{uuid.uuid4().hex[:8]}")
        if not self.image and self.url:
            self.download_image()
        super().save(*args, **kwargs)

    def download_image(self):
        logger = logging.getLogger(__name__)
        logger.info(f"Attempting to download image from {self.url}")
        response = requests.get(self.url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()

            file_name = f"{self.plant.genus}_{self.plant.species}_{uuid.uuid4().hex[:8]}.jpg"
            self.image.save(file_name, File(img_temp), save=False)
            logger.info(f"Successfully downloaded and saved image: {file_name}")
        else:
            logger.error(f"Failed to download image. Status code: {response.status_code}")


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile')
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.user_profile.user.username} on {self.plant}'
    