# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class MasterService(Client):
    class Link:
        main = "https://steering.com.ua/"
        login = "https://steering.com.ua/login"
        search = "https://steering.com.ua/catalog?oe={}"

    name = "masterservice"

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
            html_tree = html.fromstring(search_request.text)
            items = html_tree.xpath('//table[@class="vi-table vi-responsive"]/tr')
            if not items:
                return self.response_brand(1, "Артикул не знайдено")

            for item in items:
                brand_expr = './/td[@data-label=""]/a[@rel="nofollow"]/text()'
                try:
                    item_brand = self.clear(item.xpath(brand_expr)[0])
                except IndexError:
                    try:
                        item_brand = self.clear(item.xpath('.//td[@data-label=""]/text()')[1])
                    except IndexError:
                        item_brand = ""
                if self.compare(brand, item_brand):
                    break
            else:
                return self.response_brand(1, "Бренд не знайдено")

            item_link = item.xpath('.//td/div/a/@href')[0]
            item_info_request = self.session.get(item_link)
            if item_info_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")

            item_info_tree = html.fromstring(item_info_request.text)
            item_info = item_info_tree.xpath('//table[@class="vi-item-table"]//td/text()')
            item = ResponseItem(
                article=self.clear(item_info[1]),
                brand=item_brand,
                name="".join(item_info_tree.xpath('//h1[@class="vi-item-name"]/span/text()')[:-1]),
                desc=self.clear(item_info[9])
            )

            try:
                item_price = self.clear(item_info_tree.xpath('//span[@class="value"]/span/text()')[0]).replace(" ", "")
            except IndexError:
                item_price = "0"
            item["price"] = "%.2f UAH" % float(item_price)

            try:
                item_stocks = item_info_tree.xpath('//td[@class="product-nalichie-table"]/table/tr/td/text()')[1:]
            except IndexError:
                pass
            else:
                name = None
                for number, value in enumerate(item_stocks):
                    if number % 2:
                        item["stocks"].append(
                            {"name": name,
                             "quantity": self.clear(value),
                             "term": None}
                        )
                    else:
                        name = self.clear(value)
            try:
                image_link = self.Link.main[:-1] + item_info_tree.xpath('//div[@class="fotorama"]/img/@src')[0]
            except IndexError:
                pass
            else:
                item["image"] = self.get_image(image_link, image_id=image_link.split("/")[-1].split(".")[0])

            car_using = item_info_tree.xpath('//div[@class="row vi-prim-auto"]//ul[@class="prim-car"]/li')

            for car in car_using:
                car_name = self.clear(car.xpath('./span/text()')[0])
                car_models = car.xpath('./ul/li')
                for car_model in car_models:
                    model_name = self.clear(car_model.xpath('./span/text()')[0])
                    model_vars = car_model.xpath('./ul/li/text()')
                    for model_var in model_vars:
                        try:
                            item["using"][car_name].append(model_name + " " + self.clear(model_var))
                        except KeyError:
                            item["using"][car_name] = [model_name + " " + self.clear(model_var)]

            oe = item_info_tree.xpath('//div[@class="row vi-prim-auto"]//div[@class="car-oe"]//dd[@class="content"]')[0]
            oe_codes = oe.xpath("./a/text()")

            for oe_code in oe_codes:
                try:
                    item["cross"][""].append(self.clear(oe_code))
                except KeyError:
                    item["cross"][""] = [self.clear(oe_code)]

            analogs_table = item_info_tree.xpath('//table[@class="products-list vi-table vi-responsive"]')[0]
            analogs = analogs_table.xpath('.//tr[@class="even" or @class="odd"]')
            for analog in analogs:
                analogs_name_list = analog.xpath('.//a[@class="name"]/span/text()')
                try:
                    analog_brand = self.clear(analog.xpath('.//div[@class="vendor"]/span[@class="value"]/text()')[0])
                except IndexError:
                    analog_brand = ""
                analog_item = ResponseItem(
                    article=self.clear(analogs_name_list[-1]),
                    brand=analog_brand,
                    name=self.clear("".join(analogs_name_list[:-1]))
                )

                analog_stocks = analog.xpath('.//td[@class="storage"]//td[not(contains(@class, "title_sklad"))]/text()')
                stock_name = ""
                for number, stock in enumerate(analog_stocks[1:]):
                    if number % 2:
                        analog_item["stocks"].append(
                            {"name": stock_name,
                             "quantity": self.clear(stock),
                             "term": None}
                        )
                    else:
                        stock_name = self.clear(stock).replace(":", "")

                image_link = self.Link.main[:-1] + analog.xpath('.//td[@data-label="Фото"]//img/@src')[0]
                analog_item["image"] = self.get_image(image_link, image_id=image_link.split("/")[-1].split(".")[0])

                item.set_analog(analog_item)

            return self.response_brand(0, "OK", item)
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        main_page_request = self.session.get(self.Link.main)
        if main_page_request.status_code != 200:
            return 0, 0
        login_request = self.session.post(self.Link.login, data={"login": self.username, "password": self.password},
                                          headers={"Content-Type": "application/x-www-form-urlencoded"})
        if login_request.status_code == 200:
            return 1, 1
        else:
            return 1, 0
