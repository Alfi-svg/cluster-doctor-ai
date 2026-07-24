"""
MQTT Topic Manager
"""

from app.mqtt.topics import Topics


class TopicManager:

    def telemetry(self):

        return Topics.TELEMETRY

    def prediction(self):

        return Topics.PREDICTION

    def recommendation(self):

        return Topics.AI_RECOMMENDATION

    def heartbeat(self):

        return Topics.HEARTBEAT

    def beacon(self):

        return Topics.BEACON_REQUEST

    def subscribe(self):

        return Topics.subscribe_topics()

    def publish(self):

        return Topics.publish_topics()


topic_manager = TopicManager()