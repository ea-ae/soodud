"""Test registry."""

import pytest
from typing import Callable

from data.stores import StoreRegistry


@pytest.fixture
def store_registry():
    """Returns a clean StoreRegistry."""
    registry = StoreRegistry
    yield registry
    registry.registry = []  # cleanup


@pytest.fixture
def store_func_factory() -> Callable[[str], Callable]:
    """Return a store factory."""
    def store_factory(name: str):
        """Create mock store entrypoints."""
        def store_main():
            """Mock store entrypoint."""
            nonlocal name
            return name
        return store_main
    return store_factory


@pytest.mark.django_db
@pytest.mark.parametrize('stores', [('coop', 'selver', 'rimi'), ('prisma',)])
def test_adding_stores(store_registry, store_func_factory, stores):
    """Test adding new stores to the store registry."""
    for store in stores:
        store_registry(store).__call__(store_func_factory(store))

    assert len(stores) == len(store_registry.registry)

    for test_store, registry_store in zip(stores, store_registry.registry):
        assert test_store == registry_store.name
        assert test_store == registry_store.entrypoint()
