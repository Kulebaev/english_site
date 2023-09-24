from django.shortcuts import render


def index_view(request):
    return render(request, 'index.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)

    

