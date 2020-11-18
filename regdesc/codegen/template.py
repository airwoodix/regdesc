import argparse
import jinja2
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

from . import ir
from ..utils import camel_to_snake


AUTO_FORMATTERS = {
    r"\.py$": "black - -q",
    r"\.(h|hxx|hpp|c|cc|cpp|cxx|)$": "clang-format",
    r"\.rs$": "rustfmt",
    r"\.svd": "tidy -xml -iq",
}


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("device")
    parser.add_argument("-t", "--template", required=True)
    parser.add_argument("-n", "--no-auto-format", action="store_true")
    parser.add_argument(
        "-o", "--output", type=argparse.FileType("w"), default=sys.stdout
    )

    return parser.parse_args()


def get_template(spec, **jinja_env_args):
    # custom filters need to be registered before any template is loaded
    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("."), **jinja_env_args)
        env.filters["camel_to_snake"] = camel_to_snake
        tpl = env.get_template(spec)
    except jinja2.TemplateNotFound:
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("regdesc.codegen", "templates"),
            **jinja_env_args,
        )
        env.filters["camel_to_snake"] = camel_to_snake
        tpl = env.get_template(spec)

    return tpl


def get_formatter_cmd_for_template(tpl):
    for rx, cmd in AUTO_FORMATTERS.items():
        if re.search(rx, tpl.filename) is not None:
            return shlex.split(cmd)
    else:
        raise NotImplementedError


def get_device_desc(device):
    try:
        with Path(device).open() as fp:
            return json.load(fp)
    except FileNotFoundError:
        try:
            return ir.serialize(device, keep_reserved_fields=False)
        except ImportError:
            raise ValueError(f"Device not found: '{device}'") from None
    except json.JSONDecodeError as e:
        raise IOError(f"Failed reading {device}: {e}")


def ep_codegen():
    args = get_arguments()

    try:
        device_desc = get_device_desc(args.device)
    except (ValueError, IOError) as e:
        sys.exit(str(e))

    try:
        tpl = get_template(args.template)
    except jinja2.TemplateNotFound:
        sys.exit(f"Template not found: {args.template}")

    rendered_template = tpl.render(device_desc)

    if args.no_auto_format:
        print(rendered_template, file=args.output)
    else:
        subprocess.run(
            get_formatter_cmd_for_template(tpl),
            input=rendered_template.encode(),
            stdout=args.output,
        )
