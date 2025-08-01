import copy

import pytest

import peprock.patterns


class _StrSubject(peprock.patterns.Subject[str]):
    pass


class _IntFloatSubject(peprock.patterns.Subject[int, float]):
    pass


class _StrObserver(peprock.patterns.Observer[str]):
    def notify(
        self: peprock.patterns.Observer[str],
        __subject: peprock.patterns.Subject[str],
        /,
        str_value: str,
    ):
        print(f"{type(self).__name__} got {str_value=} from {type(__subject).__name__}")


class _IntFloatObserver(peprock.patterns.Observer[int, float]):
    def notify(
        self: peprock.patterns.Observer[int, float],
        __subject: peprock.patterns.Subject[int, float],
        /,
        int_value: int,
        float_value: float = 0.0,
    ):
        print(
            f"{type(self).__name__} got {int_value=}, {float_value=} from "
            f"{type(__subject).__name__}",
        )


@pytest.fixture(
    scope="session",
    params=[
        (_StrSubject, _StrObserver),
        (_IntFloatSubject, _IntFloatObserver),
    ],
)
def subject_and_observer_type(request):
    return request.param


@pytest.fixture(scope="session")
def subject_type(subject_and_observer_type):
    return subject_and_observer_type[0]


@pytest.fixture
def subject(subject_type):
    return subject_type()


@pytest.fixture(scope="session")
def observer_type(subject_and_observer_type):
    return subject_and_observer_type[1]


@pytest.fixture
def observer(observer_type):
    return observer_type()


class TestSubject:
    def test_register_observer(self, subject, observer):
        # ensure observer is initially unregistered
        assert not subject._observers

        # set of observers contains observer after registration
        subject.register_observer(observer)
        assert observer in subject._observers

        # check for idempotency
        subject.register_observer(observer)
        assert observer in subject._observers

    def test_unregister_observer(self, subject, observer):
        # ensure observer is initially unregistered
        assert not subject._observers

        # set of observers does not contain observer after unregistration
        subject.register_observer(observer)
        assert observer in subject._observers
        subject.unregister_observer(observer)
        assert observer not in subject._observers

        # check for idempotency
        subject.unregister_observer(observer)
        assert observer not in subject._observers

    def test_is_registered_observer(self, subject, observer):
        # ensure observer is initially unregistered
        assert subject.is_registered_observer(observer) is False

        # result is True for registered observer
        subject.register_observer(observer)
        assert subject.is_registered_observer(observer) is True

        # result is False for unregistered observer
        subject.unregister_observer(observer)
        assert subject.is_registered_observer(observer) is False

    def test_notify_observers(self, subject, observer, capsys):
        match subject:
            case _StrSubject():
                args = ("test_1",)
                kwargs = {}
                output = "_StrObserver got str_value='test_1' from _StrSubject\n"
            case _IntFloatSubject():
                args = (345,)
                kwargs = {
                    "float_value": 23.4,
                }
                output = (
                    "_IntFloatObserver got int_value=345, float_value=23.4 from "
                    "_IntFloatSubject\n"
                )
            case _:
                raise NotImplementedError(subject)

        observer_1 = observer
        observer_2 = copy.copy(observer)

        # ensure observers are initially unregistered
        assert not subject._observers

        # no unregistered observer notified
        subject.notify_observers(*args, **kwargs)
        captured = capsys.readouterr()
        assert not captured.out
        assert not captured.err

        # only registered observer notified
        subject.register_observer(observer_1)
        subject.notify_observers(*args, **kwargs)
        captured = capsys.readouterr()
        assert captured.out == output
        assert not captured.err

        # both registered observers notified
        subject.register_observer(observer_2)
        subject.notify_observers(*args, **kwargs)
        captured = capsys.readouterr()
        assert captured.out == 2 * output
        assert not captured.err

        # only registered observer notified
        subject.unregister_observer(observer_1)
        subject.notify_observers(*args, **kwargs)
        captured = capsys.readouterr()
        assert captured.out == output
        assert not captured.err

        # no unregistered observer notified
        subject.unregister_observer(observer_2)
        subject.notify_observers(*args, **kwargs)
        captured = capsys.readouterr()
        assert not captured.out
        assert not captured.err


class TestObserver:
    @pytest.mark.parametrize(
        (
            "observer",
            "subject",
            "args",
            "kwargs",
            "output",
        ),
        [
            (
                _StrObserver(),
                _StrSubject(),
                ("test_1",),
                {},
                "_StrObserver got str_value='test_1' from _StrSubject\n",
            ),
            (
                _StrObserver(),
                _StrSubject(),
                (),
                {
                    "str_value": "test_2",
                },
                "_StrObserver got str_value='test_2' from _StrSubject\n",
            ),
            (
                _IntFloatObserver(),
                _IntFloatSubject(),
                (123,),
                {},
                "_IntFloatObserver got int_value=123, float_value=0.0 from "
                "_IntFloatSubject\n",
            ),
            (
                _IntFloatObserver(),
                _IntFloatSubject(),
                (234, 12.3),
                {},
                "_IntFloatObserver got int_value=234, float_value=12.3 from "
                "_IntFloatSubject\n",
            ),
            (
                _IntFloatObserver(),
                _IntFloatSubject(),
                (345,),
                {
                    "float_value": 23.4,
                },
                "_IntFloatObserver got int_value=345, float_value=23.4 from "
                "_IntFloatSubject\n",
            ),
            (
                _IntFloatObserver(),
                _IntFloatSubject(),
                (),
                {
                    "int_value": 456,
                },
                "_IntFloatObserver got int_value=456, float_value=0.0 from "
                "_IntFloatSubject\n",
            ),
            (
                _IntFloatObserver(),
                _IntFloatSubject(),
                (),
                {
                    "int_value": 567,
                    "float_value": 34.5,
                },
                "_IntFloatObserver got int_value=567, float_value=34.5 from "
                "_IntFloatSubject\n",
            ),
        ],
    )
    def test_notify(self, observer, subject, args, kwargs, output, capsys):
        observer.notify(subject, *args, **kwargs)
        captured = capsys.readouterr()
        assert captured.out == output
        assert not captured.err
