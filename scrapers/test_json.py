import urllib.request
import json
import requests
from typing import Any, List, Dict, TypeVar, Callable, Type, cast
from enum import Enum
from uuid import UUID
from datetime import datetime
import dateutil.parser

url = "https://api.scryfall.com/cards/named?fuzzy=aust+com"

try:
    jason_obj = urllib.request.urlopen(url)
    data = json.load(jason_obj)
    print(data)
except:
    print('couldnt print data')
try:
    None
except:
    print('could not convert')

# Generated by https://quicktype.io




T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class ImageUris:
    small: str
    normal: str
    large: str
    png: str
    art_crop: str
    border_crop: str

    def __init__(self, small: str, normal: str, large: str, png: str, art_crop: str, border_crop: str) -> None:
        self.small = small
        self.normal = normal
        self.large = large
        self.png = png
        self.art_crop = art_crop
        self.border_crop = border_crop

    @staticmethod
    def from_dict(obj: Any) -> 'ImageUris':
        assert isinstance(obj, dict)
        small = from_str(obj.get("small"))
        normal = from_str(obj.get("normal"))
        large = from_str(obj.get("large"))
        png = from_str(obj.get("png"))
        art_crop = from_str(obj.get("art_crop"))
        border_crop = from_str(obj.get("border_crop"))
        return ImageUris(small, normal, large, png, art_crop, border_crop)

    def to_dict(self) -> dict:
        result: dict = {}
        result["small"] = from_str(self.small)
        result["normal"] = from_str(self.normal)
        result["large"] = from_str(self.large)
        result["png"] = from_str(self.png)
        result["art_crop"] = from_str(self.art_crop)
        result["border_crop"] = from_str(self.border_crop)
        return result


class Legality(Enum):
    LEGAL = "legal"
    NOT_LEGAL = "not_legal"


