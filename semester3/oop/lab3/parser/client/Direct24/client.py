# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class Direct24(Client):
    class Link:
        main = "https://direct24.com.ua/ws/json/"
        login = "https://direct24.com.ua/users/login/?next=/"

    name = "direct24"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]
        self.passwordAPI = SITE_CONFIG["apiPassword"]

        self.start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - self.start_time)

    def get_info(self, article, brand):
        search_request = self.session.post(self.Link.main, data={
            "login": self.username,
            "password": self.passwordAPI,
            "partnumber": article,
            "manufacturer": brand,
            "analogs": "on"
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})

        if search_request.status_code == 200:
            try:
                assert len(search_request.json()[2])
            except BaseException:
                return self.response_article(1, "Артикул не знайдено")

            used_analogs = []
            analogs = []
            item = ResponseItem()

            for found_item in search_request.json()[2]:
                if item["article"] == "" and self.compare_art(article, found_item["PartCleanNumber"]) and self.compare(
                        brand, found_item["Manufacturer"]):
                    item["article"] = found_item["PartCleanNumber"]
                    item["brand"] = found_item["Manufacturer"]
                    item["price"] = found_item["Price"] + " EUR"
                    try:
                        term = int(found_item["DeliveryDays"])
                    except ValueError:
                        term = int(found_item["DeliveryDays"].split("-")[1])
                    item["stocks"] = [{"name": str(found_item["StoreID"]),
                                       "quantity": found_item["Quantity"],
                                       "term": term + 2}]
                    item["name"] = found_item["PartName"]
                    item["description"] = found_item["PartDescription"]

                    item["image"] = None
                elif item["article"] == found_item["PartCleanNumber"]:
                    if "-" in found_item["DeliveryDays"]:
                        term = int(found_item["DeliveryDays"].split("-")[1])
                    else:
                        term = int(found_item["DeliveryDays"])
                    item["foreign"].append({
                        "name": str(found_item["StoreID"]),
                        "quantity": found_item["Quantity"],
                        "term": term + 2,
                        "price": found_item["Price"] + " EUR"
                    })
                else:
                    if [found_item["PartCleanNumber"], found_item["Manufacturer"]] in used_analogs:
                        for analog in analogs:
                            if [found_item["PartCleanNumber"],
                                found_item["Manufacturer"]] == [analog["article"], analog["brand"]]:
                                if "-" in found_item["DeliveryDays"]:
                                    term = int(found_item["DeliveryDays"].split("-")[1])
                                else:
                                    term = int(found_item["DeliveryDays"])
                                analog["foreign"].append({
                                    "name": str(found_item["StoreID"]),
                                    "quantity": found_item["Quantity"],
                                    "term": term + 2,
                                    "price": found_item["Price"] + " EUR"
                                })
                    else:
                        used_analogs.append([found_item["PartCleanNumber"], found_item["Manufacturer"]])
                        try:
                            term = int(found_item["DeliveryDays"])
                        except ValueError:
                            term = int(found_item["DeliveryDays"].split("-")[1])
                        analog_item = ResponseItem(
                            article=found_item["PartCleanNumber"],
                            brand=found_item["Manufacturer"],
                            price=found_item["Price"] + " EUR",
                            name=found_item["PartName"],
                            desc=found_item["PartDescription"],
                            stocks=[{"name": str(found_item["StoreID"]),
                                     "quantity": found_item["Quantity"],
                                     "term": term + 2}]
                        )
                        analogs.append(analog_item)
            for analog in analogs:
                item.set_analog(analog)

            return self.response_brand(0, "OK", item=item)

        return self.response_article(2, "Помилка з'єднання")

    def get_currency(self):
        login_data = {
            "username": self.username,
            "password": self.password
        }

        login_request = self.session.post(self.Link.login, data=login_data,
                                          headers={"Content-Type": "application/x-www-form-urlencoded"})

        if login_request.status_code == 200:
            page = html.fromstring(login_request.content)
            currencies = page.xpath('//li/a[@class="tip"]/text()')
            response = {}

            for currency in currencies:
                currency_name, currency_value = currency.split(" = ")
                if currency_name in CONFIG["currency"]["direct24"]:
                    response[currency_name] = float(currency_value.replace(" грн.", ""))
            return self.response_currency(0, "Ок", response=response)
        else:
            return self.response_currency(2, "Помилка з'єднання")
