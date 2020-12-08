# coding=utf-8


class ResponseItem(dict):
    def __init__(
            self,
            item_id: int=0,
            article: str="",
            brand: str="",
            name: str="",
            desc: str="",
            price=None,
            image=None,
            stocks=None,
            using=None,
            cross=None,
            foreign=None
    ):
        super().__init__()
        self.id = item_id

        self["article"] = article
        self["brand"] = brand
        self["name"] = name
        self["description"] = desc
        self["price"] = price
        self["image"] = image
        self["stocks"] = stocks if stocks else []
        self["using"] = using if using else dict()
        self["cross"] = cross if cross else dict()
        self["foreign"] = foreign if foreign else list()
        self["analog"] = list()

    def set_analog(self, analog):
        self["analog"].append(dict())
        for key in ["article",
                    "brand",
                    "name",
                    "description",
                    "price",
                    "stocks",
                    "image",
                    "foreign"]:
            self["analog"][-1][key] = analog[key]

    def __bool__(self):
        return bool(self["article"])
