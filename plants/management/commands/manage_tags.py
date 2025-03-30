from django.core.management.base import BaseCommand, CommandError
from plants.models import PlantTagCategory, PlantTag
from plants.utils.tag_constants import TAG_EMOJIS

class Command(BaseCommand):
    help = 'Manage plant tags and categories'

    def add_arguments(self, parser):
        parser.add_argument('--sync', action='store_true', help='Sync tags from tag_constants.py')
        parser.add_argument('--add', nargs=3, metavar=('NAME', 'EMOJI', 'COLOR'), help='Add a new tag (name, emoji, color)')
        parser.add_argument('--list', action='store_true', help='List all tags')
        parser.add_argument('--update', nargs=4, metavar=('OLD_NAME', 'NEW_NAME', 'EMOJI', 'COLOR'), help='Update a tag')
        parser.add_argument('--delete', metavar='NAME', help='Delete a tag by name')

    def handle(self, *args, **options):
        if options['sync']:
            self._sync_tags()
        elif options['add']:
            self._add_tag(*options['add'])
        elif options['list']:
            self._list_tags()
        elif options['update']:
            self._update_tag(*options['update'])
        elif options['delete']:
            self._delete_tag(options['delete'])
        else:
            self.stdout.write('Please provide a command. Use --help for options.')

    def _sync_tags(self):
        """Sync tags from tag_constants.py"""
        for tag_data in TAG_EMOJIS:
            category, created = PlantTagCategory.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'emoji': tag_data['emoji'],
                    'color': tag_data['color']
                }
            )
            
            # Update existing categories
            if not created:
                category.emoji = tag_data['emoji']
                category.color = tag_data['color']
                category.save()
            
            # Create or update the tag
            tag, tag_created = PlantTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'category': category}
            )
            
            if not tag_created:
                tag.category = category
                tag.save()
                
        self.stdout.write(self.style.SUCCESS('Successfully synced tags from tag_constants.py'))

    def _add_tag(self, name, emoji, color):
        """Add a new tag"""
        # Check if exists
        if PlantTagCategory.objects.filter(name=name).exists():
            self.stdout.write(self.style.ERROR(f'Tag "{name}" already exists'))
            return
            
        category = PlantTagCategory.objects.create(
            name=name,
            emoji=emoji,
            color=color
        )
        
        tag = PlantTag.objects.create(
            name=name,
            category=category
        )
        
        self.stdout.write(self.style.SUCCESS(f'Added tag: {name} {emoji}'))

    def _list_tags(self):
        """List all tags"""
        tags = PlantTag.objects.select_related('category').all()
        
        if not tags:
            self.stdout.write('No tags found')
            return
            
        self.stdout.write('Current tags:')
        for tag in tags:
            cat = tag.category
            if cat:
                self.stdout.write(f'- {tag.name} ({cat.emoji}, {cat.color})')
            else:
                self.stdout.write(f'- {tag.name} (no category)')

    def _update_tag(self, old_name, new_name, emoji, color):
        """Update an existing tag"""
        try:
            category = PlantTagCategory.objects.get(name=old_name)
            tag = PlantTag.objects.get(name=old_name)
            
            # Update category
            category.name = new_name
            category.emoji = emoji
            category.color = color
            category.save()
            
            # Update tag name
            tag.name = new_name
            tag.save()
            
            self.stdout.write(self.style.SUCCESS(f'Updated tag: {old_name} -> {new_name} {emoji}'))
            
        except (PlantTagCategory.DoesNotExist, PlantTag.DoesNotExist):
            self.stdout.write(self.style.ERROR(f'Tag "{old_name}" not found'))

    def _delete_tag(self, name):
        """Delete a tag"""
        try:
            category = PlantTagCategory.objects.get(name=name)
            tag = PlantTag.objects.get(name=name)
            
            tag.delete()
            category.delete()
            
            self.stdout.write(self.style.SUCCESS(f'Deleted tag: {name}'))
            
        except (PlantTagCategory.DoesNotExist, PlantTag.DoesNotExist):
            self.stdout.write(self.style.ERROR(f'Tag "{name}" not found'))