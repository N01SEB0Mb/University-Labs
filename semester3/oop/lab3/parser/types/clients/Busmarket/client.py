# coding=utf-8

from parser.types.clients.baseclient import *
from parser.config import loadJSON, Path


class Busmarket(BaseClient):
    """
    Busmarket parser client, inherits BaseClient

    Attributes:
        SITE_CONFIG (dict): Client configuration
        name (str): Name of client. Used for response
        username (str): Site account username
        password (str): Site account password
        token (str): Site API token
        currencyId (str): API currencyId
    """

    SITE_CONFIG = loadJSON(
        "config",
        dirpath=Path(__file__).resolve().parent
    )

    name: str = SITE_CONFIG["name"]
    username: str = SITE_CONFIG["username"]
    password: str = SITE_CONFIG["password"]
    token: str = SITE_CONFIG["token"]
    currencyId: str = SITE_CONFIG["currencyId"]

    class Link:
        """
        Class Link used to store site URL's used for parsing

        Attributes:
            search (str): URL for searching
            stocks (str): Stocks URL
            product (str): Item info URL
            searchBrand (str): URL for searching with brand
            image (str): Image URL

        Notes:
            Links must be formatted or concatenated using item id or other values
        """

        search = "https://api.bm.parts/search/products?q={0}&currency={1}"
        stocks = "https://api.bm.parts/product/{0}/in_stocks"
        product = "https://api.bm.parts/product/{0}"
        searchBrand = "https://api.bm.parts/search/products?q={0}&brands={1}"
        image = "https://cdn.bm.parts/photos/1920x1920"
        currencies = "https://api.bm.parts/finance/currencies/rates"

    def __init__(
            self,
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        Initializes Busmarket object and adds token to headers

        Args:
            *args (Any): requests.Session args
            **kwargs (Any): requests.Session kwargs
        """

        super(Busmarket, self).__init__(
            *args,
            **kwargs
        )

        self.headers.update({"Authorization": self.token})

    def info(self, article, brand):
        """
        Method of getting info. Gets info using specified article and brand and returns response

        Args:
            article (str): Article of item you want to find
            brand (str): Brand of item you want to find

        Returns:
            ResponseInfo.Item: Getting info response
        """

        # Searching article

        article = article.replace(" ", "")
        searchRequest = self.get(
            self.Link.search.format(
                article,
                self.currencyId
            )
        )

        # Verifying connection

        if searchRequest.status_code != 200:
            self._connected = False

            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # If no items found

        if not searchRequest.json()["products"].keys():
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_ARTICLE
                )
            )

        # Searching matching brand

        for key in searchRequest.json()["products"].keys():
            itemBrand = searchRequest.json()["products"][key]["brand"]

            # If brand matching

            if self.compareBrands(
                    brand,
                    itemBrand
            ):
                responseItem = ResponseInfo.Item(
                    itemId=key,
                    status=ResponseStatus(
                        ResponseStatus.SUCCESS
                    )
                )
                break
        else:
            # If no matching brand found

            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_BRAND
                )
            )

        # Product info requesting

        try:
            productRequest = self.get(
                self.Link.product.format(responseItem.id)
            )
            assert productRequest.status_code == 200

            productInfo = productRequest.json()["product"]
        except (AssertionError, KeyError):
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NOT_FOUND,
                    description="ID not found"
                )
            )
        else:
            productInfo["price"] = productInfo["price"] + " UAH"

        # Item basic info

        for infoKey in [
            "article",
            "brand",
            "name",
            "price"
        ]:
            responseItem[infoKey] = productInfo[infoKey]

        # Item image

        try:
            responseItem["image"] = self.getImage(
                self.Link.image + productInfo["default_image"].replace("photo", "").replace("\\", "/"),
                responseItem.id
            )
        except KeyError:
            pass
        except OSError:
            responseItem["status"] = ResponseStatus(
                ResponseStatus.NO_MEMORY
            )

        # Item stocks

        responseItem["stocks"] = list(self.__getStocks(responseItem.id))
        responseItem["stocks"].append({
            "name": "Ожидается",
            "quantity": productInfo["in_waiting"]["quantity"],
            "term": None
        })

        # Item using info

        for car in productInfo["cars"]:
            for model in car["models"]:
                for engine in model["engines"]:
                    usingBrand = car["brand"]
                    usingModel = model["model"] + " (" + engine["engine"] + ")"

                    if usingBrand in responseItem["using"]:
                        responseItem["using"][usingBrand].append(usingModel)
                    else:
                        responseItem["using"][usingBrand] = [usingModel]

        # Item analogs

        for analogUUID in productInfo["analogs"]:
            # Analog basic info

            productInfo["analogs"][analogUUID]["price"] += " UAH"

            analogItem = ResponseInfo.Analog(
                itemId=analogUUID
            )

            for infoKey in [
                "article",
                "brand",
                "name",
                "price"
            ]:
                analogItem[infoKey] = productInfo["analogs"][analogUUID][infoKey]

            # Analog stocks

            analogItem["stocks"] = list(self.__getStocks(analogUUID))
            analogItem["stocks"].append({
                "name": "Ожидается",
                "quantity": productInfo["analogs"][analogUUID]["in_waiting"]["quantity"],
                "term": None
            })

            try:
                analogItem["image"] = self.getImage(
                    self.Link.image + productInfo["analogs"][analogUUID]
                    ["default_image"].replace("photo", "").replace("\\", "/"),
                    analogUUID
                )
            except KeyError:
                pass
            except OSError:
                responseItem["status"] = ResponseStatus(
                    ResponseStatus.NO_MEMORY
                )

            responseItem.setAnalog(analogItem)

        # Returning result

        return responseItem

    def __getStocks(
            self,
            itemUUID: str
    ) -> Generator[dict, None, None]:
        """
        Get stocks for specified item

        Args:
            itemUUID (str): Item UUID

        Yields:
            dict: Item stocks info
        """

        # Requesting stocks

        stocksRequest = self.get(
            self.Link.stocks.format(itemUUID)
        )

        # Checking connection success

        if stocksRequest.status_code == 200:
            # Processing stocks

            for stockInfo in stocksRequest.json()["in_stocks"]:
                stockType = lambda typeId: stockInfo["contract_quantities"][typeId]["quantity"]
                quantityPref = ">" if ">" in stockType(0) or ">" in stockType(1) else ""

                # Yielding result

                yield {
                    "name": stockInfo["name"],
                    "quantity": quantityPref + str(
                        int(stockType(0).replace("-", "0").replace(">", "")) +
                        int(stockType(1).replace("-", "0").replace(">", ""))
                    ),
                    "term": None
                }

    def currency(self) -> ResponseCurrency.List:
        """
        Method of getting currency

        Returns:
            ResponseCurrency.List: Getting currency response
        """

        # Currency request

        currencyRequest = self.get(self.Link.currencies)

        if currencyRequest.status_code == 403:
            return ResponseCurrency.List(
                status=ResponseStatus(
                    ResponseStatus.NOT_AUTHORIZED,
                    description="Wrong API-key"
                )
            )
        elif currencyRequest.status_code != 200:
            return ResponseCurrency.List(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # Currency response item

        response = ResponseCurrency.List(
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        for currency in currencyRequest.json()["rates"]:
            if currency["currency_name"] in self.currencies:
                response.append(
                    ResponseCurrency.Currency(
                        name=currency["currency_name"],
                        price=round(currency["rate"], 2)
                    )
                )

        return response
