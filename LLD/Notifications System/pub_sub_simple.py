from typing import Dict, Set, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """Simple message class to hold content and metadata"""
    topic: str
    content: str
    timestamp: datetime = datetime.now()

class PubSub:
    """Central PubSub system managing subscribers and message delivery"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.topics = {}
        return cls._instance

    def subscribe(self, topic: str, subscriber: 'Subscriber') -> None:
        """Subscribe to a topic"""
        if topic not in self.topics:
            self.topics[topic] = set()
        self.topics[topic].add(subscriber)
        print(f"{subscriber.name} subscribed to {topic}")

    def unsubscribe(self, topic: str, subscriber: 'Subscriber') -> None:
        """Unsubscribe from a topic"""
        if topic in self.topics:
            self.topics[topic].discard(subscriber)
            print(f"{subscriber.name} unsubscribed from {topic}")

    def publish(self, topic: str, message: str) -> None:
        """Publish a message to a topic"""
        if topic in self.topics:
            msg = Message(topic=topic, content=message)
            for subscriber in self.topics[topic]:
                subscriber.receive(msg)

class Subscriber:
    """Subscriber class that can receive messages"""
    def __init__(self, name: str):
        self.name = name
        self.messages: List[Message] = []
    
    def receive(self, message: Message) -> None:
        """Receive and store a message"""
        self.messages.append(message)
        print(f"{self.name} received: {message.content}")
    
    def get_messages(self) -> List[Message]:
        """Get all received messages"""
        return self.messages

def main():
    # Create PubSub instance
    pubsub = PubSub()
    
    # Create subscribers
    john = Subscriber("John")
    jane = Subscriber("Jane")
    bob = Subscriber("Bob")
    
    # Subscribe to topics
    pubsub.subscribe("news", john)
    pubsub.subscribe("news", jane)
    pubsub.subscribe("weather", jane)
    pubsub.subscribe("weather", bob)
    
    print("\nPublishing messages:")
    # Publish messages
    pubsub.publish("news", "Breaking: Python 4.0 released!")
    pubsub.publish("weather", "Today will be sunny!")
    
    print("\nUnsubscribing Jane from news:")
    pubsub.unsubscribe("news", jane)
    
    pubsub.publish("news", "Python 5.0 in development!")
    
    # Show message history
    print("\nMessage History:")
    for subscriber in [john, jane, bob]:
        print(f"\n{subscriber.name}'s messages:")
        for msg in subscriber.get_messages():
            print(f"- {msg.content} (Topic: {msg.topic})")

if __name__ == "__main__":
    main()