# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class AsiaParts(Client):
    class Link:
        main = "https://b2b.asiaparts.ua"
        login = "https://b2b.asiaparts.ua/login/"
        search = "https://b2b.asiaparts.ua/index.php?route=product/search&search={}"
        details = "https://b2b.asiaparts.ua/index.php?route=revolution/revpopupview&product_id={}"

    name = "asiaparts"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def search(self, article):
        if self.connected and self.logged:
            search_request = self.session.get(self.Link.search.format(article))
            if search_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")

            search_tree = html.fromstring(search_request.text)
            items = search_tree.xpath('//div[@class="row products_category"]/div')

            response = []

            for item in items:
                item_id = item.xpath('.//div[@class="lupa"]/a/@onclick')[0].replace("get_revpopup_view('", "")
                item_info_request = self.session.get(self.Link.details.format(item_id.replace("');", "")), headers={
                    "Referer": self.Link.search.format(article), "X-Requested-With": "XMLHttpRequest"
                })
                item_info_tree = html.fromstring(item_info_request.text)
                item_brand, item_article = item_info_tree.xpath('//div[@class="dotted-line_right"]//text()')[:2]
                if not self.compare_art(article, item_article):
                    continue
                found_item = {
                    "article": item_article,
                    "brand": item_brand,
                    "name": item_info_tree.xpath('//div[@class="popup-heading"]/text()')[0],
                    "desc": self.clear(" ".join(item_info_tree.xpath('//div[@class="rev_slider"]/p/text()')))
                }

                try:
                    price = item_info_tree.xpath('//span[@class="update_price"]/text()')[0]
                    assert price
                except (IndexError, AssertionError):
                    pass
                else:
                    found_item["price"] = price.replace("$", "") + " USD"

                image_link = item_info_tree.xpath('//img[@class="img-responsive main-image"]/@src')[0]
                found_item["image"] = self.get_image(image_link, image_id=image_link.split("/")[-1].split(".")[0])

                stocks = item_info_tree.xpath('//div[@class="radio"]//span/text()')
                for stock in stocks:
                    stock_name, stock_quantity = stock.split(" (")
                    try:
                        found_item["stocks"].append({
                            "name": stock_name,
                            "quantity": stock_quantity.replace(" шт.)", ""),
                            "term": None
                        })
                    except KeyError:
                        found_item["stocks"] = [{
                            "name": stock_name,
                            "quantity": stock_quantity.replace(" шт.)", ""),
                            "term": None
                        }]

                response.append(found_item)

            if not response:
                return self.response_article(1, "Артикул не знайдено")

            return self.response_article(0, "OK", response)
        elif self.connected:
            return self.response_article(3, "Помилка авторизації")
        else:
            return self.response_article(2, "Помилка з'єднання")

    def get_info(self, article, brand):
        if self.connected and self.logged:
            search_request = self.session.get(self.Link.search.format(article))
            if search_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")

            search_tree = html.fromstring(search_request.text)
            items = search_tree.xpath('//div[@class="row products_category"]/div')

            if not items:
                return self.response_brand(1, "Артикул не знайдено")

            analogs = []

            found = False

            for item in items:
                item_id = item.xpath('.//div[@class="lupa"]/a/@onclick')[0].replace("get_revpopup_view('", "")
                item_info_request = self.session.get(self.Link.details.format(item_id.replace("');", "")), headers={
                    "Referer": self.Link.search.format(article), "X-Requested-With": "XMLHttpRequest"
                })
                item_info_tree = html.fromstring(item_info_request.text)
                item_brand, item_article = item_info_tree.xpath('//div[@class="dotted-line_right"]//text()')[:2]
                found_item = ResponseItem(
                    item_id=item_id.replace("');", ""),
                    article=item_article,
                    brand=item_brand,
                    name=item_info_tree.xpath('//div[@class="popup-heading"]/text()')[0],
                    desc=self.clear(" ".join(item_info_tree.xpath('//div[@class="rev_slider"]/p/text()')))
                )

                try:
                    price = item_info_tree.xpath('//span[@class="update_price"]/text()')[0]
                    assert price
                except (IndexError, AssertionError):
                    pass
                else:
                    found_item["price"] = price.replace("$", "") + " USD"

                image_link = item_info_tree.xpath('//img[@class="img-responsive main-image"]/@src')[0]
                found_item["image"] = self.get_image(image_link, image_id=image_link.split("/")[-1].split(".")[0])

                stocks = item_info_tree.xpath('//div[@class="radio"]//span/text()')
                for stock in stocks:
                    stock_name, stock_quantity = stock.split(" (")
                    found_item["stocks"].append({
                        "name": stock_name,
                        "quantity": stock_quantity.replace(" шт.)", ""),
                        "term": None
                    })

                if self.compare(brand, item_brand) and not found:
                    response_item = found_item
                    found = True
                else:
                    analogs.append(found_item)

            if found:
                for analog in analogs:
                    response_item.set_analog(analog)
            else:
                response_item = analogs.pop(0)

                for analog in analogs:
                    response_item.set_analog(analog)

            return self.response_brand(0, "OK", response_item)
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        main_page_request = self.session.get(self.Link.main)
        if main_page_request.status_code != 200:
            return 0, 0

        login_data = {
            "email": (None, self.username),
            "password": (None, self.password)
        }

        login_request = self.session.post(self.Link.login, files=login_data, headers={
            "Referer": self.Link.login, "Origin": self.Link.main
        })

        if login_request.status_code == 200:
            return 1, 1
        return 1, 0
