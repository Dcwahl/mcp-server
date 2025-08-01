"""
Caching System for MCP Development Server

Implements content-hash based caching for expensive operations,
inspired by Serena's caching strategy with immediate invalidation on file changes.
"""

import os
import json
import hashlib
import pickle
import time
from typing import Any, Optional, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Content-hash based caching system with automatic invalidation.
    
    Features:
    - File content-based cache keys
    - Automatic invalidation when files change
    - Performance metrics tracking
    - Configurable cache size limits
    """
    
    def __init__(self, cache_dir: str = None, max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir or "/tmp/mcp-server-cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size_mb = max_size_mb
        
        # Performance tracking
        self.hits = 0
        self.misses = 0
        self.invalidations = 0
        
        # File watching for invalidation
        self._file_hashes: Dict[str, str] = {}
        
    def _get_file_hash(self, file_path: str) -> str:
        """Get content hash of a file"""
        if not os.path.exists(file_path):
            return "nonexistent"
            
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash file {file_path}: {e}")
            return str(os.path.getmtime(file_path))
    
    def _build_cache_key(self, base_key: str, file_deps: list = None) -> str:
        """
        Build a cache key that includes file content hashes.
        
        Args:
            base_key: Base cache key from the tool
            file_deps: List of file paths this cache entry depends on
            
        Returns:
            Complete cache key including file hashes
        """
        key_parts = [base_key]
        
        if file_deps:
            for file_path in file_deps:
                file_hash = self._get_file_hash(file_path)
                key_parts.append(f"{file_path}:{file_hash}")
                
        return hashlib.md5("|".join(key_parts).encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache entry"""
        return self.cache_dir / f"{cache_key}.cache"
    
    def _cleanup_old_entries(self):
        """Remove LRU entries if cache is too large"""
        try:
            # Get all cache files with their access times
            cache_files = []
            total_size = 0
            
            for cache_file in self.cache_dir.glob("*.cache"):
                if cache_file.exists():
                    stat = cache_file.stat()
                    cache_files.append((cache_file, stat.st_atime, stat.st_size))
                    total_size += stat.st_size
            
            # If we're over the limit, remove oldest files
            max_size_bytes = self.max_size_mb * 1024 * 1024
            if total_size > max_size_bytes:
                # Sort by access time (oldest first)
                cache_files.sort(key=lambda x: x[1])
                
                for cache_file, _, size in cache_files:
                    cache_file.unlink()
                    total_size -= size
                    if total_size <= max_size_bytes:
                        break
                        
                logger.info(f"Cleaned up cache, new size: {total_size / 1024 / 1024:.1f} MB")
                
        except Exception as e:
            logger.warning(f"Cache cleanup failed: {e}")
    
    def get(self, cache_key: str, file_deps: list = None) -> Optional[Any]:
        """
        Get cached value if valid.
        
        Args:
            cache_key: Base cache key
            file_deps: Files this cache depends on
            
        Returns:
            Cached value or None if not found/invalid
        """
        try:
            full_key = self._build_cache_key(cache_key, file_deps)
            cache_path = self._get_cache_path(full_key)
            
            if not cache_path.exists():
                self.misses += 1
                return None
            
            # Load cached data
            with open(cache_path, 'rb') as f:
                cached_data = pickle.load(f)
            
            # Update access time
            cache_path.touch()
            
            self.hits += 1
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_data
            
        except Exception as e:
            logger.warning(f"Cache get failed for {cache_key}: {e}")
            self.misses += 1
            return None
    
    def set(self, cache_key: str, value: Any, file_deps: list = None) -> None:
        """
        Store value in cache.
        
        Args:
            cache_key: Base cache key
            value: Value to cache
            file_deps: Files this cache depends on
        """
        try:
            full_key = self._build_cache_key(cache_key, file_deps)
            cache_path = self._get_cache_path(full_key)
            
            # Store the cached data
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            
            # Track file dependencies for future invalidation
            if file_deps:
                for file_path in file_deps:
                    self._file_hashes[file_path] = self._get_file_hash(file_path)
            
            logger.debug(f"Cached result for key: {cache_key}")
            
            # Cleanup if needed
            self._cleanup_old_entries()
            
        except Exception as e:
            logger.warning(f"Cache set failed for {cache_key}: {e}")
    
    def invalidate_file(self, file_path: str) -> int:
        """
        Invalidate all cache entries that depend on a file.
        
        Args:
            file_path: Path to file that changed
            
        Returns:
            Number of entries invalidated
        """
        try:
            invalidated = 0
            current_hash = self._get_file_hash(file_path)
            old_hash = self._file_hashes.get(file_path)
            
            # If file hash changed, invalidate related entries
            if old_hash and old_hash != current_hash:
                # This is a simplified approach - in practice we'd need more sophisticated
                # dependency tracking to know exactly which cache entries to invalidate
                pattern = hashlib.md5(file_path.encode()).hexdigest()[:8]
                
                for cache_file in self.cache_dir.glob("*.cache"):
                    # This is a heuristic - ideally we'd store dependency metadata
                    if pattern in cache_file.name:
                        cache_file.unlink()
                        invalidated += 1
                
                # Update stored hash
                self._file_hashes[file_path] = current_hash
                self.invalidations += invalidated
                
                if invalidated > 0:
                    logger.info(f"Invalidated {invalidated} cache entries for {file_path}")
            
            return invalidated
            
        except Exception as e:
            logger.warning(f"Cache invalidation failed for {file_path}: {e}")
            return 0
    
    def clear(self) -> int:
        """Clear all cache entries"""
        try:
            cleared = 0
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
                cleared += 1
                
            self._file_hashes.clear()
            logger.info(f"Cleared {cleared} cache entries")
            return cleared
            
        except Exception as e:
            logger.warning(f"Cache clear failed: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        # Get cache size info
        cache_size = 0
        entry_count = 0
        for cache_file in self.cache_dir.glob("*.cache"):
            if cache_file.exists():
                cache_size += cache_file.stat().st_size
                entry_count += 1
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "invalidations": self.invalidations,
            "cache_size_mb": cache_size / 1024 / 1024,
            "entry_count": entry_count,
            "max_size_mb": self.max_size_mb
        }


# Global cache manager instance
cache_manager = CacheManager()


def cached_tool_execution(func):
    """
    Decorator for caching tool execution results.
    
    The decorated tool should implement get_cache_key() method
    and optionally get_file_dependencies() method.
    """
    def wrapper(tool_instance, **kwargs):
        # Check if tool supports caching
        cache_key = tool_instance.get_cache_key(**kwargs)
        if not cache_key:
            return func(tool_instance, **kwargs)
        
        # Get file dependencies if tool supports it
        file_deps = None
        if hasattr(tool_instance, 'get_file_dependencies'):
            file_deps = tool_instance.get_file_dependencies(**kwargs)
        
        # Try to get from cache
        cached_result = cache_manager.get(cache_key, file_deps)
        if cached_result is not None:
            return cached_result
        
        # Execute and cache result
        result = func(tool_instance, **kwargs)
        cache_manager.set(cache_key, result, file_deps)
        
        return result
    
    return wrapper
