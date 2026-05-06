from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .forms import DocumentForm, PageLinkForm, SignupForm
from .models import Category, Document, PageLink

DEFAULT_CATEGORIES = [
    "aws",
    "system-design",
    "random-topic",
    "memo",
    "revision",
    "deep-dive",
]


def ensure_default_categories():
    for category_name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=category_name)


def home(request):
    documents = Document.objects.select_related("category").order_by("-created_at")
    page_links = PageLink.objects.order_by("-created_at")
    return render(
        request,
        "home.html",
        {
            "documents": documents[:4],
            "page_links": page_links[:4],
            "total_documents": documents.count(),
            "total_pages": page_links.count(),
            "total_categories": Category.objects.count(),
        },
    )


def add_document(request):
    ensure_default_categories()

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.section = document.category.name
            document.filename = document.file.name
            document.save()
            return redirect("view_documents")
    else:
        form = DocumentForm()

    categories = Category.objects.order_by("name")
    documents = Document.objects.select_related("category").order_by("-created_at")

    return render(
        request,
        "add_document.html",
        {
            "form": form,
            "categories": categories,
            "documents": documents,
        },
    )


def view_documents(request):
    documents = Document.objects.select_related("category").order_by("-created_at")
    return render(request, "view_document.html", {"documents": documents})


def manage_page_links(request):
    if request.method == "POST":
        form = PageLinkForm(request.POST)
        if form.is_valid():
            page_link = form.save()
            return redirect("render_page_link", page_id=page_link.id)
    else:
        form = PageLinkForm()

    page_links = PageLink.objects.all()
    return render(
        request,
        "page_links.html",
        {
            "form": form,
            "page_links": page_links,
        },
    )


def render_page_link(request, page_id):
    page_link = get_object_or_404(PageLink, id=page_id)
    return render(
        request,
        "render_page_link.html",
        {
            "page_link": page_link,
        },
    )


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})
