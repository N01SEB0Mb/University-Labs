# coding=utf-8

from parser.client.Client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class AutoLider(Client):
    class Link:
        main = "https://online.avtolider-ua.com/"
        parameters = "content.php?PHPSESSID={0}&JsHttpRequest={1}"

    name = "autolider"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def get_info(self, article, brand):
        if self.connected and self.logged:
            # try:
            #     if not article[0].isdigit() and not article[1].isdigit() and article[2] == " ":
            #         article = article[2:]
            # except IndexError:
            #     pass
            search_payload = "w=makeCatalogueSearch&squery={}&stype=0".format(article)
            try:
                search_request = self.session.post(self.Link.main + self.Link.parameters.format(
                    self.session.cookies.__dict__["_cookies"]["online.avtolider-ua.com"]["/"]["PHPSESSID"].value,
                    str(int(time() * 10000)) + "-xml"), data=search_payload, timeout=self.timeout,
                                                   headers={"content-type": "text/plain"})
            except KeyError:
                search_request = self.session.post(self.Link.main + self.Link.parameters.format(
                    self.session.cookies.__dict__["_cookies"][""]["/"]["PHPSESSID"].value,
                    str(int(time() * 10000)) + "-xml"), data=search_payload, timeout=self.timeout,
                                                   headers={"content-type": "text/plain"})
            if search_request.json()["js"]:
                search_tree = html.fromstring(search_request.json()["js"]["content"])
                if search_tree.xpath('//div[@class="row brand-list"]'):  # choose brand
                    item_links = search_tree.xpath('//div[@class="row brand-list"]//a/@href')
                    item_brands = search_tree.xpath('//div[@class="row brand-list"]//span[@class="logo-name"]/text()')
                    for item_number, item_brand in enumerate(item_brands):
                        if self.compare(brand, item_brand):
                            item_link = item_links[item_number]
                            break
                    else:
                        return self.response_brand(1, "Бренд не знайдено")
                    try:
                        details_request = self.session.get(self.Link.main + item_link[1:], timeout=self.timeout)
                        details_tree = html.fromstring(details_request.text)
                        item_details = details_tree.xpath('//article[@class="prod-list"]')[0]
                        assert details_request.status_code == 200
                    except:
                        return self.response_brand(1, "Бренд не знайдено")
                    try:
                        item_extended_link = item_details.xpath('//a[@class="catlink"]/@href')[0]
                        extended_details_request = self.session.get(self.Link.main + item_extended_link[1:],
                                                                    timeout=self.timeout)
                        details_tree = html.fromstring(extended_details_request.text)
                        item_details = details_tree.xpath('//article[@class="product-single"]')[0]
                        assert extended_details_request.status_code == 200
                    except:
                        return self.response_brand(1, "Бренд не знайдено")

                else:  # details
                    try:
                        search_tree = html.fromstring(search_request.json()["js"]["content"])
                        item_extended_link = search_tree.xpath('//a[@class="catlink"]/@href')[0]
                        extended_details_request = self.session.get(self.Link.main + item_extended_link[1:],
                                                                    timeout=self.timeout)
                        details_tree = html.fromstring(extended_details_request.text)
                        item_details = details_tree.xpath('//article[@class="product-single"]')[0]
                        assert extended_details_request.status_code == 200
                    except:
                        return self.response_brand(1, "Бренд не знайдено")
                item = ResponseItem(item_id=article)
                item["article"] = self.clear(
                    item_details.xpath('.//div[@class="product-single-title heading-5"]/strong/text()')[0])
                item["name"] = item_details.xpath('.//h5[@itemprop="name"]/text()')[0]
                item["price"] = item_details.xpath('.//meta[@itemprop="price"]/@content')[0] + " UAH"
                item["brand"] = brand
                item["stocks"] = [
                    {"name": "Київ",
                     "quantity": item_details.xpath('.//span[@class="stor-kv "]/text()')[0],
                     "term": 2},
                    {"name": "Хмельницький",
                     "quantity": item_details.xpath('.//span[@class="stor-km stor-sel"]/text()')[0],
                     "term": 1},
                    {"name": "Експрес",
                     "quantity": item_details.xpath('.//span[@class="stor-ex "]/text()')[0],
                     "term": 100}
                ]
                item["cross"] = dict()
                for cross_details in details_tree.xpath('//div[@id="tabs-product-3"]//tr'):
                    item["cross"][cross_details.xpath("./td/text()")[0]] = cross_details.xpath(".//a/text()")
                image_link = item_details.xpath('.//img[@class="lazyload"]/@src')[0]
                image_name = image_link[image_link.rindex("/") + 1:].replace(".JPG", "").replace(".jpg", "")
                item["image"] = self.get_image(self.Link.main + image_link[1:], image_name)

                for analog_item in details_tree.xpath('//article[@class="prod-list"]'):
                    analog = ResponseItem()
                    analog_info = analog_item.xpath('.//input[@type="hidden"]/@value')
                    analog["article"] = analog_info[0]
                    analog["name"] = analog_info[1]
                    analog["brand"] = analog_info[2]
                    analog["price"] = analog_info[3] + " UAH"
                    analog["stocks"] = [
                        {"name": "Київ",
                         "quantity": analog_item.xpath('.//span[@class="stor-kv "]/text()')[0],
                         "term": 2},
                        {"name": "Хмельницький",
                         "quantity": analog_item.xpath('.//span[@class="stor-km stor-sel"]/text()')[0],
                         "term": 1},
                        {"name": "Експрес",
                         "quantity": analog_item.xpath('.//span[@class="stor-ex "]/text()')[0],
                         "term": 100}
                    ]
                    image_link = analog_item.xpath('.//img[@class="lazyload"]/@src')[0]
                    image_name = image_link[image_link.rindex("/") + 1:].replace(".JPG", "").replace(".jpg", "")
                    analog["image"] = self.get_image(self.Link.main + image_link[1:], image_name)
                    item.set_analog(analog)
                return self.response_brand(0, "OK", item)
            else:
                return self.response_brand(1, "Артикул не знайдено")
            return self.response_brand(0, "OK")
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        try:
            login_page_req = self.session.get(self.Link.main, timeout=self.timeout)
            assert login_page_req.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return 0, 0
        login_payload = "w=singinClient&login={0}&pass={1}&remember=1".format(self.username, self.password)
        login_request = self.session.post(self.Link.main + self.Link.parameters.format(
            self.session.cookies.__dict__["_cookies"]["online.avtolider-ua.com"]["/"]["PHPSESSID"].value,
            str(int(time() * 10000)) + "-xml"
        ), data=login_payload, headers={"content-type": "text/plain"}, timeout=self.timeout)
        if login_request.status_code == 200:
            return 1, int(login_request.json()["js"]["answer"])
