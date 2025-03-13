import os
import random
from faker import Faker
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, Category, ProductImage, Review
from django.contrib.auth import get_user_model
from django.conf import settings
import json

KSH_TO_USD_RATE = 0.00771
SCRAPE_URL = os.getenv('SCRAPE_URL')
fake = Faker()
User = get_user_model()
USER_FILE = "users.json"


class Command(BaseCommand):
    help = "Scrape products and save them to the database."

    def generate_fake_users(self, num_users=10):
        """Generate and save fake users to the database and JSON file."""
        user_data_list = []
        created_users = []

        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()

            user = User.objects.create_user(username=username, email=email, password=password)
            created_users.append(user)

            user_data_list.append({
                "username": username,
                "email": email,
                "password": password
            })

            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        with open(USER_FILE, "w", encoding="utf-8") as file:
            json.dump(user_data_list, file, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Saved {num_users} users to {USER_FILE}"))
        return created_users

    def load_users(self):
        """Load users from JSON, create them if they don't exist."""
        try:
            with open(USER_FILE, "r", encoding="utf-8") as file:
                user_data_list = json.load(file)
            users = [User.objects.get_or_create(username=data["username"], defaults={"email": data["email"]})[
                0] for data in user_data_list]
        except (FileNotFoundError, json.JSONDecodeError):
            users = self.generate_fake_users()
        return users


    def convert_ksh_to_usd(self, price_str):
        """Convert KSH price string to USD float."""
        try:
            price_numeric = float("".join(filter(str.isdigit, price_str)))
            return round(price_numeric * KSH_TO_USD_RATE, 2)
        except ValueError:
            return None

    def generate_unique_slug(self, name):
        """Generate a unique slug by appending a number if needed."""
        base_slug = slugify(name) if name else "no-title"
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def extract_reviews(self, soup):
        """Extract reviews from the product page."""
        review_section = soup.select("div.rev")

        reviews = [
            {
                "rating": random.randint(1, 5),
                "comment": fake.sentence(),
            }
            for _ in range(random.randint(1, 5))
        ]
        return reviews

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            image_name = image_url.split("/")[-1]
            image_name = f'{image_name.split("?")[1]}.jpg'
            save_dir = os.path.join(settings.MEDIA_ROOT, "products")

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            save_path = os.path.join(save_dir, image_name)

            base_name, ext = os.path.splitext(image_name)
            counter = 1
            while os.path.exists(save_path):
                save_path = os.path.join(save_dir, f"{base_name}_{chr(96+counter)}{ext}")
                counter += 1

            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            self.stdout.write(self.style.SUCCESS(f"Image saved to {save_path}"))
            return save_path

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error downloading the image: {e}"))
            return None

    def extract_product_details(self, url):
        try:
            response = requests.get(f'{SCRAPE_URL}/{url}')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            description_div = soup.find("div", class_="markup -mhm -pvl -oxa -sc")
            description = description_div.get_text(strip=True) if description_div else "Description not found"
            image_urls = []
            image_carousel = soup.find("div", class_="crs")
            if image_carousel:
                image_items = image_carousel.find_all("img")
                for img_tag in image_items:
                    img_url = img_tag.get('data-src')
                    if img_url:
                        image_urls.append(img_url)

            product_details = {
                "description": description,
                "images": image_urls
            }

            return product_details

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching the product page: {e}"))
            return {"description": "Error fetching description", "specifications": {}, "images": []}

    def scrape_products_from_page(self, url):
        # sourcery skip: merge-dict-assign, move-assign-in-block
        """Scrape a single page of products."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            products = []
            for product in soup.select("article.prd"):
                product_data = {}

                # Extract product name
                name_tag = product.find("h3", class_="name")
                title = name_tag.text.strip() if name_tag else None

                if not title:
                    self.stderr.write(self.style.WARNING("Skipped a product with no title."))
                    continue

                product_data["title"] = title
                product_data["slug"] = self.generate_unique_slug(title)

                # Extract price
                price_tag = product.find("div", class_="prc")
                price_ksh = price_tag.text.strip() if price_tag else "0"
                product_data["price_ksh"] = price_ksh
                product_data["price"] = self.convert_ksh_to_usd(price_ksh)

                img_tag = product.find("img", class_="img")
                if img_tag and img_tag.get("data-src"):
                    image_url = img_tag["data-src"]
                    if image_url:
                        image = self.download_image(image_url)
                        product_data["image"] = image
                    else:
                        print('Product image not found')
                else:
                    product_data["image"] = None

                # Extract product details
                a_tag = product.find("a", class_="core")
                if a_tag:
                    product_data["sku"] = f"SKU-{random.randint(1000, 9999)}"
                    product_data["brand"] = a_tag.get("data-ga4-item_brand", "Unknown")
                    product_data["category"] = a_tag.get("data-ga4-item_category", "Uncategorized")
                    href = a_tag.get("href")

                    if href:
                        product_details = self.extract_product_details(href)
                        product_data["description"] = product_details["description"]
                        images_urls = product_details["images"]
                        product_data["images"] = [
                            self.download_image(i) for i in images_urls if self.download_image(i)
                        ]
                    else:
                        product_data["description"] = "No description available"
                        product_data["specifications"] = {}
                        product_data["images"] = []

                product_data["stock"] = random.randint(1, 100)
                product_data["reviews"] = self.extract_reviews(soup)
                products.append(product_data)

            next_page_tag = soup.find("a", {"aria-label": "Next"})
            next_page_url = next_page_tag["href"] if next_page_tag else None

            return products, next_page_url

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to scrape page: {e}"))
            return [], None

    def save_products_to_db(self, products):
        """Save scraped products to the database with unique slugs."""
        users = self.load_users()
        for product_data in products:
            category_name = product_data.get("category", "Uncategorized")
            category, _ = Category.objects.get_or_create(name=category_name)

            # Generate a unique slug
            unique_slug = self.generate_unique_slug(product_data["title"])
            
            downloaded_images = product_data.get("images", [])
            main_image = downloaded_images[0] if downloaded_images else "products/placeholder.jpg"

            # Ensure stock and price are valid
            stock = product_data.get("stock", random.randint(1, 100))
            price = product_data.get("price", 0.00)

            product, created = Product.objects.get_or_create(
                slug=unique_slug,
                defaults={
                    "name": product_data["title"],
                    "description": product_data["description"],
                    "price": price,
                    "category": category,
                    "stock": stock,
                    "image": main_image, 
                },
            )

            if created:

                self.stdout.write(self.style.SUCCESS(f"Added: {product.name}"))
                
                for img_path in downloaded_images[1:]:
                    ProductImage.objects.create(product=product, image=img_path)
                
                for review_data in product_data["reviews"]:
                    Review.objects.create(
                        user=random.choice(users),
                        product=product,
                        rating=review_data["rating"],
                        comment=review_data["comment"],
                    )
                self.stdout.write(self.style.SUCCESS(
                    f"Added {len(product_data['reviews'])} reviews for {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped duplicate: {product.name}"))

    def scrape_all_products(self, base_url):
        """Scrape multiple pages of products."""
        all_products = []
        next_page_url = base_url

        while next_page_url:
            self.stdout.write(f"Scraping page: {next_page_url}")
            products, next_page_url = self.scrape_products_from_page(next_page_url)
            all_products.extend(products)

            if next_page_url and not next_page_url.startswith("http"):
                next_page_url = f"{SCRAPE_URL.rstrip('/')}/{next_page_url.lstrip('/')}"

        return all_products

    def handle(self, *args, **kwargs):
        self.load_users()
        url = os.getenv('SCRAPE_URL_PAGE')
        start_url = f"{url}{random.randint(1, 10)}#catalog-listing"

        all_product_data = self.scrape_all_products(start_url)

        self.save_products_to_db(all_product_data)

        self.stdout.write(self.style.SUCCESS(f"Scraping complete! {len(all_product_data)} products added."))
