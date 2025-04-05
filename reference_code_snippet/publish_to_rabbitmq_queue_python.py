#!/usr/bin/env python
import json
import os
import sys
import time
from datetime import date, datetime, timezone
from dateutil.tz import gettz

import pika

import logger
from app_config import AppConfig, Client, Entity
from util import fetch_transformed_records_from_query

log = logger.get_logger('PublishToQueue')


class PublishToQueue:

    def __init__(self, config_file_path=None):
        if config_file_path:
            self.app_config = AppConfig.get_app_config(config_file_path)
        else:
            self.app_config = AppConfig.get_app_config()
        self.enitity_channels_dict = {}

    def create_channel(self, exchange_name):
        credentials = pika.PlainCredentials(self.app_config.get_rabbitmq_connection_config('username'),
                                            self.app_config.get_rabbitmq_connection_config('password'))
        parameters = pika.ConnectionParameters(self.app_config.get_rabbitmq_connection_config('hostname'),
                                               int(self.app_config.get_rabbitmq_connection_config('port')),
                                               self.app_config.get_rabbitmq_connection_config('virtual_host'),
                                               credentials, heartbeat=6000)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type=self.app_config.get_staffing_rabbitmq_config('exchange_type'),
                                 durable=bool(self.app_config.get_staffing_rabbitmq_config('exchange_durable')))
        # channel.confirm_delivery()
        return channel

    def close_channels(self):
        for channel_name, channel in self.enitity_channels_dict.items():
            log.debug(f"Closing rabbit mq channel : {channel_name}")
            channel.close()

    def send_to_queue(self, client: Client, entity: Entity, transformed_records):
        channel_name = f'''{client.value}_{entity.value}'''
        exchange_name, routing_key = self.app_config.get_rabbit_mq_channel_configs(client=client.value,
                                                                                   entity=entity.value)
        # todo cache channel
        # if channel_name not in self.enitity_channels_dict:
        log.debug(f"creating channel : {channel_name}")
        if not exchange_name:
            raise Exception(
                f"missing exchange name for client : {client.value}, entity : {entity.value}")
        if not routing_key:
            raise Exception(
                f"missing routing key for client : {client.value}, entity : {entity.value}")
        channel = self.create_channel(exchange_name)

        # channel = self.enitity_channels_dict[channel_name]
        # if channel.is_closed or channel.connection.is_closed:
        #     channel = self.enitity_channels_dict[channel_name] = self.create_channel(exchange_name)

        published_count = self.send_to_jf_q(channel, transformed_records, exchange_name, routing_key)
        channel.close()
        return published_count

    def send_to_jf_q(self, channel, transformed_records, exchange_name, routing_key):
        records_published_count = 0
        if transformed_records:
            log.debug("publishing to queue")
            for item in transformed_records:
                message = json.dumps(self._del_none(item), default=self._json_default)
                channel.basic_publish(exchange=exchange_name,
                                      routing_key=routing_key,
                                      body=bytes(message, 'utf-8'))
                records_published_count += 1
                # log.debug(str(records_published_count) + f' :: {exchange_name} ' + item.get(
                #     'client').lower() + " :: " + message)
            log.debug(f"published count to queue : {records_published_count}")
        return records_published_count

    def _del_none(self, d):
        for key, value in list(d.items()):
            if value is None:
                del d[key]
            elif isinstance(value, dict):
                self._del_none(value)
        return d

    def _json_default(self, o):
        if type(o) is date:
            return o.isoformat()
        elif type(o) is datetime:
            return o.isoformat()

    def publish_data(self, client: Client, entity: Entity):
        table_name_mapping = {
            Entity.ORDER_BASE: '''"local".staffing_order_base''',
            Entity.TIPS: '''"local".staffing_tips''',
            Entity.DAILY_LOGIN: '''"staffing".staffing_daily_login''',
            Entity.ONBOARDING_BASE: '''"local".staffing_onboarding_base'''
        }
        query = f'''
            select * from {table_name_mapping[entity]} where client='{client.value}' and login_date between '2023-01-23' and '2023-01-29'
            order by client_rider_id ; 
        '''
        log.debug(f"Running query : ${query}")
        transformed_records = fetch_transformed_records_from_query(query, 'fetch')
        self.send_to_queue(client, entity, transformed_records)

    def consume_from_daily_login(self, channel):
        count = 0

        def callback(ch, method, properties, body):
            nonlocal count
            count += 1
            print(f"{count} : Body is " + str(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.queue_bind(exchange='staffing_dailyLogin_event_integration',
                           queue='staffing_dailyLogin_event',
                           routing_key='staffing.dailylogin')

        channel.basic_consume(queue='staffing_dailyLogin_event',
                              on_message_callback=callback,
                              auto_ack=False)
        channel.start_consuming()


if __name__ == "__main__":
    dirname, filename = os.path.split(os.path.abspath(__file__))
    config_file = os.path.dirname(dirname) + '/conf/default.config'
    app_config = AppConfig.get_app_config(config_file)

    publish_to_queue = PublishToQueue()
    publish_to_queue.publish_data(Client.ZEPTO, Entity.DAILY_LOGIN)
    # publish_to_queue.publish_data(Client.SFX, Entity.SFX_DAILY_LOGIN)
    # publish_to_queue.publish_data(Client.SFX, Entity.ORDER_BASE)
    # publish_to_queue.publish_data(Client.SFX, Entity.SFX_TIPS)
    pass
    # consume_from_daily_login(channel=daily_login_channel)

