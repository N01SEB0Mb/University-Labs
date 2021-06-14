# created by noisebomb

# coding=utf-8

from lxml import html
from html import unescape


def clear(string):
    try:
        while string[0] in ("\n", " "):
            string = string[1:]
    except IndexError:
        pass
    else:
        try:
            while string[-1] in ("\n", " "):
                string = string[:-1]
        except IndexError:
            pass
    return unescape(string)


def parse(body, partner, max_len=1024, no_img=1, no_desc=1):
    info_tree = html.fromstring(body)

    # title
    _title = info_tree.xpath('//title/text()')

    if partner == "UAMotors":
        article_title = info_tree.xpath('//h1[@class="entry-title"]/text()')

        title = max(article_title + [""], key=len)
    elif partner == "Avtoblog":
        article_title = info_tree.xpath('//h1[1]/text()')

        title = max(article_title + [""], key=len)
    elif partner == "ТОнеТО":
        article_title = info_tree.xpath('//h1/span/text()')

        title = max(article_title + [""], key=len)
    elif partner == "depo.ua":
        article_title = info_tree.xpath('//h1[@imemprop="headline"]/text()')

        title = max(article_title + [""], key=len)
    elif partner == "Перша":
        article_title = info_tree.xpath('//h1[@class="entry-title"]/text()')

        title = max(article_title + [""], key=len)
    else:
        og_title = info_tree.xpath('//meta[@property="og:title" or @name="og:title"]/@content')
        twitter_title = info_tree.xpath('//meta[@property="twitter:title" or @name="twitter:title"]/@content')

        title = max(og_title + twitter_title + [""], key=len)

    if not title:
        try:
            title = _title[0]
        except IndexError:
            return None

    # description

    if partner == "UAMotors":
        article_description = info_tree.xpath('//div[@class="td-post-content"]/p[1]/text()')
        span_description = info_tree.xpath('//div[@class="td-post-content"]//span/text()')[1]

        description = max([span_description] + article_description + [""], key=len)
    elif partner == "Avtoblog":
        article_description = info_tree.xpath('//p[@style="text-align: justify;"]/text()')[0]

        description = max([article_description] + [""], key=len)
    elif partner == "ТОнеТО":
        article_description = info_tree.xpath('//div[@class="newsText"]//p/text()')[0]

        description = max([article_description] + [""], key=len)
    elif partner == "Перша":
        article_description = info_tree.xpath('//span[@style="color: #800000;"]/text()')[0]

        description = max([article_description] + [""], key=len)
    elif partner == "Багнет":
        article_description = info_tree.xpath('//div[@id="bodytext"]/p/text()')[0]

        description = max([article_description] + [""], key=len)
    else:
        article_description = info_tree.xpath('//div[@class="article-body"]//strong/text()')  # Hyser
        og_description = info_tree.xpath('//meta[@property="og:description" or @name="og:description"]/@content')
        _description = info_tree.xpath('//meta[@property="description" or @name="description"]/@content')
        twitter_description = info_tree.xpath('//meta[@name="twitter:description" or'
                                              '@property="twitter:description"]/@content')

        description = max(article_description + og_description + _description +
                          twitter_description + [""], key=len)

    if description:
        while len(title) + len(description) + 16 > max_len:
            description = description[:-1]
        while description[-1] in (" ", ";", "."):
            description = description[:-1]
        description = clear(description) + "...\n\n"

    # image

    if partner == "ТОнеТО":
        article_image = info_tree.xpath('//div[@id="Content"]//img/@src')

        image_url = article_image[0] if article_image else None
    elif partner == "24 канал":
        article_image = info_tree.xpath('//div[@class="top-media-content"]/img/@src')

        image_url = "https://auto.24tv.ua/" + article_image[0] if article_image else None
    elif partner == "depo.ua":
        article_image = info_tree.xpath('//div[@class="openPost-content"]/img/@src')

        image_url = article_image[0] if article_image else None
    elif partner == "Перша":
        article_image = info_tree.xpath('//figure[@class="entry-thumbnail"]/img/@src')

        image_url = article_image[0] if article_image else None
    elif partner == "Fixygen":
        article_image = info_tree.xpath('//div[@class="communications-holder"]//img/@src')
        
        image_url = article_image[0] if article_image else None
    else:
        og_image = info_tree.xpath('//meta[@property="og:image" or @name="og:image"]/@content')
        twitter_image = info_tree.xpath('//meta[@name="twitter:image" or @property="twitter:image"]/@content')

        image_url = og_image[0] if og_image else twitter_image[0] if twitter_image else None

    if (description or no_desc) and (image_url or no_img):
        return clear(title), description, image_url
    else:
        return None
