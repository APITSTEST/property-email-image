from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import feedparser
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/email-image')
def email_image():
    rss_url = request.args.get('rss')
    if not rss_url:
        return "Missing RSS feed URL", 400

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    entries = feed.entries[:3]

    # Create base image
    img_width = 920
    img_height = 400
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)

    # Colors and fonts
    orange = (255, 149, 0)  # #FF9500
    draw.rectangle([0, 0, img_width - 1, img_height - 1], outline=orange, width=4)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        bold_font = ImageFont.truetype("arialbd.ttf", 16)
        button_font = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font = ImageFont.load_default()
        bold_font = font
        button_font = font

    for i, entry in enumerate(entries):
        x = i * 300 + 10
        center_x = x + 140  # Half of property card width (280)

        # Property image
        image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
        try:
            response = requests.get(image_url)
            prop_img = Image.open(BytesIO(response.content)).resize((280, 160))
            image.paste(prop_img, (x, 10))
        except:
            draw.text((x + 10, 10), "Image not available", fill="gray", font=font)

        # Property details
        title = entry.title
        description = entry.get("description", "")[:50] + "..." if len(entry.get("description", "")) > 50 else entry.get("description", "")
        price = entry.get("category", "")

        # Centered text helpers
        def draw_centered_text(text, y, font_used, color):
            w, h = draw.textsize(text, font=font_used)
            draw.text((center_x - w // 2, y), text, font=font_used, fill=color)

        draw_centered_text(title, 180, bold_font, "black")
        draw_centered_text(description, 200, font, "black")  # Beds/Baths now black
        draw_centered_text(f"Price: {price}", 220, bold_font, orange)  # Bold and orange

    # View More Button
    button_text = "View More Properties"
    button_width = 300
    button_height = 40
    button_x = (img_width - button_width) // 2
    button_y = img_height - 60

    draw.rectangle(
        [button_x, button_y, button_x + button_width, button_y + button_height],
        fill=orange
    )
    w, h = draw.textsize(button_text, font=button_font)
    draw.text(
        (button_x + (button_width - w) // 2, button_y + 10),
        button_text,
        font=button_font,
        fill="white"
    )

    # Return image
    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT or fallback
    app.run(host='0.0.0.0', port=port)
