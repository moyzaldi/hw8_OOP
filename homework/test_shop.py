"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product2():
    return Product("Pen", 1, "This is a pen", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_check_quantity_is_enough(self, product):
        assert not product.check_quantity(product.quantity + 1)

    def test_check_quantity_more(self, product):
        assert product.check_quantity(product.quantity)

    def test_product_buy_is_enough(self, product):
        quantity_before = product.quantity
        product.buy(100)
        assert product.quantity == quantity_before - 100

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


@pytest.fixture()
def cart() -> Cart:
    return Cart()


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, 10)
        assert cart.products[product] == 10

    def test_add_double_product(self, cart, product):
        cart.add_product(product, 10)
        cart.add_product(product, 10)
        assert cart.products[product] == 20

    def test_add_more_product(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)

    def test_add_zero_product(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, 0)

    def test_add_two_products(self, cart, product, product2):
        cart.add_product(product, 100)
        cart.add_product(product2, 100)
        assert cart.products[product] == 100 and cart.products[product2] == 100

    def test_remove_none_product(self, cart, product):
        cart.add_product(product, 100)
        cart.remove_product(product)
        assert cart.products == {}

    def test_remove_all_product(self, cart, product):
        q = 100
        cart.add_product(product, q)
        cart.remove_product(product, q)
        assert cart.products == {}

    def test_remove_more_product(self, cart, product):
        cart.add_product(product, product.quantity)
        cart.remove_product(product, remove_count=cart.products[product] + 1)
        assert cart.products == {}

    def test_remove_less_product(self, cart, product):
        q = 20
        cart.add_product(product, q)
        cart.remove_product(product, remove_count=q - 1)
        assert cart.products[product] == q - (q - 1)

    def test_remove_one_of_product(self, cart, product, product2):
        q = 20
        cart.add_product(product, q)
        cart.add_product(product2, q)
        cart.remove_product(product, remove_count=q - 1)
        assert cart.products[product] == q - (q - 1)
        assert cart.products[product2] == q

    def test_remove_another_product(self, cart, product, product2):
        with pytest.raises(ValueError):
            q = 20
            cart.add_product(product, q)
            cart.remove_product(product2, remove_count=q - 1)

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 100)
        cart.clear()
        # assert cart.products == {}
        assert not cart.products

    def test_clear_empty_cart(self, cart, product):
        cart.clear()
        # assert cart.products == {}
        assert not cart.products

    def test_total_price_one_product(self, cart, product):
        q_product = 100
        cart.add_product(product, 100)
        cart.get_total_price()
        total_price = cart.get_total_price()
        assert total_price == product.price * q_product

    def test_total_price_two_products(self, cart, product, product2):
        q_product = 100
        q_product2 = 100
        cart.add_product(product, 100)
        cart.add_product(product2, 100)
        cart.get_total_price()
        total_price = cart.get_total_price()
        assert total_price == product.price * q_product + product2.price * q_product2

    def test_buy_product(self, cart, product):
        product_in_storage = product.quantity
        q_product = 100
        cart.add_product(product, q_product)
        cart.buy()
        assert product.quantity == product_in_storage - q_product
        assert not cart.products

    def test_buy_two_product(self, cart, product, product2):
        product_in_storage = product.quantity
        product2_in_storage = product2.quantity
        q_product = 100
        q_product2 = 100
        cart.add_product(product, q_product)
        cart.add_product(product2, q_product2)
        cart.buy()

        assert product.quantity == product_in_storage - q_product
        assert product2.quantity == product2_in_storage - q_product2
        assert not cart.products

    def test_buy_over_product(self, cart, product):
        cart.add_product(product, product.quantity)
        cart.products[product] += 1
        with pytest.raises(ValueError):
            cart.buy()

    def test_buy_zero_product(self, cart, product):
        product_in_storage = product.quantity
        cart.add_product(product, 1)
        cart.products[product] = 0
        cart.buy()
        assert product.quantity == product_in_storage
