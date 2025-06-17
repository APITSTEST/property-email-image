from flask import Flask, request
from markupsafe import Markup
import feedparser
import os

app = Flask(__name__)

@app.route('/email-html')
def email_html():
    rss_url = request.args.get('rss')
    if not rss_url:
        return "Missing RSS feed URL", 400

    # Parse RSS feed
    feed = feedparser.parse(rss_url)
    entries = feed.entries[:3]

    # Build responsive HTML block
    html = ['<table width="100%" cellpadding="10" cellspacing="0" style="width:100%; max-width:600px; margin:0 auto;">']
    for entry in entries:
        image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
        title = entry.title
        description = entry.get("description", "")
        price = entry.get("category", "")
        link = entry.link

        html.append(f'''
            <tr>
                <td align="center" style="font-family:sans-serif; font-size:14px; color:#333; border-bottom:1px solid #eee; padding-bottom:20px;">
                    <img src="{image_url}" alt="Property image" width="100%" style="max-width:250px; border-radius:8px;" /><br/>
                    <strong>{title}</strong><br/>
                    {description}<br/>
                    <strong style="color:#FF9500;">{price}</strong><br/>
                    <a href="{link}" style="
                        display:inline-block;
                        margin-top:10px;
                        padding:10px 20px;
                        background-color:#FF9500;
                        color:#fff;
                        text-decoration:none;
                        font-weight:bold;
                        border-radius:20px;
                        font-size:14px;
                    ">View Property</a>
                </td>
            </tr>
        ''')

    html.append('</table>')
    return Markup(''.join(html))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
