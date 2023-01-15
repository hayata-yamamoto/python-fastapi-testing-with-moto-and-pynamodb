from unittest import TestCase
from uuid import uuid4

from fastapi.exceptions import HTTPException
from moto import mock_dynamodb
from starlette.testclient import TestClient

from main import Item, app, get_valid_item


class TestApp(TestCase):
    def setUp(self) -> None:
        self.mock_dynamodb = mock_dynamodb()
        self.mock_dynamodb.start()

        self.test_client = TestClient(app)
        Item.create_table()

        self.test_item = Item(
            id=str(uuid4()), name="test", description="test", price=100, tax=0.1
        )
        self.test_item.save()

    def tearDown(self) -> None:
        self.mock_dynamodb.stop()

    def test_create_item(self) -> None:
        payload = {"name": "item1", "description": "item1 description", "price": 100}
        r = self.test_client.post(url="/items", json=payload)
        self.assertEqual(200, r.status_code)

        item = Item.get(r.json()["id"])
        self.assertTrue(item.exists())

    def test_get_valid_item(self) -> None:
        item = get_valid_item(self.test_item.id)
        self.assertTrue(item.exists())

        with self.assertRaises(HTTPException):
            get_valid_item("dummy-id")

    def test_put_item(self) -> None:
        payload = {
            "name": "item1",
            "description": "item1 description",
            "price": 100,
            "version": self.test_item.version,
        }
        r = self.test_client.put(url=f"/items/{self.test_item.id}", json=payload)
        self.assertEqual(200, r.status_code)
        self.assertEqual(self.test_item.version + 1, r.json()["version"])
