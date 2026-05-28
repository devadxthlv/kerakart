# KeraKart 🌴
> **Fresh from Kerala's Farms to Your Door**

A full-stack ecommerce platform built with Python and Django for buying Kerala farm-fresh produce and traditional snacks. Built as the final project for the Full Stack Python Internship at Edure / IPSR.

![Django](https://img.shields.io/badge/Django-6.x-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

---

## Features

- **Product Catalog** — 14 products across 4 categories: Farm Fresh, Fruits, Snacks, and Spices
- **Category Filtering** — Browse by category using URL-based filtering
- **Shopping Cart** — Session-based cart with add, remove, and quantity management
- **User Auth** — Register, login, and logout using Django's built-in auth system
- **Admin Dashboard** — Full product and category management via Django's `/admin` panel
- **Premium Design** — Burnt Sienna palette, Cormorant Garant + DM Sans typography, Apple-inspired editorial layout
- **Animations** — Scroll-triggered fade-up animations, glassmorphism navbar on scroll, staggered card entrances
- **Responsive** — CSS Grid layout adapts to any screen size

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x + Django 6.x |
| Database | SQLite (development) |
| Frontend | HTML5, CSS3, Django Templates |
| Typography | Cormorant Garant + DM Sans (Google Fonts) |
| Images | Django ImageField + Pillow |
| Cart | Django Sessions |
| Admin | Django built-in `/admin` |

---

## Project Structure

```
Edure_final_project/
│
├── venv/                        # Python Virtual Environment (not committed)
├── .gitignore
├── .env.example                 # Environment variable template
├── requirements.txt
├── README.md
│
└── kerakart/                    # Django Project Root
    ├── manage.py
    │
    ├── kerakart/                # Project Config
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── store/                   # Store App — Catalog & Products
    │   ├── models.py            # Category, Product models
    │   ├── views.py             # home, product_list, product_detail
    │   ├── urls.py
    │   ├── admin.py
    │   └── management/
    │       └── commands/
    │           └── seed_products.py   # DB seeder with local images
    │
    ├── cart/                    # Cart App — Session Cart
    │   ├── views.py             # add, remove, cart detail
    │   ├── urls.py
    │   └── context_processors.py
    │
    ├── accounts/                # Accounts App — User Auth
    │   ├── views.py             # register, login, logout
    │   ├── urls.py
    │   └── forms.py
    │
    ├── templates/               # HTML Templates
    │   ├── base.html            # Main layout (navbar, footer)
    │   ├── store/
    │   │   ├── home.html
    │   │   ├── products.html
    │   │   └── product_detail.html
    │   ├── cart/
    │   │   └── cart.html
    │   └── accounts/
    │       ├── login.html
    │       └── register.html
    │
    └── static/                  # Static Assets
        ├── css/
        │   └── style.css        # Full custom design system
        └── images/
            ├── hero-kerala.jpg
            └── products/        # Local product images
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/kerakart.git
cd kerakart
```

### 2. Create & activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations & seed the database
```bash
cd kerakart
python manage.py migrate
python manage.py seed_products
```

### 5. Create a superuser (for /admin access)
```bash
python manage.py createsuperuser
# Or use the pre-seeded admin: username=admin, password=admin123
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — admin panel at **http://127.0.0.1:8000/admin/**

---

## Seed Data

The `seed_products` management command populates 14 organic products across 4 categories:

| Category | Products |
|---|---|
| Farm Fresh | Raw Coconut, Tapioca/Kappa, Jackfruit, Curry Leaves |
| Fruits | Nendran Banana, Mango, Pineapple |
| Snacks | Banana Chips, Murukku, Achappam, Unniyappam |
| Spices | Black Pepper, Cardamom, Turmeric Powder |

To re-fetch images only (without recreating products):
```bash
python manage.py seed_products --images-only
```

---

## Design System

| Token | Value |
|---|---|
| Background | `#F5F5DC` (warm cream) |
| Primary / CTA | `#E35336` (burnt sienna) |
| Dark text | `#2C1810` |
| Muted text | `#8B6355` |
| Border | `#E8D5C4` |
| Heading font | Cormorant Garant (serif) |
| Body font | DM Sans (sans-serif) |
| Border radius | `2px` (sharp, editorial) |

---

## Author

Built by **Devadath** as a final project for the Full Stack Python Internship — **Edure**.
