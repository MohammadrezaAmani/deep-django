# Copyright 2022 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ClusterMetadata(object):
    """
    Provides information about the Kafka cluster, brokers, and topics.
    Returned by list_topics().

    This class is typically not user instantiated.
    """

    def __init__(self):
        self.cluster_id = None
        """Cluster id string, if supported by the broker, else None."""
        self.controller_id = -1
        """Current controller broker id, or -1."""
        self.brokers = {}
        """Map of brokers indexed by the broker id (int). Value is a BrokerMetadata object."""
        self.topics = {}
        """Map of topics indexed by the topic name. Value is a TopicMetadata object."""
        self.orig_broker_id = -1
        """The broker this metadata originated from."""
        self.orig_broker_name = None
        """The broker name/address this metadata originated from."""

    def __repr__(self):
        return "ClusterMetadata({})".format(self.cluster_id)

    def __str__(self):
        return str(self.cluster_id)


class BrokerMetadata(object):
    """
    Provides information about a Kafka broker.

    This class is typically not user instantiated.
    """

    def __init__(self):
        self.id = -1
        """Broker id"""
        self.host = None
        """Broker hostname"""
        self.port = -1
        """Broker port"""

    def __repr__(self):
        return "BrokerMetadata({}, {}:{})".format(self.id, self.host, self.port)

    def __str__(self):
        return "{}:{}/{}".format(self.host, self.port, self.id)


class TopicMetadata(object):
    """
    Provides information about a Kafka topic.

    This class is typically not user instantiated.
    """

    # The dash in "-topic" and "-error" is needed to circumvent a
    # Sphinx issue where it tries to reference the same instance variable
    # on other classes which raises a warning/error.

    def __init__(self):
        self.topic = None
        """Topic name"""
        self.partitions = {}
        """Map of partitions indexed by partition id. Value is a PartitionMetadata object."""
        self.error = None
        """Topic error, or None. Value is a KafkaError object."""

    def __repr__(self):
        if self.error is not None:
            return "TopicMetadata({}, {} partitions, {})".format(
                self.topic, len(self.partitions), self.error
            )
        else:
            return "TopicMetadata({}, {} partitions)".format(
                self.topic, len(self.partitions)
            )

    def __str__(self):
        return self.topic


class PartitionMetadata(object):
    """
    Provides information about a Kafka partition.

    This class is typically not user instantiated.

    :warning: Depending on cluster state the broker ids referenced in
              leader, replicas and ISRs may temporarily not be reported
              in ClusterMetadata.brokers. Always check the availability
              of a broker id in the brokers dict.
    """

    def __init__(self):
        self.id = -1
        """Partition id."""
        self.leader = -1
        """Current leader broker for this partition, or -1."""
        self.replicas = []
        """List of replica broker ids for this partition."""
        self.isrs = []
        """List of in-sync-replica broker ids for this partition."""
        self.error = None
        """Partition error, or None. Value is a KafkaError object."""

    def __repr__(self):
        if self.error is not None:
            return "PartitionMetadata({}, {})".format(self.id, self.error)
        else:
            return "PartitionMetadata({})".format(self.id)

    def __str__(self):
        return "{}".format(self.id)


class GroupMember(object):
    """Provides information about a group member.

    For more information on the metadata format, refer to:
    `A Guide To The Kafka Protocol <https://cwiki.apache.org/confluence/display/KAFKA/A+Guide+To+The+Kafka+Protocol#AGuideToTheKafkaProtocol-GroupMembershipAPI>`_.

    This class is typically not user instantiated.
    """  # noqa: E501

    def __init__(
        self,
    ):
        self.id = None
        """Member id (generated by broker)."""
        self.client_id = None
        """Client id."""
        self.client_host = None
        """Client hostname."""
        self.metadata = None
        """Member metadata(binary), format depends on protocol type."""
        self.assignment = None
        """Member assignment(binary), format depends on protocol type."""


class GroupMetadata(object):
    """GroupMetadata provides information about a Kafka consumer group

    This class is typically not user instantiated.
    """

    def __init__(self):
        self.broker = None
        """Originating broker metadata."""
        self.id = None
        """Group name."""
        self.error = None
        """Broker-originated error, or None. Value is a KafkaError object."""
        self.state = None
        """Group state."""
        self.protocol_type = None
        """Group protocol type."""
        self.protocol = None
        """Group protocol."""
        self.members = []
        """Group members."""

    def __repr__(self):
        if self.error is not None:
            return "GroupMetadata({}, {})".format(self.id, self.error)
        else:
            return "GroupMetadata({})".format(self.id)

    def __str__(self):
        return self.id