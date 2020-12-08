# coding=utf-8

from parser.client.Client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class AutoTechnics(Client):
    class Link:
        main = "https://b2b.ad.ua/"
        login = "https://b2b.ad.ua/Account/Login"
        search = "https://b2b.ad.ua/api/catalog/search?grp=&item="
        category = "https://b2b.ad.ua/api/catalog/searchgrp?item="
        quantity = "https://b2b.ad.ua/api/catalog/stockitems"
        analog = "https://b2b.ad.ua/api/catalog/replace?code="
        cross = "https://b2b.ad.ua/api/catalog/oemitems?code="
        use = "https://b2b.ad.ua/api/catalog/carapplication?code="
        image = "https://b2b.ad.ua/img/"

    name = "autotechnics"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]
        self.companyId = SITE_CONFIG["companyId"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def search(self, article):
        if not self.connected:
            return self.response_article(2, "Помилка з'єднання")
        elif not self.logged:
            return self.response_article(3, "Помилка авторизації")

        try:
            article = self.clear(str(article.replace("-", "").replace("/", "").replace(" ", "")))
            get_search_results = self.session.get(self.Link.search + article, timeout=self.timeout)
            assert get_search_results.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return self.response_article(2, "Помилка з'єднання")

        items = get_search_results.json()["items"]

        if not items:
            return self.response_article(1, "Артикул не знайдено")

        response = []
        for number, item in enumerate(items):
            if self.searchArt:
                if not self.compare_art(article, item["Item"]):
                    found_by = []
                    for by in get_search_results.json()["by"]:
                        if by["item"] == item["Item"]:
                            found_by.append(by["brand"] + ": " + by["search"])

                    if found_by:
                        item["Название"] += " (Найдено по: {})".format(", ".join(found_by))
                    else:
                        continue

            response.append({"article": item["Item"],
                             "brand": item["Бренд"],
                             "name": item["Название"],
                             "description": item["Описание"],
                             "price": "%.2f UAH" % item["Retail"]})

        if not response:
            return self.response_article(1, "Артикул не знайдено")
        else:
            return self.response_article(0, "OK", item=response)

    def get_info(self, article, brand):
        if self.connected and self.logged:
            article = self.clear(str(article), delchars=" ./-")
            get_search_results = self.session.get(self.Link.search + article, timeout=self.timeout)
            if get_search_results.status_code == 200:
                result_dict = get_search_results.json()
                if result_dict and result_dict["items"]:
                    for item in result_dict["items"]:
                        if self.compare(item["Бренд"], brand):
                            item = ResponseItem(item_id=item["Item"], price="%.2f UAH" % item["Price"],
                                                brand=item["Бренд"], article=item["Item"],
                                                name=item["Название"], desc=item["Описание"])
                            break
                    else:
                        item = self.__search_by_analogs__(result_dict, article, brand, ResponseItem())
                        if item is None:
                            return self.response_brand(1, "Бренд не знайдено")
                        else:
                            return self.response_brand(0, "OK", item=item)
                    try:
                        cross_request = self.session.get(self.Link.cross + item["article"].replace(" ", "+"),
                                                         timeout=self.timeout)
                        assert cross_request.status_code == 200
                        for number in cross_request.json():
                            item["cross"] = dict()
                            try:
                                item["cross"][number["Brand1"]].append(number["Code1"])
                            except KeyError:
                                item["cross"][number["Brand1"]] = [number["Code1"]]
                    except (AssertionError, KeyError):
                        pass
                    try:
                        use_request = self.session.get(self.Link.use + item["article"].replace(" ", "+"),
                                                       timeout=self.timeout)
                        assert use_request.status_code == 200
                        for using in use_request.json():
                            item["using"] = dict()
                            try:
                                item["using"][using["MARK"]].append(using["MODEL"])
                            except KeyError:
                                item["using"][using["MARK"]] = [using["MODEL"]]
                    except (AssertionError, KeyError):
                        pass
                    i_url = "https://b2b.ad.ua/img/{0}/"
                    try:
                        for image in result_dict["images"]:
                            if image["Item"] == item.id:
                                item["image"] = self.get_image(i_url.format(image["GraTab"]) + image["GraGrdId"],
                                                               image["GraGrdId"])
                    except KeyError:
                        pass
                    analogs_list = []
                    try:
                        get_analog_info = self.session.get(self.Link.analog + str(item.id).replace(" ", "+"),
                                                           timeout=self.timeout)
                        analog_info = get_analog_info.json()["items"]
                        assert get_analog_info.status_code == 200
                        for analog_item in analog_info:
                            analog = ResponseItem(item_id=analog_item["Item"],
                                                  article=analog_item["Item"],
                                                  brand=analog_item["Бренд"],
                                                  price="%.2f UAH" % analog_item["Price"],
                                                  name=analog_item["Название"],
                                                  desc=analog_item["Описание"])
                            try:
                                for image in analog_item["images"]:
                                    if image["Item"] == analog.id:
                                        analog["image"] = self.get_image(
                                            i_url.format(image["GraTab"]) + image["GraGrdId"],
                                            image["GraGrdId"])
                            except KeyError:
                                pass
                            try:
                                analogs_list.append(deepcopy(analog))
                            except UnboundLocalError:
                                pass
                            # try:
                            #     data_body = """{"items": "''""" + str(item.id)\
                            #                 + """'', ''""" + str(analog.id) + """''"}"""
                            # except UnboundLocalError:
                            #     data_body = """{"items": "''""" + str(item.id) + """''"}"""
                            # quantity_request = self.session.post(self.quantity_link, timeout=self.timeout,
                            #                                      data=data_body,
                            #                                      headers={**self.headers,
                            #                                               "Content-Type": "text/html; charset=UTF-8"})
                    except (AssertionError, KeyError, IndexError):
                        pass
                    data_body = """{"items": "''""" + str(item.id) + """''"""
                    for analogs in analogs_list:
                        data_body += """,''""" + str(analogs.id) + "''"
                    quantity_request = self.session.post(self.Link.quantity, timeout=self.timeout,
                                                         data=(data_body + """"}""").encode("utf-8").decode("utf-8"),
                                                         headers={"Content-Type": "text/html; charset=UTF-8"})
                    if quantity_request.status_code == 200:
                        for stock_ in quantity_request.json():
                            stock = deepcopy(stock_)
                            if stock["ItemNo"] == item.id:
                                item["stocks"].append({"name": stock["LocationCode"],
                                                       "quantity": stock["Qty"],
                                                       "term": None})
                            else:
                                for analog in analogs_list:
                                    if analog["article"] == stock["ItemNo"]:
                                        analog["stocks"].append({"name": stock["LocationCode"],
                                                                 "quantity": stock["Qty"],
                                                                 "term": None})
                    analogs_id = {item.id}
                    for analog in analogs_list:
                        analogs_id.add(analog.id)
                        item.set_analog(analog)
                    return self.response_brand(0, "OK", item=self.__search_by_analogs__(result_dict, article,
                                                                                        brand, item, analogs_id))
                else:
                    return self.response_brand(1, "Артикул не знайдено")
            else:
                return self.response_brand(2, "Помилка з'єднання")
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def __search_by_analogs__(self, result_dict, article, brand, item, analog_id=None):
        analogs = []
        used_analogs = analog_id if analog_id else set()

        for item_ in result_dict["items"]:
            skip = False
            for found_by in result_dict["by"]:
                if found_by["item"] == item_["Item"]:
                    if not self.compare(found_by["brand"], brand) or not self.compare(found_by["search"], article):
                        skip = True
                    break
            if skip:
                continue

            # analog_item = ResponseItem(item_id=item_["Item"], price="%.2f UAH" % item_["Price"],
            #                            brand=item_["Бренд"], article=item_["Item"],
            #                            name=item_["Название"], desc=item_["Описание"])

            if item_["Item"] not in used_analogs:
                analogs.append(ResponseItem(item_id=item_["Item"], price="%.2f UAH" % item_["Price"],
                                            brand=item_["Бренд"], article=item_["Item"],
                                            name=item_["Название"], desc=item_["Описание"]))

            analogs_request = self.session.get(self.Link.analog + str(item_["Item"]).replace(" ", "+"))
            for analog_item in analogs_request.json()["items"]:
                if not analog_item["Item"] in used_analogs:
                    analogs.append(ResponseItem(item_id=analog_item["Item"],
                                                article=analog_item["Item"],
                                                brand=analog_item["Бренд"],
                                                price="%.2f UAH" % analog_item["Price"],
                                                name=analog_item["Название"],
                                                desc=analog_item["Описание"]))
                    used_analogs.add(analog_item["Item"])
                    try:
                        for image in analog_item["images"]:
                            if image["Item"] == analogs[-1].id:
                                i_url = "https://b2b.ad.ua/img/{0}/".format(image["GraTab"])
                                analogs[-1]["image"] = self.get_image(i_url + image["GraGrdId"], image["GraGrdId"])
                    except KeyError:
                        pass
        if item:
            try:
                cross_request = self.session.get(self.Link.cross + item["article"].replace(" ", "+"),
                                                 timeout=self.timeout)
                assert cross_request.status_code == 200
                for number in cross_request.json():
                    item["cross"] = dict()
                    try:
                        item["cross"][number["Brand1"]].append(number["Code1"])
                    except KeyError:
                        item["cross"][number["Brand1"]] = [number["Code1"]]
            except (AssertionError, KeyError):
                pass
            try:
                use_request = self.session.get(self.Link.use + item["article"].replace(" ", "+"),
                                               timeout=self.timeout)
                assert use_request.status_code == 200
                for using in use_request.json():
                    item["using"] = dict()
                    try:
                        item["using"][using["MARK"]].append(using["MODEL"])
                    except KeyError:
                        item["using"][using["MARK"]] = [using["MODEL"]]
            except (AssertionError, KeyError):
                pass
            i_url = "https://b2b.ad.ua/img/{0}/"
            try:
                for image in result_dict["images"]:
                    if image["Item"] == item.id:
                        item["image"] = self.get_image(i_url.format(image["GraTab"]) + image["GraGrdId"],
                                                       image["GraGrdId"])
            except KeyError:
                pass

            data_body = """{"items": "''""" + str(item.id) + """''"""
            for analog in analogs:
                data_body += """,''""" + str(analog.id) + "''"
            quantity_request = self.session.post(self.Link.quantity, timeout=self.timeout,
                                                 data=(data_body + """"}""").encode("utf-8"),
                                                 headers={"Content-Type": "text/html; charset=UTF-8"})
            if quantity_request.status_code == 200:
                for stock_ in quantity_request.json():
                    stock = deepcopy(stock_)
                    if stock["ItemNo"] == item.id:
                        item["stocks"].append({"name": stock["LocationCode"],
                                               "quantity": stock["Qty"],
                                               "term": None})
                    else:
                        for analog in analogs:
                            if analog["article"] == stock["ItemNo"]:
                                analog["stocks"].append({"name": stock["LocationCode"],
                                                         "quantity": stock["Qty"],
                                                         "term": None})
        else:
            try:
                data_body = """{"items": "''""" + str(analogs[0].id) + """''"""
            except IndexError:
                return item

            for analog in analogs[1:]:
                data_body += """,''""" + str(analog.id) + "''"
            quantity_request = self.session.post(self.Link.quantity, timeout=self.timeout,
                                                 data=(data_body + """"}""").encode("utf-8"),
                                                 headers={"Content-Type": "text/html; charset=UTF-8"})
            if quantity_request.status_code == 200:
                for stock_ in quantity_request.json():
                    stock = deepcopy(stock_)
                    for analog in analogs:
                        if analog["article"] == stock["ItemNo"]:
                            analog["stocks"].append({"name": stock["LocationCode"],
                                                     "quantity": stock["Qty"],
                                                     "term": None})
        for analog in analogs:
            item.set_analog(analog)

        return item

    def sign_in(self):
        try:
            login_page_request = self.session.get(self.Link.login, timeout=self.timeout)
            assert login_page_request.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return 0, 0
        page_tree = html.fromstring(login_page_request.text.encode("utf-8"))
        token_list = page_tree.xpath("//input[@name='__RequestVerificationToken']/@value")
        if token_list:
            token = token_list[0]
            data_body = "__RequestVerificationToken={0}&ComId={1}&UserName={2}&Password={3}&RememberMe={4}"
            try:
                si_request = self.session.post(self.Link.login, timeout=self.timeout,
                                               headers={"Content-Type": "application/x-www-form-urlencoded"},
                                               data=data_body.format(token, self.companyId, self.username,
                                                                     self.password, "true"))
            except (requests.Timeout, requests.RequestException):
                return 0, 0
            check_authorization_tree = html.fromstring(si_request.text.encode("utf-8"))
            problems = check_authorization_tree.xpath(
                '//div[@class="validation-summary-errors text-danger"]')
            if si_request.status_code == 200 and not problems:
                return 1, 1
            else:
                return 1, 0
        else:
            return 0, 0
