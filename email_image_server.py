from flask import Flask, request, Markup
import feedparser

app = Flask(__name__)

@app.route('/email-html')
def email_html():
    rss_url = request.args.get('rss')
    if not rss_url:
        return "Missing RSS feed URL", 400

    # Parse RSS feed
    feed = feedparser.parse(rss_url)
    entries = feed.entries[:3]

    # Build HTML block
    html = ['<table width="100%" cellpadding="10" cellspacing="0"><tr>']
    for entry in entries:
        image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
        title = entry.title
        description = entry.get("description", "")
        price = entry.get("category", "")
        link = entry.link

        html.append(f'''
            <td align="center" style="font-family:sans-serif; font-size:14px; color:#333;">
                <img src="{image_url}" alt="Property image" width="250" style="border-radius:8px;" /><br/>
                <strong>{title}</strong><br/>
                {description}<br/>
                <strong style="color:#FF9500;">{price}</strong><br/>
                <a href="{link}" style="
                    display:inline-block;
                    margin-top:8px;
                    padding:10px 15px;
                    background-color:#FF9500;
                    color:#fff;
                    text-decoration:none;
                    font-weight:bold;
                    border-radius:20px;
                    font-size:14px;
                ">View Property</a>
            </td>
        ''')

    html.append('</tr></table>')
    return Markup(''.join(html))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
