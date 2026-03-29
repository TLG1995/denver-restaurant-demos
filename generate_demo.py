#!/usr/bin/env python3
"""
Restaurant Demo Website Generator
Reads a JSON config and produces a complete HTML demo site.
Usage: python3 generate_demo.py config.json
"""

import json
import sys
import os
import shutil

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | {cuisine_label} - {city}</title>
    <meta name="description" content="{name} serves {cuisine_lower} cuisine in {city}. {tagline}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {color1};
            --primary-dark: {color2};
            --gold: {accent};
            --cream: #FFF8F0;
            --dark: #1A1A1A;
            --warm-gray: #4A4A4A;
            --light-gray: #F5F0EB;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; color: var(--dark); background: var(--cream); }}

        .hero {{
            min-height: 100vh;
            background: linear-gradient(135deg, rgba(26,26,26,0.75), {color2_alpha}),
                        url('{hero_img}') center/cover no-repeat;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; padding: 2rem; position: relative;
        }}
        .hero-content {{ position: relative; z-index: 1; max-width: 700px; }}
        .hero-badge {{
            display: inline-block; padding: 0.5rem 1.5rem; border: 1px solid var(--gold);
            color: var(--gold); font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase;
            margin-bottom: 2rem; border-radius: 2px;
        }}
        .hero h1 {{
            font-family: 'Playfair Display', serif; font-size: clamp(3rem, 8vw, 5.5rem);
            color: white; margin-bottom: 1rem; line-height: 1.1;
        }}
        .hero-tagline {{ font-size: 1.2rem; color: rgba(255,255,255,0.85); font-weight: 300; margin-bottom: 2.5rem; line-height: 1.6; }}
        .hero-stars {{ color: var(--gold); font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .hero-rating {{ color: rgba(255,255,255,0.7); font-size: 0.9rem; }}
        .hero-cta {{ display: inline-flex; gap: 1rem; margin-top: 2rem; flex-wrap: wrap; justify-content: center; }}

        .btn {{
            padding: 0.9rem 2.2rem; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px;
            text-transform: uppercase; text-decoration: none; border-radius: 3px; transition: all 0.3s; cursor: pointer; border: none;
        }}
        .btn-primary {{ background: var(--gold); color: var(--dark); }}
        .btn-primary:hover {{ filter: brightness(1.1); transform: translateY(-2px); }}
        .btn-outline {{ background: transparent; color: white; border: 1px solid rgba(255,255,255,0.4); }}
        .btn-outline:hover {{ border-color: white; background: rgba(255,255,255,0.1); }}

        nav {{
            position: fixed; top: 0; width: 100%; padding: 1.2rem 2rem;
            display: flex; justify-content: space-between; align-items: center; z-index: 100; transition: all 0.3s;
        }}
        nav.scrolled {{ background: rgba(26,26,26,0.95); backdrop-filter: blur(10px); padding: 0.8rem 2rem; box-shadow: 0 2px 20px rgba(0,0,0,0.3); }}
        .nav-logo {{ font-family: 'Playfair Display', serif; color: white; font-size: 1.5rem; text-decoration: none; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; transition: color 0.3s; }}
        .nav-links a:hover {{ color: var(--gold); }}

        section {{ padding: 5rem 2rem; }}
        .section-header {{ text-align: center; margin-bottom: 3.5rem; }}
        .section-header h2 {{ font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .section-header .divider {{ width: 60px; height: 2px; background: var(--gold); margin: 1rem auto; }}
        .section-header p {{ color: var(--warm-gray); font-weight: 300; max-width: 500px; margin: 0 auto; line-height: 1.7; }}

        .about {{ background: white; }}
        .about-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
        .about-image {{ border-radius: 8px; height: 400px; overflow: hidden; }}
        .about-image img {{ width: 100%; height: 100%; object-fit: cover; filter: brightness(1.05) contrast(1.1) saturate(1.15); }}
        .about-text h3 {{ font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 1.2rem; }}
        .about-text p {{ color: var(--warm-gray); line-height: 1.8; margin-bottom: 1rem; }}

        .gallery {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; max-width: 1000px; margin: 0 auto 3rem; border-radius: 8px; overflow: hidden; }}
        .gallery img {{ width: 100%; height: 250px; object-fit: cover; transition: transform 0.4s ease; filter: brightness(1.05) contrast(1.1) saturate(1.15); }}
        .gallery img:hover {{ transform: scale(1.05); }}

        .menu {{ background: var(--cream); }}
        .menu-grid {{ max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        .menu-category {{ background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 15px rgba(0,0,0,0.05); }}
        .menu-category h3 {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; margin-bottom: 1.5rem; padding-bottom: 0.75rem; border-bottom: 2px solid var(--gold); }}
        .menu-item {{ display: flex; justify-content: space-between; align-items: baseline; padding: 0.6rem 0; border-bottom: 1px solid var(--light-gray); }}
        .menu-item:last-child {{ border-bottom: none; }}
        .menu-item-name {{ font-weight: 500; font-size: 0.95rem; }}
        .menu-item-price {{ color: var(--primary); font-weight: 600; font-size: 0.9rem; white-space: nowrap; margin-left: 1rem; }}
        .menu-item-desc {{ font-size: 0.8rem; color: var(--warm-gray); font-weight: 300; margin-top: 0.2rem; }}

        .reviews {{ background: white; }}
        .reviews-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }}
        .review-card {{ background: var(--cream); padding: 2rem; border-radius: 8px; position: relative; }}
        .review-card::before {{ content: '\\201C'; font-family: 'Playfair Display', serif; font-size: 4rem; color: var(--gold); position: absolute; top: 0.5rem; left: 1rem; line-height: 1; opacity: 0.5; }}
        .review-stars {{ color: var(--gold); margin-bottom: 0.75rem; margin-top: 1rem; }}
        .review-text {{ font-size: 0.9rem; line-height: 1.7; color: var(--warm-gray); font-style: italic; margin-bottom: 1rem; }}
        .review-author {{ font-weight: 600; font-size: 0.85rem; }}

        .order-cta {{ background: linear-gradient(135deg, var(--primary), var(--primary-dark)); text-align: center; padding: 4rem 2rem; }}
        .order-cta h2 {{ font-family: 'Playfair Display', serif; color: white; font-size: 2.5rem; margin-bottom: 1rem; }}
        .order-cta p {{ color: rgba(255,255,255,0.8); margin-bottom: 2rem; font-weight: 300; }}

        .info {{ background: var(--dark); color: white; }}
        .info-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3rem; }}
        .info .section-header h2 {{ color: white; }}
        .info-block h3 {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; margin-bottom: 1.5rem; color: var(--gold); }}
        .info-block p, .info-block li {{ color: rgba(255,255,255,0.8); line-height: 2; font-weight: 300; font-size: 0.95rem; }}
        .info-block ul {{ list-style: none; }}
        .info-block a {{ color: var(--gold); text-decoration: none; }}
        .info-block a:hover {{ text-decoration: underline; }}
        .day-hours {{ display: flex; justify-content: space-between; }}
        .day-name {{ font-weight: 500; }}

        footer {{ background: #111; color: rgba(255,255,255,0.5); text-align: center; padding: 2rem; font-size: 0.8rem; }}

        @media (max-width: 768px) {{
            .about-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
            .menu-grid {{ grid-template-columns: 1fr; }}
            .reviews-grid {{ grid-template-columns: 1fr; }}
            .info-grid {{ grid-template-columns: 1fr; }}
            .nav-links {{ display: none; }}
            .about-image {{ height: 250px; }}
            .gallery {{ grid-template-columns: 1fr; }}
            .gallery img {{ height: 200px; }}
        }}
    </style>
</head>
<body>

<nav id="navbar">
    <a href="#" class="nav-logo">{name}</a>
    <ul class="nav-links">
        <li><a href="#about">Our Story</a></li>
        <li><a href="#menu">Menu</a></li>
        <li><a href="#reviews">Reviews</a></li>
        <li><a href="#info">Visit Us</a></li>
        <li><a href="tel:{phone_raw}" class="btn btn-primary" style="padding:0.5rem 1.2rem; font-size:0.75rem;">Order Now</a></li>
    </ul>
</nav>

<section class="hero">
    <div class="hero-content">
        <div class="hero-badge">{badge_text}</div>
        <h1>{name}</h1>
        <p class="hero-tagline">{tagline}</p>
        <div class="hero-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="hero-rating">{rating} stars &middot; {reviews}+ Google Reviews</p>
        <div class="hero-cta">
            <a href="#menu" class="btn btn-primary">View Menu</a>
            <a href="tel:{phone_raw}" class="btn btn-outline">Call to Order</a>
        </div>
    </div>
</section>

<section class="about" id="about">
    <div class="about-grid">
        <div class="about-image">
            <img src="{about_img}" alt="Food at {name}" loading="lazy">
        </div>
        <div class="about-text">
            <h3>{about_title}</h3>
            {about_paragraphs}
        </div>
    </div>
</section>

<section class="menu" id="menu">
    <div class="section-header">
        <h2>Our Menu</h2>
        <div class="divider"></div>
        <p>{menu_subtitle}</p>
    </div>
    {gallery_html}
    {menu_html}
</section>

<section class="reviews" id="reviews">
    <div class="section-header">
        <h2>What People Say</h2>
        <div class="divider"></div>
    </div>
    <div class="reviews-grid">
        {reviews_html}
    </div>
</section>

<section class="order-cta">
    <h2>Ready to Eat?</h2>
    <p>Call ahead for takeout or stop by for dine-in.</p>
    <a href="tel:{phone_raw}" class="btn btn-primary" style="font-size:1rem; padding:1rem 3rem;">Call {phone}</a>
</section>

<section class="info" id="info">
    <div class="section-header">
        <h2>Visit {name}</h2>
        <div class="divider"></div>
    </div>
    <div class="info-grid">
        <div class="info-block">
            <h3>Hours</h3>
            <ul>{hours_html}</ul>
        </div>
        <div class="info-block">
            <h3>Location</h3>
            <p>{address}</p>
            <p style="margin-top:1rem"><a href="https://maps.google.com/?q={address_encoded}" target="_blank">Get Directions &rarr;</a></p>
        </div>
        <div class="info-block">
            <h3>Contact</h3>
            <p>Phone: <a href="tel:{phone_raw}">{phone}</a></p>
            <p style="margin-top:1.5rem; font-size:0.85rem; color: rgba(255,255,255,0.5);">{services}</p>
        </div>
    </div>
</section>

<footer>
    <p>&copy; 2026 {name} | {address} | {phone}</p>
</footer>

<script>
    window.addEventListener('scroll', () => {{
        document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
    }});
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
        anchor.addEventListener('click', function(e) {{
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
    }});
</script>
</body>
</html>"""


def generate_menu_html(categories):
    html = '<div class="menu-grid">\n'
    for cat in categories:
        html += f'    <div class="menu-category">\n        <h3>{cat["name"]}</h3>\n'
        for item in cat["items"]:
            desc_html = f'\n                <div class="menu-item-desc">{item["desc"]}</div>' if item.get("desc") else ""
            html += f'        <div class="menu-item">\n            <div>\n                <div class="menu-item-name">{item["name"]}</div>{desc_html}\n            </div>\n            <span class="menu-item-price">{item.get("price", "")}</span>\n        </div>\n'
        html += '    </div>\n'
    html += '</div>'
    return html


def generate_reviews_html(reviews):
    html = ""
    for r in reviews:
        html += f"""        <div class="review-card">
            <div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <p class="review-text">{r["text"]}</p>
            <p class="review-author">{r.get("author", "Google Reviewer")}</p>
        </div>\n"""
    return html


def generate_hours_html(hours):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    html = ""
    for day in days:
        h = hours.get(day, "Closed")
        html += f'                <li class="day-hours"><span class="day-name">{day}</span> <span>{h}</span></li>\n'
    return html


def generate_gallery_html(images):
    if not images:
        return ""
    html = '    <div class="gallery">\n'
    for img in images[:3]:
        html += f'        <img src="{img["src"]}" alt="{img.get("alt", "Food photo")}" loading="lazy">\n'
    html += '    </div>'
    return html


def generate_about_paragraphs(paragraphs):
    return "\n".join(f"            <p>{p}</p>" for p in paragraphs)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_demo.py config.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    slug = config["name"].lower().replace(" ", "-").replace("'", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), slug)
    os.makedirs(os.path.join(out_dir, "img"), exist_ok=True)

    phone_raw = config["phone"].replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
    address_encoded = config["address"].replace(" ", "+").replace(",", "%2C")

    html = TEMPLATE.format(
        name=config["name"],
        cuisine_label=config.get("cuisine_label", config.get("cuisine", "Restaurant")),
        cuisine_lower=config.get("cuisine", "").lower(),
        city=config.get("city", "Denver, CO"),
        tagline=config.get("tagline", f"Authentic {config.get('cuisine', '')} cuisine."),
        color1=config.get("color1", "#C4402F"),
        color2=config.get("color2", "#8B1A1A"),
        color2_alpha=config.get("color2_alpha", "rgba(139,26,26,0.65)"),
        accent=config.get("accent", "#D4A853"),
        hero_img=config.get("hero_img", "img/hero.jpg"),
        about_img=config.get("about_img", "img/food1.jpg"),
        badge_text=config.get("badge_text", f"Est. {config.get('city', 'Denver, CO')}"),
        rating=config.get("rating", "4.9"),
        reviews=config.get("reviews", "100"),
        phone=config["phone"],
        phone_raw=phone_raw,
        about_title=config.get("about_title", f"Welcome to {config['name']}"),
        about_paragraphs=generate_about_paragraphs(config.get("about_paragraphs", [
            f"At {config['name']}, we bring authentic flavors to Denver.",
            "Fresh ingredients, family recipes, and a passion for great food.",
        ])),
        menu_subtitle=config.get("menu_subtitle", "Fresh, authentic flavors made from scratch daily"),
        gallery_html=generate_gallery_html(config.get("gallery_images", [])),
        menu_html=generate_menu_html(config.get("menu_categories", [])),
        reviews_html=generate_reviews_html(config.get("reviews_list", [])),
        hours_html=generate_hours_html(config.get("hours", {})),
        address=config["address"],
        address_encoded=address_encoded,
        services=config.get("services", "Dine-in · Takeout · Delivery"),
    )

    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w") as f:
        f.write(html)

    print(f"Generated: {out_path}")
    print(f"Directory: {out_dir}")
    print(f"Add photos to: {os.path.join(out_dir, 'img/')}")
    return out_dir


if __name__ == "__main__":
    main()
