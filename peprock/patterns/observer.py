"""Subject notifies observers of state changes.

See https://en.wikipedia.org/wiki/Observer_pattern

Examples
--------
>>> class MyObserver(Observer):
...     def notify(self, __subject, message):
...         print(f"My observer notified by {type(subject).__name__}: {message}")
...
>>> observer = MyObserver()
>>> subject = Subject()
>>> subject.register_observer(observer)
>>> subject.notify_observers("Hello, world!")
My observer notified by Subject: Hello, world!


"""

from __future__ import annotations

import abc
import functools
import typing
import weakref

_P = typing.ParamSpec("_P")


class Subject(typing.Generic[_P]):
    """Notify subjects of state changes and manage observer registration."""

    @functools.cached_property
    def _observers(self: Subject[_P]) -> weakref.WeakSet[Observer[_P]]:
        return weakref.WeakSet()

    def register_observer(self: Subject[_P], __observer: Observer[_P], /) -> None:
        """Register observer."""
        self._observers.add(__observer)

    def unregister_observer(self: Subject[_P], __observer: Observer[_P], /) -> None:
        """Unregister observer."""
        self._observers.discard(__observer)

    def is_registered_observer(self: Subject[_P], __observer: Observer[_P], /) -> bool:
        """Check if observer is registered and return as bool."""
        return __observer in self._observers

    def notify_observers(
        self: Subject[_P],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        """Notify registered observers by calling their notify() method."""
        for observer in self._observers:
            # noinspection PyTypeChecker
            observer.notify(self, *args, **kwargs)


class Observer(typing.Generic[_P], abc.ABC):
    """Receive notifications from subjects after registration."""

    @abc.abstractmethod
    def notify(
        self: Observer[_P],
        __subject: Subject[_P],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        """Notify of state change of subject."""
        ...


__all__ = [
    "Observer",
    "Subject",
]
