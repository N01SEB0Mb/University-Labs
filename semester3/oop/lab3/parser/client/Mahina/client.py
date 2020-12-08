# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class Mahina(Client):
    class Link:
        main = "https://mahina.in.ua/"
        login = "https://mahina.in.ua/personal/"
        search = "https://mahina.in.ua/catalog/?q={0}&limit={1}"
        analogs = "https://mahina.in.ua/include/analog_list_new.php"

    name = "mahina"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]
        self.searchLimit = SITE_CONFIG["searchLimit"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    # def search(self, article):
    #     if self.connected and self.logged:
    #         search_request = self.session.get(self.Link.search.format(article, self.searchLimit))
    #         if search_request.status_code != 200:
    #             return self.response_article(2, "Помилка з'єднання")
    #
    #         search_tree = html.fromstring(search_request.text)
    #         items = search_tree.xpath('//div[@class="catalog-item-card"]')
    #
    #         if not items:
    #             return self.response_article(1, "Артикул не знайдено")
    #
    #         response = []
    #
    #         for item in items:
    #             item_brand = item.xpath('.//img[@class="manufacturer agll"]/@alt')[0]
    #             item_article = self.clear(item.xpath('.//div[@class="article"]/text()')[0].replace("№: ", ""))
    #             item_name = item.xpath('.//a[@class="item-title"]/@title')[0]
    #             item_price = "%.2f UAH" % float(self.clear(item.xpath('.//meta[@itemprop="price"]/@content')[0]))
    #
    #             stocks_info = self.clear(item.xpath('.//div[@class="available"]/div/span/text()')[0])
    #             if "В наличии" in stocks_info:
    #                 quantity = stocks_info.split(" ")[-1]
    #                 if not quantity.isdigit():
    #                     quantity = "2"
    #                 item_stocks = [{"name": "В наличии", "quantity": quantity, "term": 1}]
    #             elif "Поставка" in stocks_info:
    #                 item_stocks = [{"name": "Поставка", "quantity": "10", "term": stocks_info.split(" ")[1]}]
    #             else:
    #                 item_stocks = []
    #
    #             response.append({
    #                 "article": item_article,
    #                 "brand": item_brand,
    #                 "name": item_name,
    #                 "price": item_price,
    #                 "description": "",
    #                 "stocks": item_stocks
    #             })
    #
    #         return self.response_article(0, "OK", response)
    #     elif self.connected:
    #         return self.response_article(3, "Помилка авторизації")
    #     else:
    #         return self.response_article(2, "Помилка з'єднання")

    def get_info(self, article, brand):
        if self.connected and self.logged:
            search_request = self.session.get(self.Link.search.format(article, self.searchLimit))
            if search_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")

            search_tree = html.fromstring(search_request.text)
            items = search_tree.xpath('//div[@class="catalog-item-card"]')

            if not items:
                return self.response_brand(1, "Артикул не знайдено")

            for item in items:
                item_brand = item.xpath('.//img[@class="manufacturer agll" or @class="manufacturer"]/@alt')[0]
                item_article = self.clear(item.xpath('.//div[@class="article"]/text()')[0].replace("№: ", ""))
                if self.compare(item_brand, brand) and self.compare_art(article, item_article):
                    break
            else:
                found_item = ResponseItem(
                    brand=brand,
                    article=article,
                )

                for analog in items:
                    analog_article = self.clear(analog.xpath('.//div[@class="article"]/text()')[0].replace("№: ", ""))
                    if not self.compare_art(article, analog_article):
                        continue
                    analog_item = ResponseItem(
                        brand=analog.xpath('.//img[@class="manufacturer agll"]/@alt')[0],
                        article=analog_article,
                        name=analog.xpath('.//a[@class="item-title"]/@title')[0],
                        price="%.2f UAH" % float(self.clear(analog.xpath('.//meta[@itemprop="price"]/@content')[0]))
                    )

                    stocks_info = self.clear(analog.xpath('.//div[@class="available"]/div/span/text()')[0])
                    if "В наличии" in stocks_info:
                        quantity = stocks_info.split(" ")[-1]
                        if not quantity.isdigit():
                            quantity = "2"
                        analog_item["stocks"] = [{"name": "В наличии", "quantity": quantity, "term": 1}]
                    elif "Поставка" in stocks_info:
                        analog_item["stocks"] = [
                            {"name": "Поставка", "quantity": "10", "term": stocks_info.split(" ")[1]}]

                    image_link = self.Link.main[:-1] + analog.xpath('.//meta[@itemprop="image"]/@content')[0]
                    analog_item["image"] = self.get_image(image_link, image_link.split("/")[-1].split(".")[0])

                    found_item.set_analog(analog_item)

                return self.response_brand(0, "OK", found_item)

            found_item = ResponseItem(
                brand=item_brand,
                article=self.clear(item.xpath('.//div[@class="article"]/text()')[0].replace("№: ", "")),
                name=item.xpath('.//a[@class="item-title"]/@title')[0],
                price="%.2f UAH" % float(self.clear(item.xpath('.//meta[@itemprop="price"]/@content')[0]))
            )

            stocks_info = self.clear(item.xpath('.//div[@class="available"]/div/span/text()')[0])
            if "В наличии" in stocks_info:
                quantity = stocks_info.split(" ")[-1]
                if not quantity.isdigit():
                    quantity = "2"
                found_item["stocks"] = [{"name": "В наличии", "quantity": quantity, "term": 1}]
            elif "Поставка" in stocks_info:
                found_item["stocks"] = [{"name": "Поставка", "quantity": "-1", "term": stocks_info.split(" ")[1]}]

            image_link = self.Link.main[:-1] + item.xpath('.//meta[@itemprop="image"]/@content')[0]
            found_item["image"] = self.get_image(image_link, image_link.split("/")[-1].split(".")[0])

            analogs_list = item.xpath('.//a[@class="analog_list_ajax"]/@data-list')
            if analogs_list:
                list_elem = list(analogs_list.split(";"))
                analogs_request = self.session.post(self.Link.analogs, data={"list_elem[]": list_elem},
                                                    headers={"Content-Type": "application/x-www-form-urlencoded"})
                if analogs_request.status_code == 200:
                    analogs_tree = html.fromstring(analogs_request.text)
                    analogs = analogs_tree.xpath('//div[@class="catalog-item-info"]')
                    for analog in analogs:
                        analog_item = ResponseItem(
                            name=analog.xpath('.//div[@class="catalog-item-title"]/a/@title')[0]
                        )
                        analog_desc = analog.xpath('.//meta[@itemprop="description"]/@content')[0]
                        analog_item["article"] = analog_desc.split("(")[-1].replace(")", "")
                        analog_item["price"] = "%.2f UAH" % float(analog.xpath('.//meta[@itemprop="price"]/@content')[0])

                        stocks_info = self.clear(analog.xpath('.//div[@class="available"]/div/span/text()')[0])
                        if "В наличии" in stocks_info:
                            quantity = stocks_info.split(" ")[-1]
                            if not quantity.isdigit():
                                quantity = "2"
                            analog_item["stocks"] = [{"name": "В наличии",
                                                      "quantity": quantity, "term": 1}]
                        elif "Поставка" in stocks_info:
                            analog_item["stocks"] = [{"name": "Поставка",
                                                      "quantity": "-1", "term": stocks_info.split(" ")[1]}]

                        image_link = self.Link.main[:-1] + analog.xpath('.//meta[@itemprop="image"]/@content')[0]
                        analog_item["image"] = self.get_image(image_link, image_link.split("/")[-1].split(".")[0])

                        found_item.set_analog(analog_item)

            return self.response_brand(0, "OK", found_item)
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        main_page_request = self.session.get(self.Link.main)
        if main_page_request.status_code != 200:
            return 0, 0
        login_data = {
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "backurl": "/",
            "USER_LOGIN": self.username,
            "USER_PASSWORD": self.password,
            "login": "Войти"
        }
        login_request = self.session.post(self.Link.login, login_data,
                                          headers={"Content-Type": "application/x-www-form-urlencoded"})
        if login_request.status_code == 200:
            return 1, 1
        return 1, 0
