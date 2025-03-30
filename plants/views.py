from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .forms import PlantFilterForm, CommentForm, TagForm
from .models import Plant, Image
from .utils.inaturalist_image_api import get_inaturalist_image_urls
from .utils.tag_constants import TAG_EMOJIS
import requests


def db_view(request, tag_slug=None):
    plant_list = Plant.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        plant_list = plant_list.filter(tags__in=[tag])
    filter_form = PlantFilterForm(request.GET)
    if filter_form.is_valid():
        for field in ['light', 'moisture', 'form']:
            value = filter_form.cleaned_data[field]
            if value:
                plant_list = plant_list.filter(**{f"{field}__icontains": value})

        paginator = Paginator(plant_list, 5)  # 5 results per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'db_view.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'tag': tag
    })

class PlantDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if method == 'get':
            if 'action' in kwargs:
                action = kwargs.pop('action')  # Remove 'action' from kwargs
                handler = getattr(self, action, self.http_method_not_allowed)
                print(f"Handler for action '{action}': {handler}")
            else:
                handler = self.get
            return handler(request, *args, **kwargs)
        return self.http_method_not_allowed(request, *args, **kwargs)


    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        comments = plant.comments.filter(active=True)
        tag_form = TagForm()
        comment_form = CommentForm()
        context = {'plant': plant, 'emojis': [TAG_EMOJIS.get(tag.name) for tag in plant.tags.all()],'comments': comments, 'comment_form': comment_form, 'tag_form': tag_form}
        return render(request, 'plant_detail.html', context)

    @method_decorator(require_GET)
    def get_main_image(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        main_image = Image.objects.filter(plant=plant).first()

        if not main_image:
            # If still no image, try to get one from iNaturalist
            image_url = get_inaturalist_image_urls(plant.genus, plant.species)
            if image_url:
                try:
                    original_image_url = image_url.replace('square', 'original')
                    response = requests.get(original_image_url)
                    response.raise_for_status()
                    main_image = Image(plant=plant, url=original_image_url)
                    main_image.image.save(f"{plant.genus}_{plant.species}.jpg", ContentFile(response.content), save=True)
                except requests.RequestException as e:
                    print(f"Error fetching image: {e}")
                    return JsonResponse({'error': 'Failed to fetch image'}, status=500)

        if main_image:
            return JsonResponse({'url': main_image.image.url, 'alt': plant.common_name})
        else:
            return JsonResponse({'❌ image error': 'No image available'}, status=404)

    @method_decorator(require_GET)
    def get_carousel_images(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        images = Image.objects.filter(plant=plant)[1:]  # Exclude the first image (main image)

        if not images:
            # If no additional images, try to load them
            plant.load_photos()
            images = Image.objects.filter(plant=plant)[1:]

        image_data = [{'url': image.image.url, 'alt': plant.common_name} for image in images]

        # If still no additional images, try to get from iNaturalist
        if not image_data:
            print('❌ Error getting carousel images!')

        return JsonResponse(image_data, safe=False)


@login_required
@require_POST
def plant_comment(request, slug):
    plant = get_object_or_404(Plant, slug=slug)
    comment = None
    form = CommentForm(data=request.POST, user=request.user)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.plant = plant
        comment.save()
        return redirect('plants:plant_detail', slug=plant.slug)
    
    return render(request, 
                  'comment.html', 
                  {'plant': plant, 'form': form, 'comment': comment})

@login_required
@require_POST
def plant_tag(request, slug):
    print('views.plant_tag')
    plant = get_object_or_404(Plant, slug=slug)
    form = TagForm(data=request.POST, user=request.user)

    if form.is_valid():
        tags = form.cleaned_data['tags']
        print(f'form is valid. tag: {tags}')

        for tag in tags:
            plant.tags.add(tag)

        return redirect('plants:plant_detail', slug=plant.slug)

