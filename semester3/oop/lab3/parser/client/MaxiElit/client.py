# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class MaxiElit(Client):
    class Link:
        main = "https://maxi.ecat.ua/"
        cart = "https://maxi.ecat.ua/api/desktop/v1/locales/" \
               "?limit=1000&offset=0&language_code=ru&msgid__startswith=maxi "
        login = "https://maxi.ecat.ua/api/desktop/v1/auth-login/"
        search = "https://maxi.ecat.ua/products/search/{0}/type:article"
        getSearchResults = "https://maxi.ecat.ua/api/desktop/v1/ecat-search/?q={0}&type=article"
        info = "https://maxi.ecat.ua/api/desktop/v1/products/{0}/"
        price = "https://maxi.ecat.ua/api/desktop/v1/product-price-on-click/{0}/"
        oe = "https://maxi.ecat.ua/api/desktop/v1/product-numbers/?product_id={0}&limit={1}&offset=0"
        usedIn = "https://maxi.ecat.ua/api/desktop/v1/used-in-vehicles/?erp_id={0}&limit={1}&offset=0"
        referer = "https://maxi.ecat.ua/product/detail/{0}/context:0"
        analogs = "https://maxi.ecat.ua/api/desktop/v1/product-substitutions/{0}/"
        analogsInfo = "https://maxi.ecat.ua/api/desktop/v1/products/set/"

    name = "maxielit"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]

        self.oe_limit = SITE_CONFIG["crossLimit"]
        self.using_limit = SITE_CONFIG["usingLimit"]

        self.temp_file = Path(__file__).resolve().parent / "maxielit.tmp"

        self.hex_list = [hex(i)[2:] for i in range(16)]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def get_info(self, article, brand):
        def get_item_by_id(erp_id):
            get_info_request = self.session.get(self.Link.info.format(erp_id), timeout=self.timeout,
                                                headers={"Referer": self.Link.search.format(article)})
            if get_info_request.status_code == 200:
                response = get_info_request.json()
                item_ = ResponseItem(item_id=response["id"])
                price_request = self.session.get(self.Link.price.format(erp_id), timeout=self.timeout,
                                                 headers={"Referer": self.Link.search.format(article)})
                if price_request.status_code == 200:
                    price = price_request.json()["price_vat"].replace(" ", "").replace(",", ".")
                    item_["price"] = price.replace("грн.", " UAH")
                    item_["stocks"] = [{"name": stock["branch"],
                                        "quantity": stock["quantity"],
                                        "term": None} for stock in response["full_availability"]]
                    item_["article"] = response["active_number"]
                    item_["brand"] = response["elitsupplier"]["name"]
                    item_["description"] = response["extendeddescription_pretext"]
                    item_["name"] = response["description"]
                    try:
                        image_link = response["main_image"]["uri_large"]
                    except TypeError:
                        item_["image"] = None
                    else:
                        item_["image"] = self.get_image(image_link, "{0}.jpg".format(item_.id))

                    get_numbs_request = self.session.get(self.Link.oe.format(item_.id, self.oe_limit),
                                                         timeout=self.timeout,
                                                         headers={"Referer": self.Link.referer.format(item_.id)})
                    if get_numbs_request.status_code == 200:
                        item_["cross"] = {}
                        for oe_info in get_numbs_request.json()["objects"]:
                            try:
                                item_["cross"][oe_info["name"]].append(oe_info["number"])
                            except KeyError:
                                item_["cross"][oe_info["name"]] = [oe_info["number"]]
                    get_using_request = self.session.get(self.Link.usedIn.format(erp_id, self.using_limit),
                                                         timeout=self.timeout,
                                                         headers={"Referer": self.Link.referer.format(item_.id)})
                    if get_using_request.status_code == 200:
                        item_["using"] = {}
                        for using in get_using_request.json()["objects"]:
                            autobrand = using["brand"]["name"]
                            model = using["vehiclemodel"]["name"]
                            try:
                                item_["using"][autobrand].append(model)
                            except KeyError:
                                item_["using"][autobrand] = [model]
                    return 0, "OK", item_
            return 2, "Помилка з'єднання", None

        if self.logged and self.connected:
            get_search_results = self.session.get(self.Link.getSearchResults.format(article), timeout=self.timeout,
                                                  headers={"Referer": self.Link.search.format(article)})
            if get_search_results.status_code == 200:
                result = get_search_results.json()
                objects = result["objects"]
                if objects:
                    for item in objects:
                        supplier = item["elitsupplier"]["name"]
                        if self.compare(supplier, brand):
                            erp_id = item["erp_id"]
                            break
                    else:
                        return self.response_brand(1, "Бренд не знайдено")
                    code, description, item = get_item_by_id(erp_id)
                    if code:
                        return self.response_brand(code, description)
                    analog_request = self.session.get(self.Link.analogs.format(erp_id), timeout=self.timeout,
                                                      headers={"Referer": self.Link.referer.format(item.id)})
                    try:
                        analogs = [analog_[:-1].split("/")[-1] for analog_ in analog_request.json()["substitutions"]]
                    except IndexError:
                        pass
                    else:
                        for analog in analogs:
                            item.set_analog(get_item_by_id(analog)[2])
                        # analog_info_request = self.session.get(self.Link.analogsInfo + ";".join(analogs),
                        #                                        timeout=self.timeout,
                        #                                        headers={"Referer": self.Link.referer.format(item.id)})
                        # for analog_item in analog_info_request.json()["objects"]:
                        #     analog_ = ResponseItem(item_id=0,
                        #                            article=analog_item["active_number"],
                        #                            brand=analog_item["elitsupplier"]["name"],
                        #                            name=analog_item["description"],
                        #                            desc=analog_item["extendeddescription_pretext"],
                        #                            price=analog_item["price"])
                        #     try:
                        #         image_request = self.session.get(analog_item["main_image"]["uri_large"], verify=False,
                        #                                          timeout=self.timeout)
                        #         assert image_request.status_code == 200
                        #     except (requests.Timeout, requests.RequestException, AssertionError, TypeError):
                        #         pass
                        #     else:
                        #         if self.imageType:
                        #             analog_["image"] = CONFIG["parser"]["picturesPath"].format(self.name) +\
                        #                                "{0}.jpg".format(analog_item["main_image"]["product_id"])
                        #             with open(analog_["image"], "wb") as image_file:
                        #                 image_file.write(image_request.content)
                        #         else:
                        #             analog_["image"] = image_request.content
                        #     item.set_analog(analog_)
                    return self.response_brand(0, "OK", item=item)
                else:
                    return self.response_brand(1, "Артикул не знайдено")
            elif get_search_results.status_code in (401, 403):
                connected, logged = self.sign_in(call=0)
                if connected and logged:
                    return self.get_info(article, brand)
                elif connected:
                    return self.response_brand(3, "Помилка авторизації")
                else:
                    return self.response_brand(2, "Помилка з'єдання")
            return self.response_brand(2, "Помилка з'єдання")
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єдання")

    def __generate_uuid(self):
        temp_uuid = ""
        for length in [8, 4, 4, 4, 12]:
            for number in range(length):
                temp_uuid += choice(self.hex_list)
            temp_uuid += "-"
        return temp_uuid[:-1]

    def __get_headers(self, javascript, uuid=None):
        if uuid is None:
            uuid = self.__generate_uuid()
        try:
            search_text = javascript[javascript.index("ApiKey RGL_MAXI"):]
            api_key = search_text[:search_text.index('"')]
        except ValueError:
            return None
        try:
            search_text = javascript[javascript.index("try_hard:") + 10:]
            try_hard = search_text[:search_text.index('"')]
        except ValueError:
            return None
        try:
            search_text = javascript[javascript.index("UUID:") + 8:]
            header_name = search_text[:search_text.index('"')]
        except ValueError:
            return None
        header_value = md5((try_hard + uuid).encode("utf-8")).hexdigest()
        return {"Authorization": api_key, "uuid": uuid, header_name: header_value}

    def sign_in(self):
        try:
            get_main_page = self.session.get(self.Link.main, timeout=self.timeout)
            assert get_main_page.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return 0, 0
        main_page_tree = html.fromstring(get_main_page.text.encode("utf-8"))
        javascript_link = main_page_tree.xpath("//script/@src")[0]
        try:
            get_javascript = self.session.get(self.Link.main[:-1] + javascript_link, timeout=self.timeout)
            assert get_javascript.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return 0, 0
        if self.temp_file.exists():
            with self.temp_file.open("wb") as js_file:
                js_file.write(get_javascript.content)
                js_file.close()
        required_headers = self.__get_headers(get_javascript.content.decode("utf-8")[500000:1000000])
        if required_headers is None:
            return 1, 0
        else:
            self.session.headers.update(required_headers)
            try:
                get_cookies = self.session.get(self.Link.cart, timeout=self.timeout)
                assert get_cookies.status_code == 200
            except (requests.Timeout, requests.RequestException, AssertionError):
                return 1, 0
            login_data = {"username": self.username,
                          "password": self.password,
                          "permanent_login": "on"}
            try:
                sign_in_request = self.session.post(self.Link.login, json=login_data, timeout=self.timeout,
                                                    headers={"Content-Type": "application/json"})
                assert sign_in_request.status_code == 200
            except (requests.RequestException, requests.Timeout, AssertionError):
                return 1, 0
            return 1, 1
