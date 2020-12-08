# coding=utf-8

from parser.types.clients.baseclient import *
from parser.config import loadJSON, Path


class AsiaParts(BaseClient):
    """
    AsiaParts parser client, inherits BaseClient

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
            login (str): Login page URL
            search (str): Searching URL
            details (str): Part details URL

        Notes:
            Links must be formatted or concatenated using item id or other values
        """

        main = "https://b2b.asiaparts.ua"
        login = "https://b2b.asiaparts.ua/login/"
        search = "https://b2b.asiaparts.ua/index.php?route=product/search&search={}"
        details = "https://b2b.asiaparts.ua/index.php?route=revolution/revpopupview&product_id={}"

    def search(
            self,
            article: str
    ) -> ResponseSearch.List:
        """
        Method of searching. Search items using specified article and returns found items

        Args:
            article (str): Article of item you want to find

        Returns:
            ResponseSearch.List: Searching response

        Notes:
            If an item is found not for specified article, it will be ignored
        """

        # Connection verification

        if not self.connected:
            return ResponseSearch.List(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        if not self.loggedIn:
            return ResponseSearch.List(
                status=ResponseStatus(
                    ResponseStatus.NOT_AUTHORIZED
                )
            )

        # Searching request

        try:
            searchRequest = self.get(
                self.Link.search.format(article),
                timeout=self.timeout
            )
            assert searchRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return ResponseSearch.List(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # Getting results

        searchTree = html.fromstring(searchRequest.text)
        foundItems = searchTree.xpath(
            '//div[@class="row products_category"]/div'
        )

        response = ResponseSearch.List(
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        # Iterating found items

        for foundItem in foundItems:
            # Base item info

            foundItemId = foundItem.xpath(
                './/div[@class="lupa"]/a/@onclick'
            )[0].replace("get_revpopup_view('", "").replace("');", "")

            foundItemInfoRequest = self.get(
                self.Link.details.format(foundItemId),
                headers={
                    "Referer": self.Link.search.format(article),
                    "X-Requested-With": "XMLHttpRequest"
                }
            )

            foundItemInfoTree = html.fromstring(foundItemInfoRequest.text)

            foundItemBrand, foundItemArticle = foundItemInfoTree.xpath(
                '//div[@class="dotted-line_right"]//text()'
            )[:2]

            if not self.compareArticles(article, foundItemArticle):
                continue

            foundItem = ResponseSearch.Item(
                itemId=foundItemId,
                article=foundItemArticle,
                brand=foundItemBrand,
                name=foundItemInfoTree.xpath(
                    '//div[@class="popup-heading"]/text()'
                )[0],
                description=self.clear(
                    " ".join(foundItemInfoTree.xpath(
                        '//div[@class="rev_slider"]/p/text()'
                    ))
                )
            )

            # Item price

            try:
                foundItemPrice = foundItemInfoTree.xpath(
                    '//span[@class="update_price"]/text()'
                )[0]
                assert foundItemPrice
            except (IndexError, AssertionError):
                pass
            else:
                foundItem["price"] = foundItemPrice.replace("$", "") + " USD"

            # Item image saving

            try:
                foundItemImageLink = foundItemInfoTree.xpath(
                    '//img[@class="img-responsive main-image"]/@src'
                )[0]
                foundItem["image"] = self.getImage(
                    foundItemImageLink,
                    imageId=foundItemImageLink.split("/")[-1].split(".")[0]
                )
            except IndexError:
                pass
            except OSError:
                response["status"] = ResponseStatus(
                    ResponseStatus.NO_MEMORY
                )

            # Item stocks

            stocksInfo = foundItemInfoTree.xpath('//div[@class="radio"]//span/text()')
            for stockInfo in stocksInfo:
                stockName, stockQuantity = stockInfo.split(" (")
                try:
                    foundItem["stocks"].append({
                        "name": stockName,
                        "quantity": stockQuantity.replace(" шт.)", ""),
                        "term": None
                    })
                except KeyError:
                    foundItem["stocks"] = [{
                        "name": stockName,
                        "quantity": stockQuantity.replace(" шт.)", ""),
                        "term": None
                    }]

            response.append(foundItem)

        # If no items found, return 'noArticle' status

        if not response:
            response["status"] = ResponseStatus(
                ResponseStatus.NO_ARTICLE
            )

        return response

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

        # Connection verification

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

        try:
            searchRequest = self.get(
                self.Link.search.format(article),
                timeout=self.timeout
            )
            assert searchRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            self._connected = False

            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # Getting results

        searchTree = html.fromstring(searchRequest.text)
        foundItems = searchTree.xpath(
            '//div[@class="row products_category"]/div'
        )

        if not foundItems:
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_ARTICLE
                )
            )

        isFound = False
        responseItem = ResponseInfo.Item(
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        # Iterating found items

        for foundItem in foundItems:
            # Base item info

            foundItemId = foundItem.xpath(
                './/div[@class="lupa"]/a/@onclick'
            )[0].replace("get_revpopup_view('", "").replace("');", "")

            foundItemInfoRequest = self.get(
                self.Link.details.format(foundItemId.replace(
                    "');",
                    "")
                ),
                headers={
                    "Referer": self.Link.search.format(article), "X-Requested-With": "XMLHttpRequest"
                }
            )

            foundItemInfoTree = html.fromstring(foundItemInfoRequest.text)

            foundItemBrand, foundItemArticle = foundItemInfoTree.xpath(
                '//div[@class="dotted-line_right"]//text()'
            )[:2]

            foundItemResponse = ResponseInfo.Analog(
                itemId=foundItemId,
                article=foundItemArticle,
                brand=foundItemBrand,
                name=foundItemInfoTree.xpath(
                    '//div[@class="popup-heading"]/text()'
                )[0],
                description=self.clear(
                    " ".join(foundItemInfoTree.xpath(
                        '//div[@class="rev_slider"]/p/text()'
                    ))
                )
            )

            # Item price

            try:
                foundItemPrice = foundItemInfoTree.xpath(
                    '//span[@class="update_price"]/text()'
                )[0]
                assert foundItemPrice
            except (IndexError, AssertionError):
                pass
            else:
                foundItemResponse["price"] = foundItemPrice.replace("$", "") + " USD"

            # Item image

            try:
                foundItemImageLink = foundItemInfoTree.xpath(
                    '//img[@class="img-responsive main-image"]/@src'
                )[0]
                foundItemResponse["image"] = self.getImage(
                    foundItemImageLink,
                    imageId=foundItemImageLink.split("/")[-1].split(".")[0]
                )
            except IndexError:
                pass
            except OSError:
                responseItem["status"] = ResponseStatus(
                    ResponseStatus.NO_MEMORY
                )

            # Item stocks

            stocksInfo = foundItemInfoTree.xpath('//div[@class="radio"]//span/text()')

            for stockInfo in stocksInfo:
                stockName, stockQuantity = stockInfo.split(" (")
                foundItemResponse["stocks"].append({
                    "name": stockName,
                    "quantity": stockQuantity.replace(" шт.)", ""),
                    "term": None
                })

            # Add to analogs if item was found already

            if self.compareBrands(brand, foundItemBrand) and not isFound:
                isFound = True
                responseItem.update(
                    foundItemResponse
                )
            else:
                responseItem.setAnalog(foundItemResponse)

        # If no item found, then return first analog

        if not isFound:
            responseItem.update(
                responseItem["analogs"].pop(0)
            )

        return responseItem

    def signIn(self) -> Tuple[bool, bool]:
        """
        Authorize client

        Returns:
            Tuple[bool, bool]: Is connected, is authorized
        """

        # Connection verification

        try:
            mainPageRequest = self.get(
                self.Link.main,
                timeout=self.timeout
            )
            assert mainPageRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return False, False

        # Login attempt

        loginData = {
            "email": (None, self.username),
            "password": (None, self.password)
        }

        loginRequest = self.post(
            self.Link.login,
            files=loginData,
            headers={
                "Referer": self.Link.login,
                "Origin": self.Link.main
            }
        )

        return True, loginRequest.status_code == 200
