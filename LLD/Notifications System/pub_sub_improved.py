from typing import Dict, Set
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum, auto
from threading import Lock

# Message Types using Enum
class MessageType(Enum):
    NEWS = auto()
    WEATHER = auto()
    SPORTS = auto()

# Observer Pattern - Abstract Classes
class ISubscriber(ABC):
    @abstractmethod
    def receive_message(self, message: 'Message'):
        pass

class IPublisher(ABC):
    @abstractmethod
    def publish(self, topic: str, content: str):
        pass

# Message Value Object
@dataclass(frozen=True)
class Message:
    topic: str
    content: str
    type: MessageType
    timestamp: datetime = datetime.now()

# Singleton Pattern for PubSubService
class SingletonMeta(type):
    _instances = {}
    _lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class PubSubService(metaclass=SingletonMeta):
    def __init__(self):
        self.topics = {}

    def subscribe(self, topic: str, subscriber: ISubscriber):
        if topic not in self.topics:
            self.topics[topic] = set()
        self.topics[topic].add(subscriber)
        print(f"{subscriber.name} subscribed to {topic}")
    
    def unsubscribe(self, topic: str, subscriber: ISubscriber):
        if topic in self.topics:
            self.topics[topic].discard(subscriber)
            print(f"{subscriber.name} unsubscribed from {topic}")
    
    def notify(self, message: Message):
        if message.topic in self.topics:
            for subscriber in self.topics[message.topic]:
                subscriber.receive_message(message)

# Concrete Subscriber implementing Observer Pattern
class Subscriber(ISubscriber):
    def __init__(self, name: str):
        self.name = name
        self._messages: List[Message] = []  # Store messages
    
    def receive_message(self, message: Message):
        self._messages.append(message)
        print(f"{self.name} received: {message.content} from topic: {message.topic}")
    
    def get_message_history(self):
        return self._messages

# Concrete Publisher implementing Observer Pattern
class Publisher(IPublisher):
    def __init__(self, name: str, message_type: MessageType):
        self.name = name
        self.message_type = message_type
        self._pub_sub_service = PubSubService()
    
    def publish(self, topic: str, content: str):
        message = Message(topic, content, self.message_type)
        self._pub_sub_service.notify(message)
        print(f"{self.name} published: {content} to topic: {topic}")

# Factory Pattern for creating publishers
class PublisherFactory:
    @staticmethod
    def create_publisher(name: str, type: str) -> Publisher:
        message_type_map = {
            "news": MessageType.NEWS,
            "weather": MessageType.WEATHER,
            "sports": MessageType.SPORTS
        }
        message_type = message_type_map.get(type.lower())
        if not message_type:
            raise ValueError(f"Invalid publisher type: {type}")
        return Publisher(name, message_type)

# Command Pattern for message handling
class MessageCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

class PublishCommand(MessageCommand):
    def __init__(self, publisher: Publisher, topic: str, content: str):
        self.publisher = publisher
        self.topic = topic
        self.content = content
    
    def execute(self):
        self.publisher.publish(self.topic, self.content)

def main():
    # Create the pub/sub service (Singleton)
    pub_sub = PubSubService()
    
    # Create publishers using factory
    try:
        news_agency = PublisherFactory.create_publisher("NewsAgency", "news")
        weather_service = PublisherFactory.create_publisher("WeatherService", "weather")
    except ValueError as e:
        print(f"Error creating publisher: {e}")
        return
    
    # Create subscribers
    user1 = Subscriber("User1")
    user2 = Subscriber("User2")
    user3 = Subscriber("User3")
    
    # Subscribe to topics
    pub_sub.subscribe("news", user1)
    pub_sub.subscribe("news", user2)
    pub_sub.subscribe("weather", user2)
    pub_sub.subscribe("weather", user3)
    
    print("\nPublishing messages using Command pattern:")
    # Create and execute commands
    commands = [
        PublishCommand(news_agency, "news", "Breaking: Python 4.0 released!"),
        PublishCommand(weather_service, "weather", "Today will be sunny!")
    ]
    
    for command in commands:
        command.execute()
    
    print("\nUnsubscribing User2 from news:")
    pub_sub.unsubscribe("news", user2)
    
    # Check message history
    print("\nUser1's message history:")
    for msg in user1.get_message_history():
        print(f"- {msg.content} ({msg.type.name})")

if __name__ == "__main__":
    main() 