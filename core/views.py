from django.shortcuts import render
from core.models import LangchainPgEmbedding
from core.embedding import get_embedding
from pgvector.django import L2Distance, CosineDistance

def index(request):
    if request.method == 'POST':
        text = request.POST.get('input_text')
        if not text:
            # If input_text is empty, return the same page with an error message
            context = {
                'error_message': 'Please enter a search term.'
            }
            return render(request, 'index.html', context)
        
        embedding = get_embedding(text)
        
        classes = LangchainPgEmbedding.objects.order_by(
            CosineDistance('embedding', embedding)
        )[:5]

        processed_classes = []
        for class1 in classes:
            course_name = class1.cmetadata['course_name']
            document = class1.document
            if document.startswith(course_name):
                description_without_course_name = document[len(course_name):].strip()
            else:
                description_without_course_name = document
            processed_classes.append({
                'course_name': course_name,
                'description_without_course_name': description_without_course_name
            })

        context = {
            'text': text, 
            'most_similar': processed_classes
        }

        
        return render(request, 'results.html', context)
    
    embeddings = LangchainPgEmbedding.objects.all()
    context= {'embeddings': embeddings}
    return render(request, 'index.html', context)


