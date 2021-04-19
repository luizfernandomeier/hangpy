from hangpy.services import PrintLogService
from unittest import TestCase, mock, main


def get_mock(method_mocked: str, args) -> mock.MagicMock:
    return next(mock for mock in args if f'name=\'{method_mocked}\'' in str(mock))


class TestPrintLogService(TestCase):

    @mock.patch('builtins.print')
    def test_instantiate(self, *args):
        log_service = PrintLogService()
        self.assertIsNone(log_service.log("some test message"))
        actual_print = str(get_mock('print', args).call_args[0][0])
        self.assertEqual(actual_print, 'some test message')


if (__name__ == "__main__"):
    main()
