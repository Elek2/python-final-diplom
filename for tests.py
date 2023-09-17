from slugify import slugify as pyslug
from django.utils.text import slugify as djangoslug


text = "мама Мыла раму. mom Clean,,?? windo"

python_slug = pyslug(text)
django_slug = djangoslug(text)

print(f"python_slug = {python_slug}")
print(f"django_slug = {django_slug}")