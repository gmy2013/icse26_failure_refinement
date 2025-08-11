## main.py

from typing import List, Tuple, Dict, Optional, Any
import copy


class IceCreamType:
    """Represents an ice cream type with price and tastiness."""

    def __init__(self, price: int, tastiness: int) -> None:
        """Initializes an IceCreamType.

        Args:
            price: The price of the ice cream.
            tastiness: The tastiness value of the ice cream.
        """
        self.price: int = price
        self.tastiness: int = tastiness


class Store:
    """Represents a store with an inventory of ice creams and DP cache."""

    def __init__(self, inventory: Optional[List[IceCreamType]] = None) -> None:
        """Initializes a Store.

        Args:
            inventory: Optional initial inventory (deep copied if provided).
        """
        if inventory is not None:
            # Deep copy to ensure independence after cloning
            self.inventory: List[IceCreamType] = [IceCreamType(ic.price, ic.tastiness) for ic in inventory]
        else:
            self.inventory: List[IceCreamType] = []
        # DP cache: price_limit -> max tastiness
        self._dp_cache: Dict[int, int] = {}

    def clone(self) -> 'Store':
        """Creates a deep copy of the store (for cloning).

        Returns:
            A new Store instance with a deep-copied inventory.
        """
        return Store(self.inventory)

    def add_ice_cream(self, price: int, tastiness: int) -> None:
        """Adds a new ice cream to the inventory.

        Args:
            price: The price of the new ice cream.
            tastiness: The tastiness of the new ice cream.
        """
        self.inventory.append(IceCreamType(price, tastiness))
        self._invalidate_cache()

    def remove_oldest(self) -> None:
        """Removes the oldest ice cream from the inventory (FIFO)."""
        if self.inventory:
            self.inventory.pop(0)
            self._invalidate_cache()

    def max_tastiness(self, price_limit: int) -> int:
        """Computes the maximum tastiness under the given price limit.

        Args:
            price_limit: The maximum total price allowed.

        Returns:
            The maximum total tastiness achievable.
        """
        if price_limit in self._dp_cache:
            return self._dp_cache[price_limit]

        n = len(self.inventory)
        if n == 0 or price_limit <= 0:
            self._dp_cache[price_limit] = 0
            return 0

        # 0/1 Knapsack DP
        dp = [0] * (price_limit + 1)
        for idx, ice_cream in enumerate(self.inventory):
            p = ice_cream.price
            t = ice_cream.tastiness
            # Traverse backwards to avoid using the same item more than once
            for j in range(price_limit, p - 1, -1):
                if dp[j - p] + t > dp[j]:
                    dp[j] = dp[j - p] + t

        result = dp[price_limit]
        self._dp_cache[price_limit] = result
        return result

    def _invalidate_cache(self) -> None:
        """Invalidates the DP cache (call on inventory change)."""
        self._dp_cache.clear()


class StoreManager:
    """Manages multiple stores and their operations."""

    def __init__(self) -> None:
        """Initializes the StoreManager with a single empty store."""
        self.stores: List[Store] = [Store()]

    def open_store(self, x: int) -> int:
        """Clones store x and opens a new store.

        Args:
            x: The index of the store to clone (1-based).

        Returns:
            The new store's index (1-based).
        """
        if 1 <= x <= len(self.stores):
            new_store = self.stores[x - 1].clone()
            self.stores.append(new_store)
            return len(self.stores)
        else:
            raise IndexError("Store index out of range.")

    def add_ice_cream(self, x: int, price: int, tastiness: int) -> None:
        """Adds an ice cream to store x.

        Args:
            x: The store index (1-based).
            price: The price of the ice cream.
            tastiness: The tastiness of the ice cream.
        """
        if 1 <= x <= len(self.stores):
            self.stores[x - 1].add_ice_cream(price, tastiness)
        else:
            raise IndexError("Store index out of range.")

    def remove_oldest(self, x: int) -> None:
        """Removes the oldest ice cream from store x.

        Args:
            x: The store index (1-based).
        """
        if 1 <= x <= len(self.stores):
            self.stores[x - 1].remove_oldest()
        else:
            raise IndexError("Store index out of range.")

    def max_tastiness(self, x: int, price_limit: int) -> int:
        """Returns the max tastiness for store x under price_limit.

        Args:
            x: The store index (1-based).
            price_limit: The price limit.

        Returns:
            The maximum tastiness.
        """
        if 1 <= x <= len(self.stores):
            return self.stores[x - 1].max_tastiness(price_limit)
        else:
            raise IndexError("Store index out of range.")


class CommandProcessor:
    """Processes user commands and manages the store system."""

    def __init__(self, store_manager: StoreManager) -> None:
        """Initializes the CommandProcessor.

        Args:
            store_manager: The StoreManager instance to use.
        """
        self.store_manager: StoreManager = store_manager

    def process_query(self, query: str) -> Optional[str]:
        """Processes a single query string.

        Args:
            query: The query string.

        Returns:
            The result string for type 4 queries, or None for others.
        """
        tokens = query.strip().split()
        if not tokens:
            return None

        query_type = int(tokens[0])

        if query_type == 1:
            # 1 x: Open a new store by cloning store x
            x = int(tokens[1])
            new_store_idx = self.store_manager.open_store(x)
            # No output required for this operation
            return None
        elif query_type == 2:
            # 2 x p t: Add ice cream to store x
            x = int(tokens[1])
            p = int(tokens[2])
            t = int(tokens[3])
            self.store_manager.add_ice_cream(x, p, t)
            return None
        elif query_type == 3:
            # 3 x: Remove oldest ice cream from store x
            x = int(tokens[1])
            self.store_manager.remove_oldest(x)
            return None
        elif query_type == 4:
            # 4 x p: Query max tastiness in store x under price p
            x = int(tokens[1])
            p = int(tokens[2])
            result = self.store_manager.max_tastiness(x, p)
            return str(result)
        else:
            # Unknown query type
            return None

    def run(self, queries: List[str]) -> List[str]:
        """Processes a list of queries.

        Args:
            queries: The list of query strings.

        Returns:
            A list of result strings for type 4 queries.
        """
        results: List[str] = []
        for query in queries:
            res = self.process_query(query)
            if res is not None:
                results.append(res)
        return results


def main() -> None:
    """Main function to run the command-line application."""
    import sys

    store_manager = StoreManager()
    command_processor = CommandProcessor(store_manager)

    queries: List[str] = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            queries.append(line)

    results = command_processor.run(queries)
    for res in results:
        print(res)


if __name__ == "__main__":
    main()
