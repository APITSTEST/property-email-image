from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import feedparser
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/email-image')
def email_image():
    rss_url = request.args.get('rss')
    if not rss_url:
        return "Missing RSS feed URL", 400

    feed = feedparser.parse(rss_url)
    entries = feed.entries[:3]

    img_width = 920
    img_height = 460
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)

    orange = (255, 149, 0)  # #FF9500
    draw.rectangle([0, 0, img_width - 1, img_height - 1], outline=orange, width=4)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        bold_font = ImageFont.truetype("arialbd.ttf", 16)
        button_font = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font = ImageFont.load_default()
        bold_font = font
        button_font = font

    def draw_centered_text(text, y, font_used, color, center_x):
        bbox = draw.textbbox((0, 0), text, font=font_used)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w // 2, y), text, font=font_used, fill=color)

    for i, entry in enumerate(entries):
        x = i * 300 + 10
        center_x = x + 140

        image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
        try:
            response = requests.get(image_url)
            prop_img = Image.open(BytesIO(response.content)).resize((280, 160))
            image.paste(prop_img, (x, 10))
        except:
            draw.text((x + 10, 10), "Image not available", fill="gray", font=font)

        title = entry.title
        description = entry.get("description", "")[:50] + "..." if len(entry.get("description", "")) > 50 else entry.get("description", "")
        price = entry.get("category", "")
        link = entry.link

        draw_centered_text(title, 180, bold_font, "black", center_x)
        draw_centered_text(description, 200, font, "black", center_x)
        draw_centered_text(f"Price: {price}", 220, bold_font, orange, center_x)

        # Draw rounded "View Property" button under each listing
        button_text = "View Property"
        button_width = 180
        button_height = 36
        button_x = center_x - button_width // 2
        button_y = 250

        # Draw rounded rectangle (rounded corners)
        radius = 10
        draw.rounded_rectangle(
            [button_x, button_y, button_x + button_width, button_y + button_height],
            radius=radius,
            fill=orange
        )

        # Draw bold white button text centered
        bbox = draw.textbbox((0, 0), button_text, font=button_font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            (center_x - text_width // 2, button_y + 8),
            button_text,
            font=button_font,
            fill="white"
        )

        # NOTE: The actual link is not clickable in the image
        # If needed: generate separate image-per-property or use HTML layout for real buttons

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
