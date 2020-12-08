# coding=utf-8

from parser.types.clients.baseclient import *
from parser.config import loadJSON, Path


class Direct24(BaseClient):
    """
    Direct24 parser client, inherits BaseClient

    Attributes:
        SITE_CONFIG (dict): Client configuration
        name (str): Name of client. Used for response
        username (str): Site account username
        password (str): Site account password
        passwordAPI (str): Site API password
    """

    SITE_CONFIG = loadJSON(
        "config",
        dirpath=Path(__file__).resolve().parent
    )

    name: str = SITE_CONFIG["name"]
    username: str = SITE_CONFIG["username"]
    password: str = SITE_CONFIG["password"]
    passwordAPI: str = SITE_CONFIG["apiPassword"]

    class Link:
        """
        Class Link used to store site URL's used for parsing

        Attributes:
            main (str): API URL
            login (str): Login page URL
        """

        main = "https://direct24.com.ua/"
        mainAPI = "https://direct24.com.ua/ws/json/"
        login = "https://direct24.com.ua/users/login/?next=/"

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

        # Searching request

        try:
            searchRequest = self.post(
                self.Link.mainAPI,
                timeout=self.timeout,
                data={
                    "login": self.username,
                    "password": self.passwordAPI,
                    "partnumber": article,
                    "manufacturer": brand,
                    "analogs": "on"
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            assert searchRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            self._connected = False

            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # Check if any items were found

        try:
            assert len(searchRequest.json()[2])
        except (AssertionError, IndexError, TypeError):
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_ARTICLE
                )
            )

        # Response variables

        responseItem = ResponseInfo.Item(
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        usedAnalogsList = []

        # Iterating found items

        for foundItem in searchRequest.json()[2]:
            if responseItem["article"] == "" and self.compareArticles(
                    article,
                    foundItem["PartCleanNumber"]
            ) and self.compareBrands(
                brand,
                foundItem["Manufacturer"]
            ):  # Found given item
                # Basic item info

                responseItem["article"] = foundItem["PartCleanNumber"]
                responseItem["brand"] = foundItem["Manufacturer"]
                responseItem["price"] = foundItem["Price"] + " EUR"
                responseItem["name"] = foundItem["PartName"]
                responseItem["description"] = foundItem["PartDescription"]

                # Item stocks

                if "-" in foundItem["DeliveryDays"]:
                    stockTerm = int(foundItem["DeliveryDays"].split("-")[1])
                else:
                    stockTerm = int(foundItem["DeliveryDays"])

                responseItem["stocks"].append({
                    "name": str(foundItem["StoreID"]),
                    "quantity": foundItem["Quantity"],
                    "term": stockTerm + 2
                })

            elif responseItem["article"] == foundItem["PartCleanNumber"]:  # Found given item again
                # Add foreign stock

                if "-" in foundItem["DeliveryDays"]:
                    stockTerm = int(foundItem["DeliveryDays"].split("-")[1])
                else:
                    stockTerm = int(foundItem["DeliveryDays"])

                responseItem["foreign"].append({
                    "name": str(foundItem["StoreID"]),
                    "quantity": foundItem["Quantity"],
                    "term": stockTerm + 2,
                    "price": foundItem["Price"] + " EUR"
                })

            elif [foundItem["PartCleanNumber"], foundItem["Manufacturer"]] in usedAnalogsList:  # Analog found again
                # Searching analog

                for analog in responseItem["analogs"]:
                    if [
                        foundItem["PartCleanNumber"],
                        foundItem["Manufacturer"]
                    ] == [
                        analog["article"],
                        analog["brand"]
                    ]:
                        # Add foreign stock to analog

                        if "-" in foundItem["DeliveryDays"]:
                            stockTerm = int(foundItem["DeliveryDays"].split("-")[1])
                        else:
                            stockTerm = int(foundItem["DeliveryDays"])
                        analog["foreign"].append({
                            "name": str(foundItem["StoreID"]),
                            "quantity": foundItem["Quantity"],
                            "term": stockTerm + 2,
                            "price": foundItem["Price"] + " EUR"
                        })

            else:  # New analog found
                # Add to found list

                usedAnalogsList.append([
                    foundItem["PartCleanNumber"],
                    foundItem["Manufacturer"]
                ])

                # Basic analog info

                analogItem = ResponseInfo.Analog(
                    article=foundItem["PartCleanNumber"],
                    brand=foundItem["Manufacturer"],
                    price=foundItem["Price"] + " EUR",
                    name=foundItem["PartName"],
                    description=foundItem["PartDescription"]
                )

                # Analog stocks

                try:
                    stockTerm = int(foundItem["DeliveryDays"])
                except ValueError:
                    stockTerm = int(foundItem["DeliveryDays"].split("-")[1])

                analogItem["stocks"].append({
                    "name": str(foundItem["StoreID"]),
                    "quantity": foundItem["Quantity"],
                    "term": stockTerm + 2
                })

                responseItem.setAnalog(analogItem)

        return responseItem

    def currency(self) -> ResponseCurrency.List:
        """
        Method of getting currency

        Returns:
            ResponseCurrency.List: Getting currency response
        """

        # Connection verification

        if not self.connected:
            return ResponseCurrency.List(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        if not self.loggedIn:
            return ResponseCurrency.List(
                status=ResponseStatus(
                    ResponseStatus.NOT_AUTHORIZED
                )
            )

        # Get page

        mainPageRequest = self.get(self.Link.main)

        # Get currencies

        pageTree = html.fromstring(mainPageRequest.content)
        currencies = pageTree.xpath('//li/a[@class="tip"]/text()')

        # Response item

        response = ResponseCurrency.List(
            status=ResponseStatus(
                ResponseStatus.SUCCESS
            )
        )

        # Iterating currencies

        for currency in currencies:
            currencyName, currencyValue = currency.split(" = ")

            # If currency required, then add to response

            if currencyName in self.currencies:
                response.append(
                    ResponseCurrency.Currency(
                        name=currencyName,
                        price=float(currencyValue.replace(" грн.", ""))
                    )
                )

        return response

    def signIn(self) -> Tuple[bool, bool]:
        """
        Authorize client

        Returns:
            Tuple[bool, bool]: Is connected, is authorized
        """

        try:
            loginRequest = self.post(
                self.Link.login,
                timeout=self.timeout,
                data={
                    "username": self.username,
                    "password": self.password
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            assert loginRequest.status_code == 200
        except (requests.Timeout, requests.RequestException) as Error:
            return isinstance(Error, AssertionError), False
        else:
            return True, True
