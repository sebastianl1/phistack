from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from .lang import t

VI = {"vi_mode": True}


def choices_from(tools, lang=None):
    return [
        Choice(value=tool["id"], name=f"{tool['name']}  ({tool['id']})")
        for tool in tools
    ]


def select(message, choices, default=None):
    kwargs = {"message": message, "choices": choices, **VI}
    if default is not None:
        kwargs["default"] = default
    return inquirer.select(**kwargs).execute()


def checkbox(message, choices, default=None):
    return inquirer.checkbox(
        message=message,
        choices=choices,
        cycle=False,
        transformer=lambda r: f"{len(r)} {t('count_tools', n=len(r))}",
        default=default or [],
        **VI,
    ).execute()


def confirm(message, default=True):
    return inquirer.confirm(
        message=message,
        default=default,
        **VI,
    ).execute()


def fuzzy_select(message, choices, default=None):
    kwargs = {
        "message": message,
        "choices": choices,
        "max_height": "60%",
        "multiselect": False,
        **VI,
    }
    if default is not None:
        kwargs["default"] = default
    return inquirer.fuzzy(**kwargs).execute()


def text(message, default=None):
    kwargs = {"message": message, **VI}
    if default is not None:
        kwargs["default"] = default
    return inquirer.text(**kwargs).execute()
