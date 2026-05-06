import os
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('documents/', views.view_documents, name='view_documents'),
    path('add_document/', views.add_document, name='add_document'),
    path('pages/', views.manage_page_links, name='manage_page_links'),
    path('pages/<int:page_id>/', views.render_page_link, name='render_page_link'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

# This is the line that needs to be outside the list but
# concatenated to the list.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
