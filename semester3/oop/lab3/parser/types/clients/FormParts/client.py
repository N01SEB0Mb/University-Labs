# coding=utf-8

from parser.types.clients.baseclient import *
from parser.config import loadJSON, Path


class FormParts(BaseClient):
    """
    FormParts parser client, inherits BaseClient

    Attributes:
        SITE_CONFIG (dict): Client configuration
        name (str): Name of client. Used for response
        username (str): Site account username
        password (str): Site account password
        companyId (str): Site account company id
    """

    SITE_CONFIG = loadJSON(
        "config",
        dirpath=Path(__file__).resolve().parent
    )

    name: str = SITE_CONFIG["name"]
    username: str = SITE_CONFIG["username"]
    password: str = SITE_CONFIG["password"]
    companyId: str = SITE_CONFIG["companyId"]

    class Link:
        """
        Class Link used to store site URL's used for parsing

        Attributes:
            main (str): Main page URL
            login (str): Login page URL
            search (str): Searching URL
            category (str): Category URL
            quantity (str): Quantity URL
            analog (str): URL for getting analogs
            cross (str): Cross-codes URL
            use (str): Using in models URL
            image (str): Image URL

        Notes:
            Links must be formatted or concatenated using item id or other values
        """

        main = "https://b2b.ad.ua/"
        login = "https://b2b.ad.ua/Account/Login"
        search = "https://b2b.ad.ua/api/catalog/search?grp=&item="
        category = "https://b2b.ad.ua/api/catalog/searchgrp?item="
        quantity = "https://b2b.ad.ua/api/catalog/stockitems"
        analog = "https://b2b.ad.ua/api/catalog/replace?code="
        cross = "https://b2b.ad.ua/api/catalog/oemitems?code="
        use = "https://b2b.ad.ua/api/catalog/carapplication?code="
        image = "https://b2b.ad.ua/img/"

    def info(
            self,
            article,
            brand
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

        # Searching for article

        article = self.clear(
            str(article),
            delchars=" ./-"
        )

        getSearchResults = self.get(
            self.Link.search + article,
            timeout=self.timeout
        )

        if getSearchResults.status_code != 200:
            self._connected = False

            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_CONNECTION
                )
            )

        # Processing results

        resultDict = getSearchResults.json()

        if not resultDict or not resultDict["items"]:
            return ResponseInfo.Item(
                status=ResponseStatus(
                    ResponseStatus.NO_ARTICLE
                )
            )

        for item in resultDict["items"]:
            if self.compareBrands(
                    item["Бренд"],
                    brand
            ):
                responseItem = ResponseInfo.Item(
                    itemId=item["Item"],
                    article=item["Item"],
                    brand=item["Бренд"],
                    name=item["Название"],
                    description=item["Описание"],
                    price="%.2f UAH" % item["Price"],
                    status=ResponseStatus(
                        ResponseStatus.SUCCESS
                    )
                )
                break
        else:
            # If item was not found, then searching by analogs

            responseItem = self.__searchByAnalogs(
                resultDict,
                article,
                brand,
                ResponseInfo.Item()
            )

            if responseItem is None:
                return ResponseInfo.Item(
                    status=ResponseStatus(
                        ResponseStatus.NO_BRAND
                    )
                )
            else:
                return responseItem

        # Getting cross codes

        try:
            crossRequest = self.get(
                self.Link.cross + responseItem["article"].replace(" ", "+"),
                timeout=self.timeout
            )
            assert crossRequest.status_code == 200

            for cross in crossRequest.json():
                crossCode = cross["Code1"]
                crossBrand = cross["Brand1"]

                if crossBrand in responseItem["cross"]:
                    responseItem["cross"][crossBrand].append(crossCode)
                else:
                    responseItem["cross"][crossBrand] = [crossCode]
        except (AssertionError, KeyError):
            pass

            # Getting using models

            try:
                useRequest = self.get(
                    self.Link.use + responseItem["article"].replace(" ", "+"),
                    timeout=self.timeout
                )
                assert useRequest.status_code == 200

                for using in useRequest.json():
                    usingModel = using["MODEL"]
                    usingBrand = using["MARK"]

                    if usingBrand in responseItem["cross"]:
                        responseItem["cross"][usingBrand].append(usingModel)
                    else:
                        responseItem["cross"][usingBrand] = [usingModel]
            except (AssertionError, KeyError):
                pass

                # Getting images

                try:
                    for image in resultDict["images"]:
                        if image["Item"] == responseItem.id:
                            responseItem["image"] = self.getImage(
                                self.Link.image.format(image["GraTab"]) + image["GraGrdId"],
                                image["GraGrdId"]
                            )
                except KeyError:
                    pass
                except OSError:
                    responseItem["status"] = ResponseStatus(
                        ResponseStatus.NO_MEMORY
                    )

        # Getting analogs

        try:
            getAnalogInfo = self.get(
                self.Link.analog + str(responseItem.id).replace(" ", "+"),
                timeout=self.timeout
            )
            assert getAnalogInfo.status_code == 200

            foundAnalogsInfo = getAnalogInfo.json()["items"]

            for foundAnalogItem in foundAnalogsInfo:
                analogItem = ResponseInfo.Analog(
                    itemId=foundAnalogItem["Item"],
                    article=foundAnalogItem["Item"],
                    brand=foundAnalogItem["Бренд"],
                    price="%.2f UAH" % foundAnalogItem["Price"],
                    name=foundAnalogItem["Название"],
                    description=foundAnalogItem["Описание"]
                )

                try:
                    for image in foundAnalogsInfo["images"]:
                        if image["Item"] == analogItem.id:
                            analogItem["image"] = self.getImage(
                                self.Link.image.format(image["GraTab"]) + image["GraGrdId"],
                                image["GraGrdId"]
                            )
                except KeyError:
                    pass
                except OSError:
                    responseItem["status"] = ResponseStatus(
                        ResponseStatus.NO_MEMORY
                    )

                responseItem.setAnalog(analogItem)
        except (AssertionError, KeyError, IndexError):
            pass

            # Getting stocks

            dataBody = """{"items": "''""" + str(responseItem.id) + """''"""

            for analogItem in responseItem["analogs"]:
                dataBody += """,''""" + str(analogItem.id) + "''"

            quantityRequest = self.post(
                self.Link.quantity,
                data=(dataBody + """"}""").encode("utf-8").decode("utf-8"),
                headers={
                    "Content-Type": "text/html; charset=UTF-8"
                },
                timeout=self.timeout
            )

            # Setting stocks

            if quantityRequest.status_code == 200:
                for stock in quantityRequest.json():
                    if stock["ItemNo"] == responseItem.id:
                        responseItem["stocks"].append({
                            "name": stock["LocationCode"],
                            "quantity": stock["Qty"],
                            "term": None
                        })
                    else:
                        for analogItem in responseItem["analogs"]:
                            if analogItem["article"] == stock["ItemNo"]:
                                analogItem["stocks"].append({
                                    "name": stock["LocationCode"],
                                    "quantity": stock["Qty"],
                                    "term": None
                                })

        return responseItem

    def __searchByAnalogs(
            self,
            resultDict: dict,
            article: str,
            brand: str,
            foundItem: ResponseInfo.Item,
            analogsId: Optional[Set[str]] = None
    ) -> ResponseInfo.Item:
        """
        Method of getting items and analogs found by specified article and brand

        Args:
            resultDict (dict): Searching results
            article (str): Article of item you searched
            brand (str): Brand of item you searched
            foundItem (ResponseInfo.Item): Found item
            analogsId (Optional[set]): Id of found analogs

        Returns:
            ResponseInfo.Item: Getting info response
        """

        usedAnalogs = analogsId or set()

        # Searching for found items

        for item in resultDict["items"]:
            skip = False

            for foundBy in resultDict["by"]:
                if foundBy["item"] == item["Item"]:
                    equalArticles = self.compareArticles(
                        foundBy["search"],
                        article
                    )
                    equalBrands = self.compareBrands(
                        foundBy["brand"],
                        brand
                    )

                    if not (equalArticles and equalBrands):
                        skip = True

                    break

            if skip:
                continue

            # Analogs

            if item["Item"] not in usedAnalogs:
                foundItem.setAnalog(
                    ResponseInfo.Analog(
                        itemId=item["Item"],
                        article=item["Item"],
                        brand=item["Бренд"],
                        name=item["Название"],
                        description=item["Описание"],
                        price="%.2f UAH" % item["Price"]
                    )
                )

            analogsRequest = self.get(
                self.Link.analog + str(item["Item"]).replace(" ", "+")
            )

            for analogItem in analogsRequest.json()["items"]:
                if analogItem["Item"] not in usedAnalogs:
                    foundItem.setAnalog(
                        ResponseInfo.Analog(
                            itemId=analogItem["Item"],
                            article=analogItem["Item"],
                            name=analogItem["Название"],
                            desc=analogItem["Описание"],
                            brand=analogItem["Бренд"],
                            price="%.2f UAH" % analogItem["Price"]
                        )
                    )

                    usedAnalogs.add(analogItem["Item"])

                    # Getting analogs image

                    try:
                        for image in analogItem["images"]:
                            if image["Item"] == foundItem["analogs"][-1].id:
                                foundItem["analogs"][-1]["image"] = self.getImage(
                                    self.Link.image.format(image["GraTab"]) + image["GraGrdId"],
                                    image["GraGrdId"]
                                )
                    except KeyError:
                        pass
                    except OSError:
                        foundItem["status"] = ResponseStatus(
                            ResponseStatus.NO_MEMORY
                        )

        # Item info

        if foundItem:
            # Item cross-codes

            try:
                crossRequest = self.get(
                    self.Link.cross + foundItem["article"].replace(" ", "+"),
                    timeout=self.timeout
                )
                assert crossRequest.status_code == 200

                for cross in crossRequest.json():
                    crossCode = cross["Code1"]
                    crossBrand = cross["Brand1"]

                    if crossBrand in foundItem["cross"]:
                        foundItem["cross"][crossBrand].append(crossCode)
                    else:
                        foundItem["cross"][crossBrand] = [crossCode]
            except (AssertionError, KeyError):
                pass

            # Item using models

            try:
                useRequest = self.get(
                    self.Link.use + foundItem["article"].replace(" ", "+"),
                    timeout=self.timeout
                )
                assert useRequest.status_code == 200

                for using in useRequest.json():
                    usingModel = using["MODEL"]
                    usingBrand = using["MARK"]

                    if usingBrand in foundItem["using"]:
                        foundItem["using"][usingBrand].append(usingModel)
                    else:
                        foundItem["using"][usingBrand] = [usingModel]
            except (AssertionError, KeyError):
                pass

            # Item image

            try:
                for image in resultDict["images"]:
                    if image["Item"] == foundItem.id:
                        foundItem["image"] = self.getImage(
                            self.Link.image.format(image["GraTab"]) + image["GraGrdId"],
                            image["GraGrdId"]
                        )
            except KeyError:
                pass
            except OSError:
                foundItem["status"] = ResponseStatus(
                    ResponseStatus.NO_MEMORY
                )

            # Item and analogs stocks

            dataBody = """{"items": "''""" + str(foundItem.id) + """''"""

            for analogItem in foundItem["analogs"]:
                dataBody += """,''""" + str(analogItem.id) + "''"

            quantityRequest = self.post(
                self.Link.quantity,
                data=(dataBody + """"}""").encode("utf-8"),
                headers={
                    "Content-Type": "text/html; charset=UTF-8"
                },
                timeout=self.timeout
            )

            # Setting stocks

            if quantityRequest.status_code == 200:
                for stock in quantityRequest.json():
                    if stock["ItemNo"] == foundItem.id:
                        foundItem["stocks"].append({
                            "name": stock["LocationCode"],
                            "quantity": stock["Qty"],
                            "term": None
                        })
                    else:
                        for analogItem in foundItem["analogs"]:
                            if analogItem["article"] == stock["ItemNo"]:
                                analogItem["stocks"].append({
                                    "name": stock["LocationCode"],
                                    "quantity": stock["Qty"],
                                    "term": None
                                })
        else:
            # Getting stocks

            try:
                dataBody = """{"items": "''""" + str(foundItem["analogs"][0].id) + """''"""
            except IndexError:
                return foundItem

            for analogItem in foundItem["analogs"][1:]:
                dataBody += """,''""" + str(analogItem.id) + "''"

            quantityRequest = self.post(
                self.Link.quantity,
                data=(dataBody + """"}""").encode("utf-8"),
                headers={
                    "Content-Type": "text/html; charset=UTF-8"
                },
                timeout=self.timeout
            )

            # Setting stocks

            if quantityRequest.status_code == 200:
                for stock in quantityRequest.json():
                    for analogItem in foundItem["analogs"]:
                        if analogItem["article"] == stock["ItemNo"]:
                            analogItem["stocks"].append({
                                "name": stock["LocationCode"],
                                "quantity": stock["Qty"],
                                "term": None
                            })

        # Returning result

        for analogItem in foundItem["analogs"]:
            foundItem.setAnalog(analogItem)

        return foundItem

    def signIn(self) -> Tuple[bool, bool]:
        """
        Authorize client

        Returns:
            Tuple[bool, bool]: Is connected, is authorized
        """

        try:
            loginPageRequest = self.get(
                self.Link.login,
                timeout=self.timeout
            )
            assert loginPageRequest.status_code == 200
        except (requests.Timeout, requests.RequestException, AssertionError):
            return False, False

        pageTree = html.fromstring(
            loginPageRequest.text.encode("utf-8")
        )

        tokenList = pageTree.xpath(
            "//input[@name='__RequestVerificationToken']/@value"
        )

        if not tokenList:
            return False, False

        token = tokenList[0]
        dataBody = f"__RequestVerificationToken={token}&"\
                   f"ComId={self.companyId}&"\
                   f"UserName={self.username}&"\
                   f"Password={self.password}&"\
                   f"RememberMe=true"

        try:
            signInRequest = self.post(
                self.Link.login,
                timeout=self.timeout,
                data=dataBody,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
        except (requests.Timeout, requests.RequestException):
            return False, False

        checkAuthorizationTree = html.fromstring(
            signInRequest.text.encode("utf-8")
        )

        problems = checkAuthorizationTree.xpath(
            '//div[@class="validation-summary-errors text-danger"]'
        )

        if signInRequest.status_code == 200 and not problems:
            return True, True
        else:
            return True, False
