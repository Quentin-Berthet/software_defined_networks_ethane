from typing import List, Any, TypeVar, Callable, Type, cast

T = TypeVar("T")


# JSON to Object : https://app.quicktype.io

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class VLAN:
    interfaces: List[str]
    name: str
    status: str
    vlan_id: int

    def __init__(self, interfaces, name, status, vlan_id):
        self.interfaces = interfaces
        self.name = name
        self.status = status
        self.vlan_id = vlan_id

    @staticmethod
    def from_dict(obj: Any) -> 'VLAN':
        assert isinstance(obj, dict)
        interfaces = from_list(from_str, obj.get("interfaces"))
        name = from_str(obj.get("name"))
        status = from_str(obj.get("status"))
        vlan_id = int(from_str(obj.get("vlan_id")))
        return VLAN(interfaces, name, status, vlan_id)

    def to_dict(self) -> dict:
        result: dict = {"interfaces": from_list(from_str, self.interfaces), "name": from_str(self.name),
                        "status": from_str(self.status), "vlan_id": from_str(str(self.vlan_id))}
        return result


class Switch:
    name: str
    vlans: List[VLAN]
    trunk_interfaces: List[str]

    def __init__(self, name, vlans, trunk_interfaces):
        self.name = name
        self.vlans = vlans
        self.trunk_interfaces = trunk_interfaces

    @staticmethod
    def from_dict(obj: Any) -> 'Switch':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        vlans = from_list(VLAN.from_dict, obj.get("vlans"))
        trunk_interfaces = obj.get("trunk_interfaces")
        return Switch(name, vlans, trunk_interfaces)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "vlans": from_list(lambda x: to_class(VLAN, x), self.vlans),
                        "trunk_interfaces": from_list(from_str, self.trunk_interfaces)}
        return result


class Switches:
    switches: List[Switch]

    def __init__(self, switches):
        self.switches = switches

    def add_switch(self, name: str, vlans: [dict], trunk_interfaces: List[str]):
        self.switches.append(Switch.from_dict({
            "name": name,
            "vlans": vlans,
            "trunk_interfaces": trunk_interfaces
        }))

    @staticmethod
    def from_dict(obj: Any) -> 'Switches':
        assert isinstance(obj, dict)
        switches = from_list(Switch.from_dict, obj.get("switches"))
        return Switches(switches)

    def to_dict(self) -> dict:
        result: dict = {"switches": from_list(lambda x: to_class(Switch, x), self.switches)}
        return result


def switches_from_dict(s: Any) -> Switches:
    return Switches.from_dict(s)


def switches_to_dict(x: Switches) -> Any:
    return to_class(Switches, x)
