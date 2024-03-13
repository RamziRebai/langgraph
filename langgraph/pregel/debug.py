from pprint import pformat
from textwrap import indent
from typing import Any, Iterator, Mapping

from langchain_core.runnables import Runnable
from langchain_core.utils.input import get_bolded_text, get_colored_text

from langgraph.channels.base import BaseChannel, EmptyChannelError
from langgraph.pregel.reserved import AllReservedChannels


def print_step_start(step: int, next_tasks: list[tuple[Runnable, Any, str]]) -> None:
    n_tasks = len(next_tasks)
    print(
        f"{get_colored_text('[langgraph/step]', color='blue')} "
        + get_bolded_text(
            f"Starting step {step} with {n_tasks} task{'s' if n_tasks > 1 else ''}. Next tasks:\n"
        )
        + "\n".join(
            f"- {get_colored_text(name, color='green')}:\n{indent(pformat(val), prefix='    ')}"
            for _, val, name in next_tasks
        )
    )


def print_checkpoint(step: int, channels: Mapping[str, BaseChannel]) -> None:
    print(
        f"{get_colored_text('[langgraph/checkpoint]', color='blue')} "
        + get_bolded_text(f"Finishing step {step}. Channel values:\n")
        + "\n".join(
            f"- {get_colored_text(name, color='green')}:\n{indent(pformat(val), prefix='    ')}"
            for name, val in _read_channels(channels)
        )
    )


def _read_channels(channels: Mapping[str, BaseChannel]) -> Iterator[tuple[str, Any]]:
    for name, channel in channels.items():
        if name in AllReservedChannels:
            continue
        try:
            yield (name, channel.get())
        except EmptyChannelError:
            pass
