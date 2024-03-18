import argparse
from importlib import import_module
import json
import operator
import sys

from ..utils import get_object_registers


def serialize(obj, *, keep_reserved_fields=True):
    """
    Serialize an object containing Register definitions as a dictionary
    """
    if isinstance(obj, str):
        obj = import_module(f"regdesc.devices.{obj}")

    registers = []
    for reg_name, reg in get_object_registers(obj).items():
        fields = [
            dict(
                name=field_name,
                **{k: getattr(field, k) for k in field.__dataclass_fields__.keys()},
            )
            for field_name, field in reg.__register_fields__.items()
            if keep_reserved_fields or not field_name.startswith("_")
        ]

        registers.append(
            dict(
                name=reg_name,
                description=reg.__doc__.strip() if reg.__doc__ else None,
                address=reg.__address__,
                width=reg.__width__,
                reset=reg.__reset__,
                fields=fields,
            )
        )

    return dict(
        device=obj.__name__.split(".")[-1],
        description=obj.__doc__.strip() if obj.__doc__ else None,
        registers=list(sorted(registers, key=operator.itemgetter("address"))),
    )


def emit_json(device, output_file):
    try:
        ir = serialize(device)
    except ImportError:
        raise ValueError(f"Device not found: regdesc.devices.{device}") from None

    json.dump(ir, output_file, indent=4)


def ep_emit_json():
    parser = argparse.ArgumentParser()
    parser.add_argument("device")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=sys.stdout)
    args = parser.parse_args()

    try:
        emit_json(args.device, args.output)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
