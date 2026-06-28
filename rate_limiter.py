import asyncio
import time
import logging
from typing import Dict, Tuple

# Setup structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TokenBucketLimiter")

class TokenBucketLimiter:
    """
    Thread-safe asynchronous rate limiter implementing the Token Bucket algorithm.
    Used to protect sensitive endpoints from brute-force and resource exhaustion.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity          # Maximum tokens allowed in bucket
        self.refill_rate = refill_rate    # Tokens added per second
        self.buckets: Dict[str, Tuple[float, float]] = {} # Client IP -> (tokens, last_update_time)

    def _refresh_tokens(self, client_id: str) -> float:
        """Calculates current tokens based on elapsed time since last request."""
        current_time = time.time()
        if client_id not in self.buckets:
            self.buckets[client_id] = (self.capacity, current_time)
            return self.capacity

        last_tokens, last_update = self.buckets[client_id]
        elapsed = current_time - last_update
        
        # Calculate newly generated tokens
        new_tokens = last_tokens + (elapsed * self.refill_rate)
        current_tokens = min(self.capacity, new_tokens)
        
        self.buckets[client_id] = (current_tokens, current_time)
        return current_tokens

    async def is_allowed(self, client_id: str, tokens_requested: int = 1) -> bool:
        """Determines if the client request falls within authorized rate thresholds."""
        current_tokens = self._refresh_tokens(client_id)

        if current_tokens >= tokens_requested:
            # Consume tokens
            remaining_tokens = current_tokens - tokens_requested
            self.buckets[client_id] = (remaining_tokens, time.time())
            logger.info(f"Access GRANTED for {client_id}. Remaining security tokens: {round(remaining_tokens, 2)}")
            return True
        
        logger.warning(f"Access DENIED for {client_id}. Rate limit threshold breached.")
        return False

async def main():
    # Allow max 3 requests, refills at 1 token per second
    limiter = TokenBucketLimiter(capacity=3, refill_rate=1.0)
    target_ip = "192.168.43.10"

    logger.info("Simulating high-frequency request burst (DDoS simulation)...")
    # Simulate rapid successive hits
    for i in range(5):
        await limiter.is_allowed(target_ip)
        await asyncio.sleep(0.1)

    logger.info("Simulating cooldown period for token refill...")
    await asyncio.sleep(2.0)
    
    logger.info("Simulating subsequent request post-refill...")
    await limiter.is_allowed(target_ip)

if __name__ == "__main__":
    asyncio.run(main())
