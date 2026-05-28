import decimal
import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files import File
from store.models import Category, Product

# ── Local image base path (relative to manage.py) ────────────────────────────
LOCAL_IMG_DIR = os.path.join('static', 'images', 'products')

# ── Unsplash CDN fallback for products without a local image ─────────────────
UNSPLASH_URLS = {
    'coconut,tropical':       'https://images.unsplash.com/photo-1589883661923-6476cb0ae9f2?w=500&q=80',
    'banana,yellow,fruit':    'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80',
    'mango,fruit,yellow':     'https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80',
    'pineapple,fruit,tropical': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=500&q=80',
}


def load_local_image(filename):
    """Return (open file handle, filename) for a file in LOCAL_IMG_DIR, or (None, None)."""
    path = os.path.join(LOCAL_IMG_DIR, filename)
    if os.path.exists(path):
        return open(path, 'rb'), filename
    return None, None


def fetch_remote_image(keyword):
    """Download image from Unsplash CDN. Returns ContentFile or None."""
    url = UNSPLASH_URLS.get(keyword)
    if not url:
        url = 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=500&q=80'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return ContentFile(resp.content)
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = 'Seeds categories and products; attaches local or Unsplash images.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--images-only',
            action='store_true',
            help='Only re-fetch/update images without creating new records.',
        )

    def handle(self, *args, **options):
        images_only = options.get('images_only', False)
        mode = 'images-only' if images_only else 'full seed'
        self.stdout.write(f'Running seed_products ({mode})...')

        # ── Categories ────────────────────────────────────────────────────────
        categories_data = [
            {'name': 'Farm Fresh', 'slug': 'farm-fresh', 'image': 'kappa.jpg'},
            {'name': 'Fruits',     'slug': 'fruits',     'image': ''},
            {'name': 'Snacks',     'slug': 'snacks',     'image': 'snacks.jpg'},
            {'name': 'Spices',     'slug': 'spices',     'image': 'spices.jpg'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'  Created category: {cat.name}')

            # Attach category image
            if cat_data['image']:
                f, name = load_local_image(cat_data['image'])
                if f:
                    cat.image.save(name, File(f), save=True)
                    f.close()
                    self.stdout.write(f'  OK image: Category "{cat.name}" -> {name}')

            categories[cat_data['name']] = cat

        # ── Products ─────────────────────────────────────────────────────────
        # local_image: filename in static/images/products/ (None = use Unsplash)
        products_data = [
            # Farm Fresh
            {
                'category': 'Farm Fresh',
                'name': 'Raw Coconut',
                'slug': 'raw-coconut',
                'description': 'Freshly harvested coconuts from organic groves in Kerala. Ideal for cooking, making fresh coconut oil, or grated toppings.',
                'price': decimal.Decimal('45.00'),
                'unit': 'per piece',
                'stock': 120,
                'local_image': 'coconut.webp',
                'keyword': 'coconut,tropical',
            },
            {
                'category': 'Farm Fresh',
                'name': 'Tapioca / Kappa',
                'slug': 'tapioca-kappa',
                'description': 'Freshly dug organic tapioca roots, a staple carbohydrate in Kerala. Boil and serve with spicy fish curry or coconut chutney.',
                'price': decimal.Decimal('30.00'),
                'unit': 'per kg',
                'stock': 150,
                'local_image': 'kappa.jpg',
                'keyword': None,
            },
            {
                'category': 'Farm Fresh',
                'name': 'Jackfruit',
                'slug': 'jackfruit',
                'description': 'Large fresh jackfruit harvested at the peak of freshness. Sweet, fleshy, and highly versatile for traditional recipes.',
                'price': decimal.Decimal('80.00'),
                'unit': 'per kg',
                'stock': 25,
                'local_image': 'Jackfruit.jpg',
                'keyword': None,
            },
            {
                'category': 'Farm Fresh',
                'name': 'Curry Leaves',
                'slug': 'curry-leaves',
                'description': 'Extremely aromatic, fresh green curry leaves grown in backyard gardens. The ultimate seasoning for South Indian curries.',
                'price': decimal.Decimal('10.00'),
                'unit': 'per bunch',
                'stock': 200,
                'local_image': 'curryleaves.webp',
                'keyword': None,
            },

            # Fruits
            {
                'category': 'Fruits',
                'name': 'Nendran Banana',
                'slug': 'nendran-banana',
                'description': 'Sweet, ripe, golden Kerala Nendran bananas. Highly nutritious, delicious raw, or lightly caramelised in ghee.',
                'price': decimal.Decimal('60.00'),
                'unit': 'per dozen',
                'stock': 80,
                'local_image': None,
                'keyword': 'banana,yellow,fruit',
            },
            {
                'category': 'Fruits',
                'name': 'Mango',
                'slug': 'mango',
                'description': 'Locally sourced sweet mangoes (Priyoor or Alphonso varieties grown in Kerala gardens). Rich, pulpy, and delicious.',
                'price': decimal.Decimal('120.00'),
                'unit': 'per kg',
                'stock': 60,
                'local_image': None,
                'keyword': 'mango,fruit,yellow',
            },
            {
                'category': 'Fruits',
                'name': 'Pineapple',
                'slug': 'pineapple',
                'description': 'Sweet and tangy pineapples grown in the fertile soils of Vazhakulam, Kerala. Known for their unique sweetness.',
                'price': decimal.Decimal('50.00'),
                'unit': 'per piece',
                'stock': 90,
                'local_image': None,
                'keyword': 'pineapple,fruit,tropical',
            },

            # Snacks — all share snacks.jpg
            {
                'category': 'Snacks',
                'name': 'Banana Chips',
                'slug': 'banana-chips',
                'description': 'Crispy, thin slices of raw Nendran banana deep-fried in 100% pure coconut oil. The authentic taste of Kerala.',
                'price': decimal.Decimal('80.00'),
                'unit': 'per pack',
                'stock': 100,
                'local_image': 'snacks.jpg',
                'keyword': None,
            },
            {
                'category': 'Snacks',
                'name': 'Murukku',
                'slug': 'murukku',
                'description': 'Crunchy, spiral-shaped rice flour snack seasoned with sesame and cumin seeds. Perfectly roasted and savory.',
                'price': decimal.Decimal('60.00'),
                'unit': 'per pack',
                'stock': 150,
                'local_image': 'snacks.jpg',
                'keyword': None,
            },
            {
                'category': 'Snacks',
                'name': 'Achappam',
                'slug': 'achappam',
                'description': 'Traditional rose cookie snack. Extremely light, crispy, and sweet made from rice flour and coconut milk.',
                'price': decimal.Decimal('70.00'),
                'unit': 'per pack',
                'stock': 80,
                'local_image': 'snacks.jpg',
                'keyword': None,
            },
            {
                'category': 'Snacks',
                'name': 'Unniyappam',
                'slug': 'unniyappam',
                'description': 'Sweet, spongy, deep-fried fritters made of rice, jaggery, banana, and roasted coconut bits. A classic tea-time treat.',
                'price': decimal.Decimal('90.00'),
                'unit': 'per pack',
                'stock': 60,
                'local_image': 'snacks.jpg',
                'keyword': None,
            },

            # Spices — all share spices.jpg
            {
                'category': 'Spices',
                'name': 'Black Pepper',
                'slug': 'black-pepper',
                'description': 'Premium whole black peppercorns from the hills of Wayanad, Kerala. Rich in piperine and intensely aromatic.',
                'price': decimal.Decimal('200.00'),
                'unit': 'per 100g',
                'stock': 110,
                'local_image': 'spices.jpg',
                'keyword': None,
            },
            {
                'category': 'Spices',
                'name': 'Cardamom',
                'slug': 'cardamom',
                'description': 'Green cardamom pods sorted by size and color from Idukki plantations. Adds sweet, exotic spice flavor to tea and sweets.',
                'price': decimal.Decimal('250.00'),
                'unit': 'per 50g',
                'stock': 70,
                'local_image': 'spices.jpg',
                'keyword': None,
            },
            {
                'category': 'Spices',
                'name': 'Turmeric Powder',
                'slug': 'turmeric-powder',
                'description': 'Pure turmeric powder processed from premium high-curcumin turmeric roots grown in Kerala. Ground to perfection.',
                'price': decimal.Decimal('40.00'),
                'unit': 'per pack',
                'stock': 130,
                'local_image': 'spices.jpg',
                'keyword': None,
            },
        ]

        for p_data in products_data:
            slug = p_data['slug']
            try:
                prod = Product.objects.get(slug=slug)
                exists = True
            except Product.DoesNotExist:
                prod = None
                exists = False

            if images_only and not exists:
                self.stdout.write(f'  SKIP (not found): {slug}')
                continue

            if not exists:
                category_obj = categories[p_data['category']]
                prod = Product.objects.create(
                    category=category_obj,
                    name=p_data['name'],
                    slug=slug,
                    description=p_data['description'],
                    price=p_data['price'],
                    unit=p_data['unit'],
                    stock=p_data['stock'],
                    is_available=True,
                )
                self.stdout.write(f'  Created product: {prod.name}')

            # ── Attach image ─────────────────────────────────────────────────
            local_file = p_data.get('local_image')
            if local_file:
                # Use local image — always overwrite for correct assignment
                f, name = load_local_image(local_file)
                if f:
                    prod.image.save(name, File(f), save=True)
                    f.close()
                    self.stdout.write(f'  OK (local): {prod.name} -> {name}')
                else:
                    self.stdout.write(f'  WARN: local file not found: {local_file}')
            else:
                # Only download from Unsplash if the product has no image yet
                if not prod.image:
                    keyword = p_data.get('keyword', '')
                    img = fetch_remote_image(keyword)
                    if img:
                        prod.image.save(f'{slug}.jpg', img, save=True)
                        self.stdout.write(f'  OK (remote): {prod.name}')
                    else:
                        self.stdout.write(f'  WARN: remote fetch failed for {prod.name}')
                else:
                    self.stdout.write(f'  SKIP (has image): {prod.name}')

        self.stdout.write(self.style.SUCCESS('Done! All products and categories updated.'))
