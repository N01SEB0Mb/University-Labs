# coding=utf-8

from parser.client.Client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class Busmarket(Client):
    class Link:
        search = "https://api.bm.parts/search/products?q={0}&currency={1}"
        stocks = "https://api.bm.parts/product/{0}/in_stocks"
        product = "https://api.bm.parts/product/{0}"
        search_with_brand = "https://api.bm.parts/search/products?q={0}&brands={1}"
        photo = "https://cdn.bm.parts/photos/1920x1920"

    name = "busmarket"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]
        self.token = SITE_CONFIG["token"]

        self.currency = SITE_CONFIG["currency"]
        self.session.headers.update({"Authorization": self.token})

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def get_info(self, article, brand):
        def get_uuid(article, brand):
            article = article.replace(" ", "")
            search_request = self.session.get(self.Link.search.format(article, self.currency))
            if search_request.status_code == 200:
                if not search_request.json()["products"].keys():
                    return True, "Артикул не знайдено"
                for key in search_request.json()["products"].keys():
                    item_brand = search_request.json()["products"][key]["brand"]
                    if self.compare(brand, item_brand):
                        return key, "OK"
                return True, "Бренд не знайдено"
            return False, "Помилка з'єнання"

        response, message = get_uuid(article, brand)
        if response is True:
            return self.response_brand(1, message)
        elif response is False:
            return self.response_brand(2, "Помилка з'єднання")

        product_request = self.session.get(self.Link.product.format(response))
        product_info = product_request.json()["product"]

        if product_request.status_code == 200:
            item = ResponseItem(
                item_id=response,
                article=product_info["article"],
                brand=product_info["brand"],
                name=product_info["name"],
                price=product_info["price"] + " UAH")

            image_link = self.Link.photo + product_info["default_image"].replace("photo", "").replace("\\", "/")
            item["image"] = self.get_image(image_link, response)

            item["stocks"] = self.__get_stocks(response)
            item["stocks"].append({"name": "Ожидается",
                                   "quantity": product_info["in_waiting"]["quantity"],
                                   "term": None})

            for car in product_info["cars"]:
                for model in car["models"]:
                    for engine in model["engines"]:
                        try:
                            item["using"][car["brand"]].append(model["model"] + " (" + engine["engine"] + ")")
                        except KeyError:
                            item["using"][car["brand"]] = [model["model"] + " (" + engine["engine"] + ")"]

            for analog_uuid in product_info["analogs"]:
                analog = ResponseItem(
                    item_id=analog_uuid,
                    article=product_info["analogs"][analog_uuid]["article"],
                    brand=product_info["analogs"][analog_uuid]["brand"],
                    name=product_info["analogs"][analog_uuid]["name"],
                    price=product_info["analogs"][analog_uuid]["price"] + " UAH")

                analog["stocks"] = self.__get_stocks(analog_uuid)
                analog["stocks"].append({"name": "Ожидается",
                                         "quantity": product_info["analogs"][analog_uuid]["in_waiting"]["quantity"],
                                         "term": None})
                image_link = product_info["analogs"][analog_uuid]["default_image"].replace("photo", "")
                analog["image"] = self.get_image(self.Link.photo + image_link.replace("\\", "/"), analog_uuid)

                item.set_analog(analog)

            return self.response_brand(0, "OK", item=item)
        elif product_request.status_code in (404, 422):
            return self.response_brand(1, "ID не найден")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def __get_stocks(self, uuid):
        stocks_request = self.session.get(self.Link.stocks.format(uuid))
        stocks = []
        if stocks_request.status_code == 200:
            for stock in stocks_request.json()["in_stocks"]:
                stock_pp = stock["contract_quantities"][0]["quantity"]
                stock_dag = stock["contract_quantities"][1]["quantity"]
                stock_pp = "0" if stock_pp == "-" else stock_pp
                stock_dag = "0" if stock_dag == "-" else stock_dag

                if stock_pp == stock_dag == "> 10":
                    stocks.append({"name": stock["name"],
                                   "quantity": ">20",
                                   "term": None})
                elif stock_pp == "> 10":
                    stocks.append({"name": stock["name"],
                                   "quantity": ">" + str(10 + int(stock_dag)),
                                   "term": None})
                elif stock_dag == "> 10":
                    stocks.append({"name": stock["name"],
                                   "quantity": ">" + str(10 + int(stock_pp)),
                                   "term": None})
                else:
                    stocks.append({"name": stock["name"],
                                   "quantity": str(int(stock_pp) + int(stock_dag)),
                                   "term": None})
        return stocks
