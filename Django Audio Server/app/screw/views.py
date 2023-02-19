import os
import filetype
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'audio/'))


@csrf_exempt
def files_list(request):
    files = fs.listdir('')[1]
    return render(request, 'files_list.html', {'files': files})


@csrf_exempt
def main(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        filet = filetype.guess(file)
        if file is not None and filet is not None and 'audio' in filet.mime:
            fs.save(file.name, file)
        else:
            return render(request, 'error.html')

    files = fs.listdir('')[1]
    return render(request, 'home.html', {'files': files})
