from typing import Dict
from dataclasses import dataclass


@dataclass
class Payload:
    uuid: str
    name: str
    age: int


items: Dict[str, Payload] = {
    "1": Payload(uuid="1", name="Jane Doe1", age=20),
    "2": Payload(uuid="2", name="Jane Doe2", age=18),
    "3": Payload(uuid="3", name="Jane Doe3", age=18),
    "4": Payload(uuid="4", name="Jane Doe4", age=18),
    "5": Payload(uuid="5", name="Jane Doe5", age=18),
    "6": Payload(uuid="6", name="Jane Doe6", age=18),
    "7": Payload(uuid="7", name="Jane Doe7", age=18),
    "8": Payload(uuid="8", name="Jane Doe8", age=18),
    "9": Payload(uuid="9", name="Jane Doe9", age=18),
    "10": Payload(uuid="10", name="Jane Doe10", age=18),
    "11": Payload(uuid="11", name="Jane Doe11", age=18),
}
