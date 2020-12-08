# coding=utf-8

from parser.types.clients.baseclient import *
from parser.config import loadJSON, Path


class AutoLider(BaseClient):
    """
    AutoLider parser client inherits BaseClient

    Attributes:
        SITE_CONFIG (dict): Client configuration
        name (str): Name of client. Used for response
        username (str): Site account username
        password (str): Site account password
    """

    SITE_CONFIG = loadJSON(
        "config",
        dirpath=Path(__file__).resolve().parent
    )

    name: str = SITE_CONFIG["name"]
    username: str = SITE_CONFIG["username"]
    password: str = SITE_CONFIG["password"]

    class Link:
        """
        Class Link used to store site URL's used for parsing

        Attributes:
            main (str): Main page URL
            parameters (str): Parameters URL

        Notes:
            Links must be formatted or concatenated using item id or other values
        """

        main = "https://online.avtolider-ua.com/"
        parameters = "content.php?PHPSESSID={0}&JsHttpRequest={1}"

    def info(
            self,
            article: str,
            brand: str
    ) -> ResponseInfo.Item:
        """
        Method of getting info. Gets info using specified article and brand and returns response

        Args:
            article (str): Article of item you want to find
            brand (str): Brand of item you want to find

        Returns:
            ResponseInfo.Item: Getting info response
        """

        # Verifying connection

        if not self.connected:
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        if not self.loggedIn:
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NOT_AUTHORIZED
                )
            )

        # Searching request

        searchPayload = "w=makeCatalogueSearch&squery={}&stype=0".format(article)

        try:
            searchRequest = self.post(
                self.Link.main + self.Link.parameters.format(
                    self.PHPSESSID,
                    str(int(time() * 10000)) + "-xml"
                ),
                data=searchPayload,
                timeout=self.timeout,
                headers={
                    "Content-Type": "text/plain"
                }
            )
            assert searchRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # If no items found

        try:
            assert searchRequest.json()["js"]
        except (KeyError, AssertionError):
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_ARTICLE
                )
            )

        searchTree = html.fromstring(searchRequest.json()["js"]["content"])

        if searchTree.xpath('//div[@class="row brand-list"]'):  # Found brands (choose brand)
            # Brands and links
            foundLinks = searchTree.xpath(
                '//div[@class="row brand-list"]//a/@href'
            )
            foundBrands = searchTree.xpath(
                '//div[@class="row brand-list"]//span[@class="logo-name"]/text()'
            )

            # Select brand and get it link

            for foundItemNumber, foundItemBrand in enumerate(foundBrands):
                if self.compareBrands(brand, foundItemBrand):
                    foundItemLink = foundLinks[foundItemNumber]
                    break
            else:
                return ResponseInfo.Item(
                    status=ResponseStatus(
                        ResponseStatus.NO_BRAND
                    )
                )

            # Detailed info

            try:
                detailsRequest = self.get(
                    self.Link.main + foundItemLink[1:],
                    timeout=self.timeout
                )
                assert detailsRequest.status_code == 200

                detailsTree = html.fromstring(detailsRequest.text)
                itemDetails = detailsTree.xpath(
                    '//article[@class="prod-list"]'
                )[0]
            except (requests.Timeout, requests.RequestException, AssertionError, IndexError):
                return ResponseInfo.Item(
                    status=ResponseStatus(
                        ResponseStatus.NO_BRAND
                    )
                )

            # Item detailed info link

            try:
                itemExtendedLink = itemDetails.xpath(
                    '//a[@class="catlink"]/@href'
                )[0]

                extendedDetailsRequest = self.get(
                    self.Link.main + itemExtendedLink[1:],
                    timeout=self.timeout
                )
                assert extendedDetailsRequest.status_code == 200

                detailsTree = html.fromstring(extendedDetailsRequest.text)
                itemDetails = detailsTree.xpath(
                    '//article[@class="product-single"]'
                )[0]
            except (requests.Timeout, requests.RequestException, AssertionError, IndexError):
                return ResponseInfo.Item(
                    status=ResponseStatus(
                        ResponseStatus.NO_BRAND
                    )
                )

        else:  # Found items
            try:
                searchTree = html.fromstring(
                    searchRequest.json()["js"]["content"]
                )
                itemExtendedLink = searchTree.xpath(
                    '//a[@class="catlink"]/@href'
                )[0]

                extendedDetailsRequest = self.get(
                    self.Link.main + itemExtendedLink[1:],
                    timeout=self.timeout
                )
                assert extendedDetailsRequest.status_code == 200

                detailsTree = html.fromstring(extendedDetailsRequest.text)
                itemDetails = detailsTree.xpath('//article[@class="product-single"]')[0]
            except (requests.Timeout, requests.RequestException, AssertionError, IndexError):
                return ResponseInfo.Item(
                    status=ResponseStatus(
                        ResponseStatus.NO_BRAND
                    )
                )

        # Response item

        responseItem = ResponseInfo.Item(
            itemId=article,
            brand=brand,
            article=self.clear(itemDetails.xpath(
                './/div[@class="product-single-title heading-5"]/strong/text()'
            )[0]),
            name=itemDetails.xpath(
                './/h5[@itemprop="name"]/text()'
            )[0],
            price=itemDetails.xpath(
                './/meta[@itemprop="price"]/@content'
            )[0] + " UAH",
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        # Item stocks

        for stockName, stockId, stockTerm in [
            ["Київ", "stor-kv ", 2],
            ["Хмельницький", "stor-km stor-sel", 1],
            ["Експрес", "stor-ex ", 100]
        ]:
            responseItem["stocks"].append({
                "name": stockName,
                "quantity": itemDetails.xpath(
                    f'.//span[@class="{stockId}"]/text()'
                )[0],
                "term": stockTerm
            })

        # Item cross codes

        for crossDetails in detailsTree.xpath('//div[@id="tabs-product-3"]//tr'):
            responseItem["cross"][
                crossDetails.xpath("./td/text()")[0]
            ] = crossDetails.xpath(".//a/text()")

        # Item image saving

        try:
            itemImageLink = itemDetails.xpath(
                './/img[@class="lazyload"]/@src'
            )[0]
            imageName = itemImageLink[itemImageLink.rindex("/") + 1:].replace(".JPG", "").replace(".jpg", "")

            responseItem["image"] = self.getImage(
                self.Link.main[:-1] + itemImageLink,
                imageName
            )
        except IndexError:
            pass
        except OSError:
            responseItem["status"] = ResponseStatus(
                ResponseStatus.NO_MEMORY
            )

        # Item analogs

        for foundAnalog in detailsTree.xpath('//article[@class="prod-list"]'):
            foundAnalogInfo = foundAnalog.xpath(
                './/input[@type="hidden"]/@value'
            )

            # Analog basic info

            analogItem = ResponseInfo.Analog(
                article=foundAnalogInfo[0],
                brand=foundAnalogInfo[2],
                name=foundAnalogInfo[1],
                price=foundAnalogInfo[3] + " UAH"
            )

            # Analog stocks

            for stockName, stockId, stockTerm in [
                ["Київ", "stor-kv ", 2],
                ["Хмельницький", "stor-km stor-sel", 1],
                ["Експрес", "stor-ex ", 100]
            ]:
                analogItem["stocks"].append({
                    "name": stockName,
                    "quantity": foundAnalog.xpath(
                        f'.//span[@class="{stockId}"]/text()'
                    )[0],
                    "term": stockTerm
                })

            # Analog image

            try:
                itemImageLink = foundAnalog.xpath(
                    './/img[@class="lazyload"]/@src'
                )[0]
                imageName = itemImageLink[itemImageLink.rindex("/") + 1:].replace(".JPG", "").replace(".jpg", "")

                analogItem["image"] = self.getImage(
                    self.Link.main + itemImageLink[1:],
                    imageName
                )
            except IndexError:
                pass
            except OSError:
                responseItem["status"] = ResponseStatus(
                    ResponseStatus.NO_MEMORY
                )

            responseItem.setAnalog(analogItem)

        return responseItem

    def signIn(self):
        """
        Authorize client

        Returns:
            Tuple[bool, bool]: Is connected, is authorized
        """

        # Connection verifying

        try:
            loginPageRequest = self.get(
                self.Link.main,
                timeout=self.timeout
            )
            assert loginPageRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return False, False

        # Login attempt

        loginPayload = f"w=singinClient&" \
                       f"login={self.username}&" \
                       f"pass={self.password}&" \
                       f"remember=1"

        loginRequest = self.post(
            self.Link.main + self.Link.parameters.format(
                self.PHPSESSID,
                str(int(time() * 10000)) + "-xml"
            ),
            data=loginPayload,
            timeout=self.timeout,
            headers={
                "Content-Type": "text/plain"
            }
        )

        if loginRequest.status_code == 200:
            return True, not not int(loginRequest.json()["js"]["answer"])

    @property
    def PHPSESSID(self) -> str:
        """
        Pulls "PHPSESSID" cookies from session

        Returns:
            str: "PHPSESSID" cookie value
        """

        try:
            return self.cookies.__dict__["_cookies"]["online.avtolider-ua.com"]["/"]["PHPSESSID"].value
        except KeyError:
            return self.cookies.__dict__["_cookies"][""]["/"]["PHPSESSID"].value
