from threading import Lock
from collections import OrderedDict
from typing import Optional, Any
import threading
import time

class LRUCache:
    """Thread-safe LRU Cache implementation"""
    
    def __init__(self, capacity: int):
        """Initialize LRU Cache with given capacity"""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = Lock()  # Thread lock for synchronization
        
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value for key and mark as most recently used.
        Returns -1 if key doesn't exist.
        Thread-safe operation.
        """
        with self.lock:
            if key not in self.cache:
                return -1
            
            # Move to end (most recently used)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
            
    def put(self, key: Any, value: Any) -> None:
        """
        Put key-value pair into cache.
        If key exists, update value and mark as most recently used.
        If cache is full, remove least recently used item.
        Thread-safe operation.
        """
        with self.lock:
            if key in self.cache:
                # Remove existing key-value pair
                self.cache.pop(key)
            elif len(self.cache) >= self.capacity:
                # Remove least recently used item (first item)
                self.cache.popitem(last=False)
            
            # Add new key-value pair (most recently used)
            self.cache[key] = value
    
    def clear(self) -> None:
        """Clear all items from cache"""
        with self.lock:
            self.cache.clear()
    
    def get_size(self) -> int:
        """Get current size of cache"""
        with self.lock:
            return len(self.cache)
    
    def is_full(self) -> bool:
        """Check if cache is full"""
        with self.lock:
            return len(self.cache) >= self.capacity
    
    def peek(self, key: Any) -> Optional[Any]:
        """
        Get value for key without marking as most recently used.
        Returns -1 if key doesn't exist.
        """
        with self.lock:
            return self.cache.get(key, -1)

def test_concurrent_access():
    """Test concurrent access to LRU Cache"""
    cache = LRUCache(2)
    
    def worker1():
        for i in range(5):
            cache.put(f'key{i}', f'value{i}')
            time.sleep(0.1)
    
    def worker2():
        for i in range(5):
            cache.get(f'key{i}')
            time.sleep(0.1)
    
    # Create and start threads
    thread1 = threading.Thread(target=worker1)
    thread2 = threading.Thread(target=worker2)
    
    thread1.start()
    thread2.start()
    
    # Wait for threads to complete
    thread1.join()
    thread2.join()
    
    return cache

def main():
    # Basic usage test
    cache = LRUCache(2)
    
    print("Testing basic operations:")
    cache.put(1, 'one')
    cache.put(2, 'two')
    print(f"Get 1: {cache.get(1)}")  # Returns 'one'
    
    cache.put(3, 'three')  # Evicts key 2
    print(f"Get 2: {cache.get(2)}")  # Returns -1 (not found)
    print(f"Get 3: {cache.get(3)}")  # Returns 'three'
    
    # Test concurrent access
    print("\nTesting concurrent access:")
    concurrent_cache = test_concurrent_access()
    print(f"Final cache size: {concurrent_cache.get_size()}")
    
    # Performance test
    print("\nTesting performance:")
    large_cache = LRUCache(1000)
    
    start_time = time.time()
    for i in range(1000):
        large_cache.put(f'key{i}', f'value{i}')
    end_time = time.time()
    
    print(f"Time to insert 1000 items: {end_time - start_time:.4f} seconds")
    
    start_time = time.time()
    for i in range(1000):
        large_cache.get(f'key{i}')
    end_time = time.time()
    
    print(f"Time to retrieve 1000 items: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main() 