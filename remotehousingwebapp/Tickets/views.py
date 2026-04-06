from django.shortcuts import render

# Create your views here.
def home(request):
	"""Render the site home page."""
	return render(request, "home.html")
