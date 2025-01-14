# biblioteki do testowania
import unittest
from unittest.mock import AsyncMock, Mock

#biblioteki telegramu
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# paczki z funkcjami, które testujemy
from bot.handlers.employer.employer_handlers import validate_string
from bot.handlers.employer.employer_states import AddJobOfferState

import unittest
from bot.handlers.employer.employer_handlers import validate_string


class TestValidateString(unittest.TestCase):
    def test_validate_string_valid_inputs(self):
        # Testy dla poprawnych danych wejściowych
        self.assertTrue(validate_string("poland"))
        self.assertTrue(validate_string("united kingdom"))
        self.assertTrue(validate_string("bosnia-herzegovina"))
        self.assertTrue(validate_string("new zealand"))

    def test_validate_string_invalid_inputs(self):
        # Testy dla niepoprawnych danych wejściowych
        self.assertFalse(validate_string("Poland"))  # Wielka litera
        self.assertFalse(validate_string("united_kingdom"))  # Podkreślnik
        self.assertFalse(validate_string("123"))  # Cyfry
        self.assertFalse(validate_string("bosnia&herzegovina"))  # Niedozwolony znak &
        self.assertFalse(validate_string("new@zealand"))  # Niedozwolony znak @
        self.assertFalse(validate_string(""))  # Pusty ciąg
        self.assertFalse(validate_string(" "))  # Samo miejsce
        self.assertFalse(validate_string("  "))  # Kilka miejsc
        self.assertFalse(validate_string("a"))  # Za krótki ciąg
        self.assertFalse(validate_string("a-"))  # Jedna litera z myślnikiem
        self.assertFalse(validate_string("-a"))  # Myślnik przed literą
        self.assertFalse(validate_string("a "))  # Jedna litera ze spacją

if __name__ == "__main__":
    unittest.main()
