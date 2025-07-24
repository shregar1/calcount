import pytest
from datetime import datetime
from unittest.mock import Mock

from services.user.logout import UserLogoutService
from models.user import User
from errors.bad_input_error import BadInputError


@pytest.mark.asyncio
class TestUserLogoutService:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Setup runs before each test method"""
        # Create mock user
        self.mock_user = User(
            id=1,
            urn="test-urn",
            email="test@example.com",
            is_logged_in=True,
            updated_on=datetime.now(),
        )

        # Create service instance
        self.service = UserLogoutService(
            urn="test-urn", user_urn="test-user-urn", api_name="test-api"
        )
        self.service.user_repository.session = db_session

    async def test_successful_logout(self):
        # Arrange
        logout_data = {"user_id": 1}

        self.service.user_repository.retrieve_record_by_id_is_logged_in = Mock(
            return_value=self.mock_user
        )
        self.service.user_repository.update_record = Mock(
            return_value=self.mock_user
        )

        # Act
        result = await self.service.run(logout_data)

        # Assert
        assert result.status == "SUCCESS"
        assert result.data["status"] == self.mock_user.is_logged_in
        assert result.responseKey == "success_user_logout"
        assert "Successfully Logged Out the user" in result.responseMessage

    async def test_user_not_found(self, mocker):
        # Arrange
        logout_data = {"user_id": 2}  # Non-existent user ID

        mocker.patch.object(
            self.service.user_repository,
            "retrieve_record_by_id_is_logged_in",
            return_value=None,
        )

        # Act & Assert
        with pytest.raises(BadInputError) as exc_info:
            await self.service.run(logout_data)

        assert exc_info.value.responseKey == "error_authorisation_failed"
        assert "User not Found" in exc_info.value.responseMessage
        assert exc_info.value.http_status_code == 400

    async def test_logout_updates_user_status(self):
        # Arrange
        logout_data = {"user_id": 1}

        self.service.user_repository.retrieve_record_by_id_is_logged_in = Mock(
            return_value=self.mock_user
        )
        self.service.user_repository.update_record = Mock()

        # Act
        await self.service.run(logout_data)

        # Assert
        self.service.user_repository.update_record.assert_called_once()
        update_call_args = (
            self.service.user_repository.update_record.call_args[1]
        )
        assert update_call_args["id"] == self.mock_user.id
        assert update_call_args["new_data"]["is_logged_in"] is False

    async def test_user_already_logged_out(self):
        # Arrange
        logout_data = {"user_id": 1}

        # Create a user that's already logged out
        logged_out_user = User(
            id=1,
            urn="test-urn",
            email="test@example.com",
            is_logged_in=False,
            updated_on=datetime.now(),
        )

        self.service.user_repository.retrieve_record_by_id_is_logged_in = Mock(
            return_value=None  # Will return None because is_logged_in=False
        )

        # Act & Assert
        with pytest.raises(BadInputError) as exc_info:
            await self.service.run(logout_data)

        assert exc_info.value.responseKey == "error_authorisation_failed"
        assert "User not Found" in exc_info.value.responseMessage

    async def test_missing_user_id(self):
        # Arrange
        logout_data = {}  # Missing user_id

        # Act & Assert
        with pytest.raises(BadInputError) as exc_info:
            await self.service.run(logout_data)

        assert exc_info.value.responseKey == "error_authorisation_failed"
        assert "User not Found" in exc_info.value.responseMessage
