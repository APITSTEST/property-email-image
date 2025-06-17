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

    feed = feedparser.parse(rss_url)
    entries = feed.entries[:4]  # Show up to 4 properties

    html = ['''
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
    ''']

    for i in range(0, len(entries), 2):
        html.append('<tr>')

        for j in range(2):
            if i + j < len(entries):
                entry = entries[i + j]
                image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
                title = entry.title
                description = entry.get("description", "")
                price = entry.get("category", "")
                link = entry.link

                html.append(f'''
                    <td width="50%" style="padding:10px;" align="center" valign="top">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:280px;">
                            <tr>
                                <td align="center" style="font-family:sans-serif; font-size:14px; color:#333;">
                                    <img src="{image_url}" alt="Property image" width="100%" style="border-radius:8px;"><br/>
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
                        </table>
                    </td>
                ''')
            else:
                html.append('<td width="50%" style="padding:10px;"></td>')

        html.append('</tr>')

    html.append('</table>')
    return Markup(''.join(html))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
