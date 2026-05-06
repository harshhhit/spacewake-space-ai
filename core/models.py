from django.db import models
import os




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# A callable to generate the dynamic upload path
def document_upload_path(instance, filename):
    # This will create a path like 'documents/category_name/document_title/filename.ext'
    category_name = instance.category.name.replace(" ", "_")
    document_title = instance.title.replace(" ", "_")
    return os.path.join('documents', category_name, document_title, filename)


class Document(models.Model):
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    description = models.TextField(blank=True)
    
    # Use the callable here
    file = models.FileField(upload_to=document_upload_path)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def file_url(self):
        return self.file.url


class PageLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
