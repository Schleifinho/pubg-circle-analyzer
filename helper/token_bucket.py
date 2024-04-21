import time
import threading


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.refill_rate = refill_rate
        self.token_available_event = threading.Event()

    def refill(self):
        now = time.time()
        time_since_last_refill = now - self.last_refill_time
        tokens_to_add = time_since_last_refill * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now
        self.token_available_event.set()  # Set the event to signal token availability

    def consume(self, tokens):
        self.refill()
        while tokens > self.tokens:
            self.token_available_event.clear()  # Clear the event to indicate no tokens available
            time.sleep(0.1)  # Sleep briefly before checking again
            self.refill()  # Refill tokens
        self.tokens -= tokens
        if self.tokens < self.capacity:
            self.token_available_event.set()  # Set the event if tokens are available
        return True
