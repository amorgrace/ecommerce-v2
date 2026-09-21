from django.shortcuts import render


def home_view(request):
    """Render the landing page for UDDY API BASE."""
    return render(request, "index.html")
