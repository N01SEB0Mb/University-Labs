# coding=utf-8

from parser.client import *
from parser.client.ResponseItem import *


with (Path(__file__).resolve().parent / "config.json").open("rt") as siteConfigFile:
    SITE_CONFIG = json.load(siteConfigFile)


class InterCars(Client):
    class Link:
        main = "https://ic-ua.intercars.eu/"
        login = "https://ic-ua.intercars.eu/dynamic/uni/ws_login.php?x=1"
        login_status = "https://ic-ua.intercars.eu/dynamic/uni/ws_login_status.php?x=1"
        search = "https://ic-ua.intercars.eu/dynamic/uni/ws_towary.php?wit=ICKATALOGWEB&pro=&kraj=UA&oesearch={}&ofe="
        details = "https://ic-ua.intercars.eu/dynamic/uni/ws_towDetail.php?wit=ICKATALOGWEB&p=F"
        price = "https://ic-ua.intercars.eu/dynamic/ickatalogweb/ws_getsoap.php?towkod={}&call=dkc&cen=HB-DB-HN-DN&qty=1&sta=T&fir=UM1&gru=|"
        stocks = "https://ic-ua.intercars.eu/dynamic/ickatalogweb/ws_sta.php?towkod={}&wit=ICKATALOGWEB&src=na&popup=T"
        cross = "https://ic-ua.intercars.eu/dynamic/ickatalogweb/ws_getsoap.php?call=numoe&art={}&wit=ICKATALOGWEB"
        using = "https://ic-ua.intercars.eu/dynamic/ickatalogweb/ws_getsoap.php?call=stos&art={}&wit=ICKATALOGWEB"
        analogs = "https://ic-ua.intercars.eu/dynamic/ickatalogweb/ws_zamienniki.php?popup=T&firgru=|&towkod={}&zakres=all"

    name = "intercars"

    def __init__(self):
        super().__init__()

        self.username = SITE_CONFIG["username"]
        self.password = SITE_CONFIG["password"]
        self.cartNumber = SITE_CONFIG["cartNumber"]

        # encrypted login info
        self.kh_kod = SITE_CONFIG["kh_kod"]
        self.kh_ksk = SITE_CONFIG["kh_ksk"]
        self.kh_has = SITE_CONFIG["kh_has"]

        start_time = time()
        self.connected, self.logged = self.sign_in()
        self.login_time = "%.3f s" % (time() - start_time)

    def get_info(self, article, brand):
        if self.connected and self.logged:
            search_data = {"oesearch": article.replace(" ", "")}
            search_request = self.session.post(self.Link.search.format(article.replace(" ", "")), data=search_data,
                                               headers={"Content-Type": "application/x-www-form-urlencoded",
                                                        "Referer": self.Link.main})
            if search_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання")
            html_tree = html.fromstring(search_request.content)
            found_items = html_tree.xpath('//div[@class="tecdocSecRow"]/div[3]/@onclick')
            if not found_items:
                return self.response_brand(1, "Артикул не знайдено")
            item_global_stocks = html_tree.xpath("""//div[@onmouseover="tdHintShow('DOSTEPNOSC_OFFLINE');"]/text()""")
            item_local_stocks = html_tree.xpath("""//div[@onmouseover="tdHintShow('DOST_W_ODDZIELE');"]/text()""")
            for number, found_item in enumerate(found_items):
                item_info = eval(found_item.replace("Daj_Katalog_Detail_Clob(", "").replace(");", ""))
                item_br_ls = html_tree.xpath('//div[@id="span{}_{}pp"]//nobr/text()'.format(item_info[1], item_info[4]))
                item_brand = item_br_ls[0].replace("\xa0", "")
                if self.compare_art(article, item_info[0]) and self.compare(brand, item_brand):
                    item = ResponseItem(item_id=item_info[9], article=item_info[0], brand=item_brand, stocks=[
                        {"name": "Наявність Offline",
                         "quantity": item_global_stocks[number],
                         "term": None},
                        {"name": "Offline доступність у вашому відділені",
                         "quantity": item_local_stocks[number],
                         "term": None}
                    ])
                    break
            else:
                return self.response_brand(1, "Бренд не знайдено")
            item_details_request = self.session.post(self.Link.details, data={
                "artnr": item_info[0],
                "pro": item_info[1],
                "typ": item_info[2],
                "wsk": item_info[3],
                "gen": item_info[4],
                "kraj": item_info[5],
                "witryna": item_info[6],
                "lang": item_info[7],
                "nb": item_info[8],
                "towkod": item_info[9]
            }, headers={"Content-Type": "application/x-www-form-urlencoded",
                        "Referer": self.Link.search.format(article.replace(" ", ""))})
            if item_details_request.status_code != 200:
                return self.response_brand(2, "Помилка з'єднання (додаткова інформація про товар)")
            item_price = self.session.get(self.Link.price.format(item_info[9]))
            item_details = html.fromstring(item_details_request.text)
            item["price"] = item_price.text.split("^")[0].replace(",", ".") + " UAH"
            item["name"] = item_details.xpath('//h3/b/text()')[0]
            item["description"] = item_details.xpath("//title/text()")[0]
            item["image"] = self.get_image(self.Link.main[:-1] + item_details.xpath("//img/@src")[9], item["article"])

            item_stocks_request = self.session.post(self.Link.stocks.format(item.id))
            if item_stocks_request.status_code == 200:
                stocks_tree = html.fromstring(item_stocks_request.text)
                stocks_name = stocks_tree.xpath('//div[@id="dStanyOnline"]/text()')
                stocks_quantity = stocks_tree.xpath('//div[@id="dStanyOnlineBold"]/text()')
                for number, stock_name in enumerate(stocks_name):
                    item["stocks"].append({
                        "name": stock_name,
                        "quantity": stocks_quantity[number].replace(" шт. ", ""),
                        "term": None
                    })

            try:
                oe_article_text = item_details_request.text[item_details_request.text.index("daj_numeryOE('") + 14:]
                oe_article = oe_article_text[:oe_article_text.index("'")]
            except ValueError:
                pass
            else:
                oe_request = self.session.post(self.Link.cross.format(oe_article))
                oe_tree = html.fromstring(oe_request.text)
                if oe_request.status_code == 200:
                    oe_codes = oe_tree.xpath('//div[@style="float:left;width:250px;"]/text()')
                    oe_brands = oe_tree.xpath('//div[@id="dZastosowanieModel"]/text()')[1:]
                    for number, oe_brand in enumerate(oe_brands):
                        try:
                            item["cross"][self.clear(oe_brand)].append(self.clear(oe_codes[number]))
                        except KeyError:
                            item["cross"][self.clear(oe_brand)] = [self.clear(oe_codes[number])]

                using_request = self.session.post(self.Link.using.format(oe_article))
                using_tree = html.fromstring(using_request.text)
                if using_request.status_code == 200:
                    using_brands = using_tree.xpath('//div[@class="dZB1"]/u/text()')
                    using_models = using_tree.xpath('//div[@class="dZM2"]')
                    for number, using_brand in enumerate(using_brands):
                        model_names = using_models[number].xpath('.//div[@class="dZB2"]/u/text()')
                        model_variations = using_models[number].xpath('.//div[@class="dZT2"]')
                        for model_number, model_name in enumerate(model_names):
                            model_variants = model_variations[model_number].xpath('.//span[@class="dZOn"]/u/text()')
                            for model_variant in model_variants:
                                try:
                                    item["using"][using_brand].append(model_name + model_variant)
                                except KeyError:
                                    item["using"][using_brand] = [model_name + model_variant]

            analogs_request = self.session.get(self.Link.analogs.format(item.id))
            if analogs_request.status_code == 200:
                analogs_tree = html.fromstring(analogs_request.text)
                analogs = analogs_tree.xpath('//tbody/tr')[1:]

                for analog in analogs:
                    analog_item = ResponseItem(
                        article=self.clear(analog.xpath('.//td[@class="smallFontBold  FontRed"]/b/text()')[0]),
                        brand=self.clear(analog.xpath('.//td[@class="att-right"]/b/text()')[0]),
                        name=self.clear(analog.xpath('.//td[@class="att-right"]/span/text()')[0]),
                        price=self.clear(analog.xpath('.//span[@class="cHurt"]/text()')[0])
                    )

                    stocks = analog.xpath('.//span[@class="dostepnosczam smallFontBold FontRed"]')
                    for stock in stocks:
                        analog_item["stocks"].append({
                            "name": self.clear(stock.xpath('./@title')[0]),
                            "quantity": stock.xpath('./text()')[0].replace(" \xa0шт.", ""),
                            "term": None
                        })

                    item.set_analog(analog_item)

            return self.response_brand(0, "Ok", item=item)
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    def sign_in(self):
        try:
            get_main_page = self.session.get(self.Link.main, timeout=self.timeout)
            assert get_main_page.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return 0, 0
        phpsessid = self.session.cookies.__dict__["_cookies"]["ic-ua.intercars.eu"]["/"]["PHPSESSID"].value
        login_payload = {
            "kh_kod": self.kh_kod,
            "kh_ksk": self.kh_ksk,
            "kh_has": self.kh_has,
            "phpsessid": phpsessid
        }
        login_request = self.session.post(self.Link.login, data=login_payload,
                                          headers={"Content-Type": "application/x-www-form-urlencoded",
                                                   "Referer": self.Link.main})
        self.session.cookies.set("khkod", self.username, expires=int(time()) + 1000000)
        login_status_request = self.session.post(self.Link.login_status, data={"phpsessid": phpsessid},
                                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                                          "Referer": self.Link.main})
        if login_status_request.status_code == 200:
            if login_status_request.text == "1":
                return 1, 1
        return 1, 0
