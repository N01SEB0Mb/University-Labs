# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class XPertAuto(Client):
    class Link:
        main = "https://xpert-auto.ua/"
        login = "https://xpert-auto.ua/actions/login-form"
        search = "https://xpert-auto.ua/storage?q={}"
        stocks = "https://xpert-auto.ua/actions/check-product-store"

    name = "xpertauto"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def get_info(self, article, brand):
        if self.connected and self.logged:
            search_request = self.session.get(self.Link.search.format(article))
            if search_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")

            search_tree = html.fromstring(search_request.text.replace("<tbody", "<tbody>"))
            csrf_token = search_tree.xpath('//meta[@name="csrf-token"]/@content')[0]
            items = search_tree.xpath('//tbody/tr[not(contains(@class, "spacer"))]')

            if not items:
                return self.response_brand(1, "Артикул не знайдено")

            found = False
            response_item = ResponseItem()

            for item in items:
                item_brand = self.clear(item.xpath('.//td[@data-label="Бренд"]/a/text()')[0])
                found_item = ResponseItem(
                    brand=item_brand,
                    article=self.clear(item.xpath('.//td[@data-label="Артикул"]/a/text()')[0]),
                    name=self.clear(item.xpath('.//td[@data-label="Наименование"]/a/text()')[0]),
                    price="%.2f UAH" % float(item.xpath('.//td[@data-label="Вход. Цена"]/span/text()')[0])
                )
                stocks_id = item.xpath('.//td[@data-label="Наличие"]/@data-id')[0]

                stock_request = self.session.post(self.Link.stocks, data={"id": stocks_id},
                                                  headers={"Content-Type": "application/x-www-form-urlencoded",
                                                           "X-CSRF-Token": csrf_token})

                if stock_request.status_code == 200:
                    if "stores" in stock_request.json():
                        for stock in stock_request.json()["stores"]:
                            found_item["stocks"].append(
                                {"name": stock["store"],
                                 "quantity": stock["stock"],
                                 "term": None}
                            )

                try:
                    image_link = self.Link.main[:-1] + item.xpath('.//td[@data-label="Фото"]/img/@src')[0]
                except IndexError:
                    pass
                else:
                    found_item["image"] = self.get_image(image_link, image_link.split("/")[-1].split(".")[0])

                if found:
                    response_item.set_analog(found_item)
                else:
                    found = True
                    response_item = found_item

            return self.response_brand(0, "OK", response_item)
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        main_page_request = self.session.get(self.Link.main)
        if main_page_request.status_code != 200:
            return 0, 0
        html_tree = html.fromstring(main_page_request.text)
        csrf_token = html_tree.xpath('//meta[@name="csrf-token"]/@content')[0]
        login_request = self.session.post(self.Link.login, data={"email": self.username, "password": self.password},
                                          headers={"Content-Type": "application/x-www-form-urlencoded",
                                                   "X-CSRF-Token": csrf_token})
        if login_request.status_code == 200:
            if login_request.text == "login":
                return 1, 1
        return 1, 0
