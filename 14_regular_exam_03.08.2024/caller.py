import os
import django
from django.db.models import Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article


# Create queries within functions
def get_authors(search_name=None, search_email=None):
    authors = None
    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(
            full_name__icontains=search_name,
            email__icontains=search_email
        ).order_by(
            '-full_name'
        )

    if search_name is None:
        authors = Author.objects.filter(
            email__icontains=search_email
        ).order_by(
            '-full_name'
        )

    if search_email is None:
        authors = Author.objects.filter(
            full_name__icontains=search_name
        ).order_by(
            '-full_name'
        )

    if authors is None:
        return ""

    result = [
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}" for a in authors
    ]
    return '\n'.join(result)


def get_top_publisher():
    top = Author.objects.get_authors_by_article_count().first()

    if not top or top.articles_count == 0:
        return ""
    return f"Top Author: {top.full_name} with {top.articles_count} published articles."


def get_top_reviewer():
    top = Author.objects.annotate(
        reviews_count=Count('author_reviews')
    ).order_by(
        '-reviews_count',
        'email'
    ).first()

    if not top or top.reviews_count == 0:
        return ""
    return f"Top Reviewer: {top.full_name} with {top.reviews_count} published reviews."


# -------------------------------------------------------------------------

def get_latest_article():
    latest = Article.objects.prefetch_related(
        'authors', 'article_reviews'
    ).annotate(
        num_reviews=Count('article_reviews')
    ).annotate(
        avg_reviews_rating=Avg('article_reviews__rating')
    ).order_by(
        '-id'
    ).first()

    if not latest:
        return ""

    authors = latest.authors.all().order_by('full_name')

    return (f"The latest article is: {latest.title}. "
            f"Authors: {', '.join([a.full_name for a in authors])}. "
            f"Reviewed: {latest.num_reviews} times. "
            f"Average Rating: {0 if latest.avg_reviews_rating is None else latest.avg_reviews_rating:.2f}.")


# I have to check this and previous submissions
def get_top_rated_article():
    # Prefetch related reviews and calculate the correct average rating and review count
    top = Article.objects.prefetch_related('article_reviews') \
        .annotate(
            avg_rating=Avg('article_reviews__rating'),
            num_reviews=Count('article_reviews')
        ).filter(
            avg_rating__isnull=False
        ).order_by(
            '-avg_rating',
            'title'
        ).first()

    if not top or top.num_reviews == 0:
        return ''

    # Now, the average rating reflects the actual average of all reviews.
    return (f"The top-rated article is: {top.title}, "
            f"with an average rating of {top.avg_rating:.2f}, "
            f"reviewed {top.num_reviews} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    target = Author.objects.annotate(
        reviews_count=Count('author_reviews')
    ).filter(
        email=email
    ).first()

    if not target:
        return "No authors banned."

    reviews = target.author_reviews.all()
    reviews_count = reviews.count()

    target.is_banned = True
    target.save()

    for r in reviews:
        r.delete()

    return f"Author: {target.full_name} is banned! {reviews_count} reviews deleted."

