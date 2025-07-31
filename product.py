import enum

class Brand(enum.Enum):
    GVFC = "Graf von Faber-Castell"
    VISCONTI = "Visconti"
    MONTBLANC = "MontBlanc"
    ESTERBROOK = "Esterbrook"

    @property
    def af_repr(self):
        return {
            Brand.GVFC: "graf-von-faber-castell",
            Brand.VISCONTI: "visconti",
            Brand.MONTBLANC: "montblanc-kalem",
            Brand.ESTERBROOK: "esterbrook"
        }.get(self)

class Category(enum.Enum):
    FOUNTAIN_PEN = "Fountain Pen"
    ROLLERBALL_PEN = "Rollerball Pen"
    BALLPOINT_PEN = "Ballpoint Pen"
    OTHER = "Other"

class Product:
    def __init__(self, name:str, price:int, link:str, category:Category, brand:Brand):
        self.name = name
        self.price = price
        self.link = link
        self.category = category
        self.brand = brand

    @classmethod
    def from_csv_line(cls, line:str):
        """
        order should be: name, price, link, category, brand
        """
        _split = line.replace("\n", "").split(',')
        assert len(_split) == 5, f"Length of csv line is not 5. \nProvided line: {line}"
        name, price, link, category, brand = _split

        try: c = Category(category)
        except ValueError: raise ValueError(f"{category} is not a valid category. \nfaulty line: {line}")

        try: b = Brand(brand)
        except ValueError: raise ValueError(f"{brand} is not a valid brand. \nfaulty line: {line}")

        assert link.startswith("https://"), f"Link must start with https://. \nfaulty line: {line}"

        try: price = int(price)
        except ValueError: raise ValueError(f"{price} is not a valid price. \nfaulty line: {line}")

        return cls(name, int(price), link, c, b)

    def __dict__(self):
        return {
            "name": self.name,
            "price": self.price,
            "link": self.link,
            "category": self.category.value,
            "brand": self.brand.value
        }
    def __str__(self):
        return str(self.__dict__())