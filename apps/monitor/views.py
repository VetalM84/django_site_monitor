from django.shortcuts import render


async def index(request):
    """Index view."""
    return render(request, 'monitor/index.html', context={"monitor": "Hi,there!"})
