from unittest import TestCase

from fastapi.testclient import TestClient

from katalogus.api import app
from katalogus.dependencies.plugins import get_plugin_service
from katalogus.routers.organisations import check_organisation_exists
from katalogus.tests.test_plugin_service import mock_plugin_service


class TestPlugins(TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_plugin_service] = mock_plugin_service
        app.dependency_overrides[check_organisation_exists] = lambda: None

        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    def test_list(self):
        res = self.client.get("/v1/organisations/test-org/plugins")
        self.assertEqual(200, res.status_code)
        self.assertSetEqual(
            {
                "test-boefje-1",
                "test-boefje-2",
                "test-bit-1",
                "test-normalizer-1",
                "kat_test",
                "kat_test_normalize",
            },
            set([x["id"] for x in res.json()]),
        )

    def test_list_repository(self):
        res = self.client.get(
            "/v1/organisations/test-org/repositories/test-repo/plugins"
        )
        self.assertEqual(200, res.status_code)
        self.assertListEqual(
            ["test-boefje-1", "test-boefje-2"],
            list(res.json().keys()),
        )

    def test_list_repository2(self):
        res = self.client.get(
            "/v1/organisations/test-org/repositories/test-repo-2/plugins"
        )
        self.assertEqual(200, res.status_code)
        self.assertListEqual(
            ["test-bit-1", "test-normalizer-1"],
            list(res.json().keys()),
        )

    def test_get_plugin(self):
        res = self.client.get(
            "/v1/organisations/test-org/repositories/test-repo/plugins/test-boefje-1"
        )
        self.assertEqual(200, res.status_code)

    def test_non_existing_plugin(self):
        res = self.client.get(
            "/v1/organisations/test-org/repositories/test-repo/plugins/future-plugin"
        )
        self.assertEqual(404, res.status_code)

    def test_default_enabled_property_list(self):
        res = self.client.get(
            "/v1/organisations/test-org/repositories/test-repo/plugins"
        )
        self.assertEqual(200, res.status_code)
        self.assertFalse(any([plugin["enabled"] for plugin in res.json().values()]))

    def test_patching_enabled_state(self):
        res = self.client.patch(
            "/v1/organisations/test-org/repositories/test-repo/plugins/test-boefje-1",
            json={"enabled": False},
        )
        self.assertEqual(200, res.status_code)

        res = self.client.get("/v1/organisations/test-org/plugins")
        self.assertEqual(200, res.status_code)
        self.assertEqual(
            {
                "test-boefje-1": False,
                "test-boefje-2": False,
                "test-bit-1": True,
                "test-normalizer-1": True,
                "kat_test": False,
                "kat_test_normalize": True,
            },
            {plugin["id"]: plugin["enabled"] for plugin in res.json()},
        )
