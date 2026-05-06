from core.models import Document, DictionaryEntry

def list_documents():
    return Document.objects.all()

def search_dictionary(term):
    return DictionaryEntry.objects.filter(term__icontains=term)
