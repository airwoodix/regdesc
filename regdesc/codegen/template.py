import argparse
import jinja2
import json
from pathlib import Path
import shlex
import subprocess
import sys

from . import ir


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
    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("."), **jinja_env_args)
        tpl = env.get_template(spec)
    except jinja2.TemplateNotFound:
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("regdesc.codegen", "templates"),
            **jinja_env_args,
        )
        tpl = env.get_template(spec)

    return tpl


def ep_codegen():
    args = get_arguments()

    try:
        with Path(args.device).open() as fp:
            device_desc = json.load(fp)
    except FileNotFoundError:
        try:
            device_desc = ir.serialize(args.device, keep_reserved_fields=False)
        except ImportError:
            sys.exit(f"Device not found: '{args.device}'")
    except json.JSONDecodeError as e:
        sys.exit(f"Failed reading {args.device}: {e}")

    try:
        tpl = get_template(args.template)
    except jinja2.TemplateNotFound:
        sys.exit(f"Template not found: {args.template}")

    rendered_template = tpl.render(device_desc)

    if args.no_auto_format:
        print(rendered_template, file=args.output)
    else:
        subprocess.run(
            shlex.split("black - -q"),
            input=rendered_template.encode(),
            stdout=args.output,
        )
