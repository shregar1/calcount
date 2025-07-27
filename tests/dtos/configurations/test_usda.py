from pydantic import ValidationError
import pytest

from dtos.configurations.usda import USDAConfigurationDTO

from tests.dtos.configurations.test_configuration_abstractions import (
    TestIConfigurationDTO,
)


@pytest.mark.asyncio
class TestDBConfigurationDTO(TestIConfigurationDTO):

    @pytest.fixture
    def url(self):
        return "test_url"

    async def test_usda_configuration_dto_all_field_valid(
        self,
        url: str,
    ):
        configuration_dto = USDAConfigurationDTO(
            url=url,
        )

        assert configuration_dto.url == url

    async def test_usda_configuration_dto_all_none_error(self):

        with pytest.raises(ValidationError) as exc_info:
            USDAConfigurationDTO(
                url=None,
            )

        assert isinstance(exc_info.value.errors(), list)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["input"] is None