class PurchaseUris:
    tcgplayer: str
    cardmarket: str
    cardhoarder: str

    def __init__(self, tcgplayer: str, cardmarket: str, cardhoarder: str) -> None:
        self.tcgplayer = tcgplayer
        self.cardmarket = cardmarket
        self.cardhoarder = cardhoarder

    @staticmethod
    def from_dict(obj: Any) -> 'PurchaseUris':
        assert isinstance(obj, dict)
        tcgplayer = from_str(obj.get("tcgplayer"))
        cardmarket = from_str(obj.get("cardmarket"))
        cardhoarder = from_str(obj.get("cardhoarder"))
        return PurchaseUris(tcgplayer, cardmarket, cardhoarder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tcgplayer"] = from_str(self.tcgplayer)
        result["cardmarket"] = from_str(self.cardmarket)
        result["cardhoarder"] = from_str(self.cardhoarder)
        return result


class RelatedUris:
    gatherer: str
    tcgplayer_decks: str
    edhrec: str
    mtgtop8: str

    def __init__(self, gatherer: str, tcgplayer_decks: str, edhrec: str, mtgtop8: str) -> None:
        self.gatherer = gatherer
        self.tcgplayer_decks = tcgplayer_decks
        self.edhrec = edhrec
        self.mtgtop8 = mtgtop8

    @staticmethod
    def from_dict(obj: Any) -> 'RelatedUris':
        assert isinstance(obj, dict)
        gatherer = from_str(obj.get("gatherer"))
        tcgplayer_decks = from_str(obj.get("tcgplayer_decks"))
        edhrec = from_str(obj.get("edhrec"))
        mtgtop8 = from_str(obj.get("mtgtop8"))
        return RelatedUris(gatherer, tcgplayer_decks, edhrec, mtgtop8)

    def to_dict(self) -> dict:
        result: dict = {}
        result["gatherer"] = from_str(self.gatherer)
        result["tcgplayer_decks"] = from_str(self.tcgplayer_decks)
        result["edhrec"] = from_str(self.edhrec)
        result["mtgtop8"] = from_str(self.mtgtop8)
        return result


class Card:
    object: str
    id: UUID
    oracle_id: UUID
    multiverse_ids: List[int]
    mtgo_id: int
    mtgo_foil_id: int
    tcgplayer_id: int
    name: str
    lang: str
    released_at: datetime
    uri: str
    scryfall_uri: str
    layout: str
    highres_image: bool
    image_uris: ImageUris
    mana_cost: str
    cmc: int
    type_line: str
    oracle_text: str
    colors: List[str]
    color_identity: List[str]
    legalities: Dict[str, Legality]
    games: List[str]
    reserved: bool
    foil: bool
    nonfoil: bool
    oversized: bool
    promo: bool
    reprint: bool
    variation: bool
    set: str
    set_name: str
    set_type: str
    set_uri: str
    set_search_uri: str
    scryfall_set_uri: str
    rulings_uri: str
    prints_search_uri: str
    collector_number: int
    digital: bool
    rarity: str
    card_back_id: UUID
    artist: str
    artist_ids: List[UUID]
    illustration_id: UUID
    border_color: str
    frame: int
    full_art: bool
    textless: bool
    booster: bool
    story_spotlight: bool
    edhrec_rank: int
    prices: Dict[str, str]
    related_uris: RelatedUris
    purchase_uris: PurchaseUris

    def __init__(self, object: str, id: UUID, oracle_id: UUID, multiverse_ids: List[int], mtgo_id: int, mtgo_foil_id: int, tcgplayer_id: int, name: str, lang: str, released_at: datetime, uri: str, scryfall_uri: str, layout: str, highres_image: bool, image_uris: ImageUris, mana_cost: str, cmc: int, type_line: str, oracle_text: str, colors: List[str], color_identity: List[str], legalities: Dict[str, Legality], games: List[str], reserved: bool, foil: bool, nonfoil: bool, oversized: bool, promo: bool, reprint: bool, variation: bool, set: str, set_name: str, set_type: str, set_uri: str, set_search_uri: str, scryfall_set_uri: str, rulings_uri: str, prints_search_uri: str, collector_number: int, digital: bool, rarity: str, card_back_id: UUID, artist: str, artist_ids: List[UUID], illustration_id: UUID, border_color: str, frame: int, full_art: bool, textless: bool, booster: bool, story_spotlight: bool, edhrec_rank: int, prices: Dict[str, str], related_uris: RelatedUris, purchase_uris: PurchaseUris) -> None:
        self.object = object
        self.id = id
        self.oracle_id = oracle_id
        self.multiverse_ids = multiverse_ids
        self.mtgo_id = mtgo_id
        self.mtgo_foil_id = mtgo_foil_id
        self.tcgplayer_id = tcgplayer_id
        self.name = name
        self.lang = lang
        self.released_at = released_at
        self.uri = uri
        self.scryfall_uri = scryfall_uri
        self.layout = layout
        self.highres_image = highres_image
        self.image_uris = image_uris
        self.mana_cost = mana_cost
        self.cmc = cmc
        self.type_line = type_line
        self.oracle_text = oracle_text
        self.colors = colors
        self.color_identity = color_identity
        self.legalities = legalities
        self.games = games
        self.reserved = reserved
        self.foil = foil
        self.nonfoil = nonfoil
        self.oversized = oversized
        self.promo = promo
        self.reprint = reprint
        self.variation = variation
        self.set = set
        self.set_name = set_name
        self.set_type = set_type
        self.set_uri = set_uri
        self.set_search_uri = set_search_uri
        self.scryfall_set_uri = scryfall_set_uri
        self.rulings_uri = rulings_uri
        self.prints_search_uri = prints_search_uri
        self.collector_number = collector_number
        self.digital = digital
        self.rarity = rarity
        self.card_back_id = card_back_id
        self.artist = artist
        self.artist_ids = artist_ids
        self.illustration_id = illustration_id
        self.border_color = border_color
        self.frame = frame
        self.full_art = full_art
        self.textless = textless
        self.booster = booster
        self.story_spotlight = story_spotlight
        self.edhrec_rank = edhrec_rank
        self.prices = prices
        self.related_uris = related_uris
        self.purchase_uris = purchase_uris

    @staticmethod
    def from_dict(obj: Any) -> 'Card':
        assert isinstance(obj, dict)
        object = from_str(obj.get("object"))
        id = UUID(obj.get("id"))
        oracle_id = UUID(obj.get("oracle_id"))
        multiverse_ids = from_list(from_int, obj.get("multiverse_ids"))
        mtgo_id = from_int(obj.get("mtgo_id"))
        mtgo_foil_id = from_int(obj.get("mtgo_foil_id"))
        tcgplayer_id = from_int(obj.get("tcgplayer_id"))
        name = from_str(obj.get("name"))
        lang = from_str(obj.get("lang"))
        released_at = from_datetime(obj.get("released_at"))
        uri = from_str(obj.get("uri"))
        scryfall_uri = from_str(obj.get("scryfall_uri"))
        layout = from_str(obj.get("layout"))
        highres_image = from_bool(obj.get("highres_image"))
        image_uris = ImageUris.from_dict(obj.get("image_uris"))
        mana_cost = from_str(obj.get("mana_cost"))
        cmc = from_int(obj.get("cmc"))
        type_line = from_str(obj.get("type_line"))
        oracle_text = from_str(obj.get("oracle_text"))
        colors = from_list(from_str, obj.get("colors"))
        color_identity = from_list(from_str, obj.get("color_identity"))
        legalities = from_dict(Legality, obj.get("legalities"))
        games = from_list(from_str, obj.get("games"))
        reserved = from_bool(obj.get("reserved"))
        foil = from_bool(obj.get("foil"))
        nonfoil = from_bool(obj.get("nonfoil"))
        oversized = from_bool(obj.get("oversized"))
        promo = from_bool(obj.get("promo"))
        reprint = from_bool(obj.get("reprint"))
        variation = from_bool(obj.get("variation"))
        set = from_str(obj.get("set"))
        set_name = from_str(obj.get("set_name"))
        set_type = from_str(obj.get("set_type"))
        set_uri = from_str(obj.get("set_uri"))
        set_search_uri = from_str(obj.get("set_search_uri"))
        scryfall_set_uri = from_str(obj.get("scryfall_set_uri"))
        rulings_uri = from_str(obj.get("rulings_uri"))
        prints_search_uri = from_str(obj.get("prints_search_uri"))
        collector_number = int(from_str(obj.get("collector_number")))
        digital = from_bool(obj.get("digital"))
        rarity = from_str(obj.get("rarity"))
        card_back_id = UUID(obj.get("card_back_id"))
        artist = from_str(obj.get("artist"))
        artist_ids = from_list(lambda x: UUID(x), obj.get("artist_ids"))
        illustration_id = UUID(obj.get("illustration_id"))
        border_color = from_str(obj.get("border_color"))
        frame = int(from_str(obj.get("frame")))
        full_art = from_bool(obj.get("full_art"))
        textless = from_bool(obj.get("textless"))
        booster = from_bool(obj.get("booster"))
        story_spotlight = from_bool(obj.get("story_spotlight"))
        edhrec_rank = from_int(obj.get("edhrec_rank"))
        prices = from_dict(from_str, obj.get("prices"))
        related_uris = RelatedUris.from_dict(obj.get("related_uris"))
        purchase_uris = PurchaseUris.from_dict(obj.get("purchase_uris"))
        return Card(object, id, oracle_id, multiverse_ids, mtgo_id, mtgo_foil_id, tcgplayer_id, name, lang, released_at, uri, scryfall_uri, layout, highres_image, image_uris, mana_cost, cmc, type_line, oracle_text, colors, color_identity, legalities, games, reserved, foil, nonfoil, oversized, promo, reprint, variation, set, set_name, set_type, set_uri, set_search_uri, scryfall_set_uri, rulings_uri, prints_search_uri, collector_number, digital, rarity, card_back_id, artist, artist_ids, illustration_id, border_color, frame, full_art, textless, booster, story_spotlight, edhrec_rank, prices, related_uris, purchase_uris)

    def to_dict(self) -> dict:
        result: dict = {}
        result["object"] = from_str(self.object)
        result["id"] = str(self.id)
        result["oracle_id"] = str(self.oracle_id)
        result["multiverse_ids"] = from_list(from_int, self.multiverse_ids)
        result["mtgo_id"] = from_int(self.mtgo_id)
        result["mtgo_foil_id"] = from_int(self.mtgo_foil_id)
        result["tcgplayer_id"] = from_int(self.tcgplayer_id)
        result["name"] = from_str(self.name)
        result["lang"] = from_str(self.lang)
        result["released_at"] = self.released_at.isoformat()
        result["uri"] = from_str(self.uri)
        result["scryfall_uri"] = from_str(self.scryfall_uri)
        result["layout"] = from_str(self.layout)
        result["highres_image"] = from_bool(self.highres_image)
        result["image_uris"] = to_class(ImageUris, self.image_uris)
        result["mana_cost"] = from_str(self.mana_cost)
        result["cmc"] = from_int(self.cmc)
        result["type_line"] = from_str(self.type_line)
        result["oracle_text"] = from_str(self.oracle_text)
        result["colors"] = from_list(from_str, self.colors)
        result["color_identity"] = from_list(from_str, self.color_identity)
        result["legalities"] = from_dict(lambda x: to_enum(Legality, x), self.legalities)
        result["games"] = from_list(from_str, self.games)
        result["reserved"] = from_bool(self.reserved)
        result["foil"] = from_bool(self.foil)
        result["nonfoil"] = from_bool(self.nonfoil)
        result["oversized"] = from_bool(self.oversized)
        result["promo"] = from_bool(self.promo)
        result["reprint"] = from_bool(self.reprint)
        result["variation"] = from_bool(self.variation)
        result["set"] = from_str(self.set)
        result["set_name"] = from_str(self.set_name)
        result["set_type"] = from_str(self.set_type)
        result["set_uri"] = from_str(self.set_uri)
        result["set_search_uri"] = from_str(self.set_search_uri)
        result["scryfall_set_uri"] = from_str(self.scryfall_set_uri)
        result["rulings_uri"] = from_str(self.rulings_uri)
        result["prints_search_uri"] = from_str(self.prints_search_uri)
        result["collector_number"] = from_str(str(self.collector_number))
        result["digital"] = from_bool(self.digital)
        result["rarity"] = from_str(self.rarity)
        result["card_back_id"] = str(self.card_back_id)
        result["artist"] = from_str(self.artist)
        result["artist_ids"] = from_list(lambda x: str(x), self.artist_ids)
        result["illustration_id"] = str(self.illustration_id)
        result["border_color"] = from_str(self.border_color)
        result["frame"] = from_str(str(self.frame))
        result["full_art"] = from_bool(self.full_art)
        result["textless"] = from_bool(self.textless)
        result["booster"] = from_bool(self.booster)
        result["story_spotlight"] = from_bool(self.story_spotlight)
        result["edhrec_rank"] = from_int(self.edhrec_rank)
        result["prices"] = from_dict(from_str, self.prices)
        result["related_uris"] = to_class(RelatedUris, self.related_uris)
        result["purchase_uris"] = to_class(PurchaseUris, self.purchase_uris)
        return result


def card_from_dict(s: Any) -> Card:
    return Card.from_dict(s)


def card_to_dict(x: Card) -> Any:
    return to_class(Card, x)


aust_com = card_from_dict(data)
