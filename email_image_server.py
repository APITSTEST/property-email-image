@app.route('/email-html')
def email_html():
    rss_url = request.args.get('rss')
    if not rss_url:
        return "Missing RSS feed URL", 400

    feed = feedparser.parse(rss_url)
    entries = feed.entries[:4]  # Show up to 4 properties

    html = ['<table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0 auto;">']

    for i in range(0, len(entries), 2):
        html.append('<tr>')  # Start row

        for j in range(2):
            if i + j < len(entries):
                entry = entries[i + j]
                image_url = entry.media_content[0]['url'] if 'media_content' in entry else ''
                title = entry.title
                description = entry.get("description", "")
                price = entry.get("category", "")
                link = entry.link

                html.append(f'''
                    <td width="50%" valign="top" align="center" style="font-family:sans-serif; font-size:14px; color:#333; padding:10px;">
                        <img src="{image_url}" alt="Property image" style="width:100%; max-width:250px; border-radius:8px;" /><br/>
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
                ''')
            else:
                html.append('<td width="50%" style="padding:10px;"></td>')  # Empty cell for odd number of entries

        html.append('</tr>')  # End row

    html.append('</table>')
    return Markup(''.join(html))
