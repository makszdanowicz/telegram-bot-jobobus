# biblioteki do testowania
import unittest
from unittest.mock import AsyncMock, Mock

#biblioteki telegramu
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# paczki z funkcjami, które testujemy
from bot.utils.validators import validate_string_for_tags
from bot.handlers.employer.employer_states import AddJobOfferState

import unittest



class TestValidateString(unittest.TestCase):
    def test_validate_string_valid_inputs(self):
        # Testy dla poprawnych danych wejściowych
        self.assertTrue(validate_string_for_tags("poland"))
        self.assertTrue(validate_string_for_tags("united kingdom"))
        self.assertTrue(validate_string_for_tags("bosnia-herzegovina"))
        self.assertTrue(validate_string_for_tags("new zealand"))

    def test_validate_string_invalid_inputs(self):
        # Testy dla niepoprawnych danych wejściowych
        self.assertFalse(validate_string_for_tags("Poland"))  # Wielka litera
        self.assertFalse(validate_string_for_tags("united_kingdom"))  # Podkreślnik
        self.assertFalse(validate_string_for_tags("123"))  # Cyfry
        self.assertFalse(validate_string_for_tags("bosnia&herzegovina"))  # Niedozwolony znak &
        self.assertFalse(validate_string_for_tags("new@zealand"))  # Niedozwolony znak @
        self.assertFalse(validate_string_for_tags(""))  # Pusty ciąg
        self.assertFalse(validate_string_for_tags(" "))  # Samo miejsce
        self.assertFalse(validate_string_for_tags("  "))  # Kilka miejsc
        self.assertFalse(validate_string_for_tags("a"))  # Za krótki ciąg
        self.assertFalse(validate_string_for_tags("a-"))  # Jedna litera z myślnikiem
        self.assertFalse(validate_string_for_tags("-a"))  # Myślnik przed literą
        self.assertFalse(validate_string_for_tags("a "))  # Jedna litera ze spacją

if __name__ == "__main__":
    unittest.main()
