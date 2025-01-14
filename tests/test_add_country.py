# biblioteki do testowania
import unittest
from unittest.mock import AsyncMock, Mock

#biblioteki telegramu
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# paczki z funkcjami, które testujemy
from bot.handlers.employer.employer_handlers import add_country
from bot.handlers.employer.employer_states import AddJobOfferState

"""
W Pythonie mocki są dostępne dzięki modułowi unittest.mock. Najczęściej używane klasy i metody:

Mock – tworzy mock obiekt.
AsyncMock – do mockowania funkcji asynchronicznych.
patch – tymczasowo zamienia rzeczywisty obiekt w mock w określonym zakresie (np. dla konkretnej funkcji).
assert_called_once_with – sprawdza, czy mock został wywołany dokładnie raz z podanymi argumentami.

"""


# Mock the `validate_string` function
def mock_validate_string(s: str) -> bool:
    return s.isalpha() or (" " in s or "-" in s)

class TestEmployerHandlers(unittest.IsolatedAsyncioTestCase):

    async def test_process_country_valid_lowercase(self):
        # Mock the message and state
        message = Mock(spec=Message)
        message.text = "Poland"  # Użytkownik wprowadza nazwę z wielką literą
        message.answer = AsyncMock()
        
        state = Mock(spec=FSMContext)
        state.update_data = AsyncMock()
        state.set_state = AsyncMock()

        # Call the handler
        await add_country(message, state)

        # Assert that the country was converted to lowercase
        state.update_data.assert_called_once_with(country="poland")  # Zapisane jako małe litery

        # Assert that the message.answer was called with the next prompt
        message.answer.assert_called_once_with("Enter the city for the job offer (for example Wroclaw)")

        # Assert that the state.set_state was called with the next state
        state.set_state.assert_called_once_with(AddJobOfferState.city)

    async def test_process_country_invalid_characters(self):
        # Mock the message and state
        message = Mock(spec=Message)
        message.text = "Pol@nd"  # Invalid due to '@'
        message.answer = AsyncMock()
        
        state = Mock(spec=FSMContext)
        state.update_data = AsyncMock()
        state.set_state = AsyncMock()

        # Patch validate_string
        validate_string = Mock(return_value=False)

        # Call the handler
        await add_country(message, state)

        # Assert that the message.answer was called with the correct response
        message.answer.assert_called_once_with('Use only english alphabet, spaces and "-"')
        state.update_data.assert_not_called()
        state.set_state.assert_not_called()

    async def test_process_country_invalid_length(self):
        # Mock the message and state
        message = Mock(spec=Message)
        message.text = "A"  # Invalid because it's too short
        message.answer = AsyncMock()
        
        state = Mock(spec=FSMContext)
        state.update_data = AsyncMock()
        state.set_state = AsyncMock()

        # Call the handler
        await add_country(message, state)

        # Assert that the message.answer was called with the correct response
        message.answer.assert_called_once_with('Use only english alphabet, spaces and "-"')
        state.update_data.assert_not_called()
        state.set_state.assert_not_called()

    async def test_process_country_valid(self):
        # Mock the message and state
        message = Mock(spec=Message)
        message.text = "Poland"
        message.answer = AsyncMock()
        
        state = Mock(spec=FSMContext)
        state.update_data = AsyncMock()
        state.set_state = AsyncMock()

        # Call the handler
        await add_country(message, state)

        # Assert that the state.update_data was called with the correct data
        state.update_data.assert_called_once_with(country="poland")  # Country should be lowercase as per the function

        # Assert that the message.answer was called with the next prompt
        message.answer.assert_called_once_with("Enter the city for the job offer (for example Wroclaw)")

        # Assert that the state.set_state was called with the next state
        state.set_state.assert_called_once_with(AddJobOfferState.city)

    async def test_process_country_too_long(self):
        # Mock the message and state
        message = Mock(spec=Message)
        message.text = "The United Kingdom of Great Britain and Northern Ireland Extra"
        message.answer = AsyncMock()
        
        state = Mock(spec=FSMContext)
        state.update_data = AsyncMock()
        state.set_state = AsyncMock()

        # Call the handler
        await add_country(message, state)

        # Assert that the message.answer was called with the correct response
        message.answer.assert_called_once_with("Invalid country name. Please enter a valid country.")
        state.update_data.assert_not_called()
        state.set_state.assert_not_called()

if __name__ == '__main__':
    unittest.main()
