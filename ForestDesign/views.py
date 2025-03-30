from django.http import HttpResponse

def index(request):
    return HttpResponse(f"Hey. This is the main page. 🌱 \n<a href='/plants/'>Go to the database.</a>")
