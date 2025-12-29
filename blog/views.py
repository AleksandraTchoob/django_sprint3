from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


# Create your views here.
def index(request):
    """Лента записей."""
    current_time = timezone.now()

    posts = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).select_related(
        'category', 'location', 'author'
    ).order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    """Страница отдельного поста."""
    current_time = timezone.now()

    post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).select_related('category', 'location', 'author'),
        id=id
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница с постами определенной категории."""
    current_time = timezone.now()

    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    posts = Post.objects.filter(
        category=category,
        pub_date__lte=current_time,
        is_published=True
    ).select_related('location', 'author').order_by('-pub_date')

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': posts
    })
