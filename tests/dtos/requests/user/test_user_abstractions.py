import pytest

from tests.dtos.requests.test_requests_abstractions import TestIRequestDTO


@pytest.mark.asyncio
class TestIUserRequestDTO(TestIRequestDTO):

    @pytest.fixture
    def email(self):
        return "test@test.com"

    @pytest.fixture
    def password(self):
        return "test_password"
