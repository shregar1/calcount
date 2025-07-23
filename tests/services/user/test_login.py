import os
import pytest
import bcrypt
from datetime import datetime
from unittest.mock import Mock

from services.user.login import UserLoginService
from models.user import User
from errors.bad_input_error import BadInputError


@pytest.mark.asyncio
class TestUserLoginService:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Setup runs before each test method"""
        self.test_password = "correct_password"
        self.salt = os.getenv("BCRYPT_SALT")
        self.hashed_password = bcrypt.hashpw(
            self.test_password.encode("utf8"), self.salt.encode("utf8")
        ).decode("utf8")

        # Create mock user
        self.mock_user = User(
            id=1,
            urn="test-urn",
            email="test@example.com",
            password=self.hashed_password,
            is_logged_in=False,
            updated_on=datetime.now(),
        )

        # Create service instance
        self.service = UserLoginService(
            urn="test-urn", user_urn="test-user-urn", api_name="test-api"
        )
        self.service.user_repository.session = db_session

    async def test_successful_login(self):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": self.test_password,
            "user_type": "COMPANY",
        }

        self.service.user_repository.retrieve_record_by_email_user_type_id = (
            Mock(return_value=self.mock_user)
        )
        self.service.user_repository.update_record = Mock(
            return_value=self.mock_user
        )
        self.service.jwt_utility.create_access_token = Mock(
            return_value="mock-jwt-token"
        )

        # Act
        result = await self.service.run(login_data)

        # Assert
        assert result.status == "SUCCESS"
        assert result.data["status"] == self.mock_user.is_logged_in
        assert result.data["token"] == "mock-jwt-token"
        assert result.data["user_urn"] == self.mock_user.urn

    async def test_user_not_found(self):
        # Arrange
        login_data = {
            "email": "nonexistent@example.com",
            "password": "any_password",
            "user_type": "COMPANY",
        }

        self.service.user_repository.retrieve_record_by_email_user_type_id = (
            Mock(return_value=None)
        )

        # Act & Assert
        with pytest.raises(BadInputError) as exc_info:
            await self.service.run(login_data)

        assert exc_info.value.responseKey == "error_authorisation_failed"
        assert "User not Found" in exc_info.value.responseMessage

    async def test_incorrect_password(self):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "wrong_password",
            "user_type": "COMPANY",
        }

        self.service.user_repository.retrieve_record_by_email_user_type_id = (
            Mock(return_value=self.mock_user)
        )

        # Act & Assert
        with pytest.raises(BadInputError) as exc_info:
            await self.service.run(login_data)

        assert exc_info.value.responseKey == "error_authorisation_failed"
        assert "Incorrect password" in exc_info.value.responseMessage

    async def test_login_updates_user_status(self):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": self.test_password,
            "user_type": "COMPANY",
        }

        self.service.user_repository.retrieve_record_by_email_user_type_id = (
            Mock(return_value=self.mock_user)
        )
        self.service.user_repository.update_record = Mock()
        self.service.jwt_utility.create_access_token = Mock(
            return_value="mock-jwt-token"
        )

        # Act
        await self.service.run(login_data)

        # Assert
        self.service.user_repository.update_record.assert_called_once()
        update_call_args = (
            self.service.user_repository.update_record.call_args[1]
        )
        assert update_call_args["id"] == self.mock_user.id
        assert update_call_args["new_data"]["is_logged_in"] is True
        assert "last_login" in update_call_args["new_data"]

    async def test_jwt_token_payload(self):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": self.test_password,
            "user_type": "COMPANY",
        }

        self.service.user_repository.retrieve_record_by_email_user_type_id = (
            Mock(return_value=self.mock_user)
        )
        self.service.user_repository.update_record = Mock(
            return_value=self.mock_user
        )

        create_token_mock = Mock(return_value="mock-jwt-token")
        self.service.jwt_utility.create_access_token = create_token_mock

        # Act
        await self.service.run(login_data)

        # Assert
        expected_payload = {
            "user_id": self.mock_user.id,
            "user_urn": self.mock_user.urn,
            "user_email": self.mock_user.email,
            "last_login": str(self.mock_user.updated_on),
        }
        self.service.jwt_utility.create_access_token.assert_called_once_with(
            data=expected_payload
        )
