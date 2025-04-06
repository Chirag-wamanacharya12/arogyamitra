from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Document

def report(request):
    documents = Document.objects.filter()
    context = {
        'documents': documents
    }
    return render(request, 'reports/reports.html', context)


def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if title and file:
            Document.objects.create(title=title, file=file, description=description)
            return redirect('reports')  # You can change this to your own success URL
        else:
            error = "Title and file are required."
            return render(request, 'upload_document.html', {'error': error})
    
    return render(request, 'upload_document.html')

def delete_document(request, document_id):
    document = Document.objects.get(id=document_id)
    document.delete()
    return redirect('reports')