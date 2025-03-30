from django.db import models
from taggit.models import GenericTaggedItemBase, TagBase

class CustomTag(TagBase):
    def get_css_class(self):
        css_classes = {
            'nut': 'nut-tag',
            'fruit': 'fruit-tag',
            'vegetable': 'vegetable-tag',
            'tree': 'tree-tag',
            'shrub': 'shrub-tag',
            'herb': 'herb-tag',
            'grass': 'grass-tag',
            'edible': 'edible-tag',
            'perennial': 'perennial-tag',
            'annual': 'annual-tag',
            'root': 'root-tag',
        }
        return css_classes.get(self.name, 'generic-tag')
    
class CustomTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(CustomTag, related_name="tagged_items", on_delete=models.CASCADE)
    content_object = models.ForeignKey('Plant', on_delete=models.CASCADE)
