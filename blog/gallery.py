"""This file is responsible for rendering the gallery.

Once this matures it might be an interesting exercise to make it a tool built into
arlunio itself.
"""
import argparse
import os
import typing as t

from datetime import datetime

import attr
import jinja2 as j2
import tomlkit as toml

# from importlib import import_module


# from arlunio.imp import NotebookLoader


@attr.s(auto_attribs=True)
class Config:
    """Represents site configuration."""

    baseurl: str
    output: str
    templates: str

    @classmethod
    def fromfile(cls, filepath):

        with open(filepath) as f:
            config = toml.parse(f.read())

        baseurl = config["site"]["baseurl"]
        templates = config["site"]["templates"]
        output = config["site"]["output"]

        return cls(baseurl=baseurl, templates=templates, output=output)


@attr.s(auto_attribs=True)
class Context:
    """Represents values to pass to a context"""

    baseurl: str
    date: str
    images: t.List[str]

    @classmethod
    def new(cls, config, local):
        baseurl = config.baseurl

        if local:
            baseurl = "http://localhost:8000/"

        date = datetime.now().strftime("%d %B %Y -- %H:%M:%S")
        images = ["a" for _ in range(25)]

        return cls(baseurl=baseurl, date=date, images=images)

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class Site:

    config: str
    local: bool

    def build(self, destination):
        env = j2.Environment(loader=j2.FileSystemLoader(self.config.templates))
        template = env.get_template("gallery.html")

        index = os.path.join(self.config.output, "index.html")
        context = Context.new(self.config, self.local)

        with open(index, "w") as f:
            f.write(template.render(context.as_dict()))


cli = argparse.ArgumentParser(description="Gallery builder for the arlunio blog.")
cli.add_argument("-c", "--config", help="path to config file", default="config.toml")
cli.add_argument(
    "-l",
    "--local",
    help="switch to indicate when building locally",
    action="store_true",
)
cli.add_argument(
    "-o", "--output", help="folder to render results to", default="public/"
)

if __name__ == "__main__":
    args = cli.parse_args()
    config = Config.fromfile(args.config)

    site = Site(config, args.local)
    site.build(args.output)
