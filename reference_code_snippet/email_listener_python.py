import datetime
import os
import re
import sys
import time

import pandas as pd
from iso8601 import iso8601

import logger
import util as util
from app_config import AppConfig, Client, Entity
from email_data_downloader import EmailDataDownloader
from notify import Notify

NOTIFY_PROCESSING_SUCCESS = 'rapido_data_download_success'
NOTIFY_PROCESSING_FAILURE = 'rapido_data_download_failure'

log = logger.get_logger('RapidoDataDownloader')

RAPIDO_MAIL_SENDERS = ["data_support@vahan.co"]


class RapidoDataDownloader:
    _kill_signal_received = False
    _processing = False

    def __init__(self, out_dir, config_file_path=None):
        self.out_dir = out_dir
        if config_file_path:
            self.app_config = AppConfig.get_app_config(config_file_path)
        else:
            self.app_config = AppConfig.get_app_config()

        self.attachment_dir = self.app_config.get_client_email_attachment_dir(Client.RAPIDO.value)
        util.create_dir_if_not_exists(self.out_dir)
        util.create_dir_if_not_exists(self.attachment_dir)
        self.notify = Notify()

    def get_email_data_downloader(self):
        email_account_name = self.app_config.get_mailgun_connection_config(param='email_account_name')
        email_account_pass = self.app_config.get_mailgun_connection_config(param='email_account_pass')
        email_data_downloader = EmailDataDownloader(email_add=email_account_name, email_pass=email_account_pass,
                                                    attachment_dir=self.attachment_dir)
        return email_data_downloader

    def get_rapido_messages(self, messages):
        rapido_messages = []
        for sender, message_info in messages.items():
            for rapido_mail_sender in RAPIDO_MAIL_SENDERS:
                if rapido_mail_sender in RAPIDO_MAIL_SENDERS:
                    rapido_messages.append(message_info)
        return rapido_messages

    def download_data(self):
        processing_exception = None
        notifications = None
        try:
            email_data_downloader = self.get_email_data_downloader()
            email_data_downloader.login()
            messages = self.get_rapido_messages(email_data_downloader.poll_messages())
            log.info(f"Email messages : {messages}")
            if not messages:
                return
            email_data_downloader.logout()

            # transform
            notifications = self.transform_and_write_data(messages)
        except Exception as e:
            log.exception(e)
            processing_exception = str(e)

        # notify
        notify_payload = {}
        if not processing_exception:
            for notification_info in notifications:
                notify_payload["entity"] = notification_info["entity"] if "entity" in notification_info else None
                notify_payload["day_window"] = notification_info[
                    "day_window"] if "day_window" in notification_info else None
                notify_payload["file_name"] = notification_info[
                    "file_name"] if "file_name" in notification_info else None
                notify_payload["row_count"] = notification_info[
                    "row_count"] if "row_count" in notification_info else None
                self.notify.send(NOTIFY_PROCESSING_SUCCESS, notify_payload)
        else:
            notify_payload["processing_exception"] = processing_exception
            self.notify.send(NOTIFY_PROCESSING_FAILURE, notify_payload)

    def scheduled_run(self):
        while True:
            for cron in self.app_config.get_rapido_scheduled_crons():
                if not util.is_cron_valid(cron):
                    log.exception(f'Invalid cron expression : {cron}')
                    continue
                if util.is_cron_expression_in_next_x_secs(cron, secs_threshold=60):
                    self.start_processing()
            log.debug("Cron checker executed")
            time.sleep(60)

    def start_processing(self):
        log.debug("Executing rapido data download")
        self.download_data()
        log.debug("Executed rapido data download")

    @staticmethod
    def shutdown():
        log.debug("gracefully shutting down RapidoDataDownloader")
        RapidoDataDownloader._kill_signal_received = True
        log.debug("RapidoDataDownloader is shutdown")

    def _get_todays_date(self):
        '''
        :return: end date is today's date in YYYY-MM-DD format
        '''
        return datetime.date.today().strftime('%Y-%m-%d')

    def _get_yesterdays_date(self):
        '''
        :return: end date is today's date in YYYY-MM-DD format
        '''

        return (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def transform_and_write_data(self, messages):
        def get_day_window_and_date_from_email_subject(subject):
            '''
                returns day's window form email subject
            '''
            subject_fil = re.sub('[^a-zA-Z0-9]', '', subject.lower()).lower()
            if "5am" in subject_fil:
                return Entity.DAILY_LOGIN.value, self._get_yesterdays_date(), 0
            elif "12am8am" in subject_fil:
                return "12AM-8AM", self._get_todays_date(), 1
            elif "8am11am" in subject_fil:
                return "8AM-11AM", self._get_todays_date(), 2
            elif "11am5pm" in subject_fil:
                return "11AM-5PM", self._get_todays_date(), 3
            elif "5pm9pm" in subject_fil:
                return "5PM-9PM", self._get_todays_date(), 4
            elif "9pm12am" in subject_fil:
                return "9PM-12AM", self._get_yesterdays_date(), 5
            else:
                raise Exception(f"Unknown slot in email: {subject}")

        notifications = []
        for message in messages:
            subject = message["Subject"]
            day_window, file_date, file_index = get_day_window_and_date_from_email_subject(subject)
            for attachment_file in message['attachments']:
                if not os.path.exists(attachment_file):
                    continue
                attachment_df = pd.read_csv(attachment_file, dtype=str, keep_default_na=False)
                attachment_df["day_window"] = day_window
                if day_window == Entity.DAILY_LOGIN.value:
                    out_file_name = os.path.join(self.out_dir,
                                                 f"{Entity.DAILY_LOGIN.value}_{file_date}_{file_index}.csv")
                # else:
                #     out_file_name = os.path.join(self.out_dir,
                #                                  f"{Entity.DAILY_SLOT_INFO.value}_{file_date}_{file_index}.csv")

                # parse iso8601 datetime
                attachment_df["report_time"] = attachment_df["report_time"].apply(
                    lambda val: iso8601.parse_date(val).strftime('%Y-%m-%d %H:%M:%S'))
                attachment_df["ols_date"] = attachment_df["report_time"].apply(
                    lambda val: iso8601.parse_date(val).strftime('%Y-%m-%d %H:%M:%S'))
                if day_window == Entity.DAILY_LOGIN.value:
                    attachment_df.to_csv(out_file_name, index=False)
                os.remove(attachment_file)
                if day_window == Entity.DAILY_LOGIN.value:
                    notify_info = {
                        "entity": Entity.DAILY_LOGIN.value if day_window == Entity.DAILY_LOGIN.value else Entity.DAILY_SLOT_INFO.value,
                        "day_window": day_window, "file_name": os.path.basename(out_file_name),
                        "row_count": len(attachment_df)}
                    notifications.append(notify_info)
        return notifications


if __name__ == '__main__':
    config_file_path = sys.argv[1] if len(sys.argv) > 1 else os.environ[
        'STAFFING_CONFIG'] if 'STAFFING_CONFIG' in os.environ else None
    os.environ["PGTZ"] = "Asia/Kolkata"
    os.environ["TZ"] = "Asia/Kolkata"

    log.info(f"ENV var STAFFING_CONFIG:{config_file_path}")
    data_dir = None
    if not config_file_path:
        dirname, filename = os.path.split(os.path.abspath(__file__))
        config_file_path = os.path.dirname(os.path.dirname(dirname)) + '/conf/default.config'

    os.environ['STAFFING_CONFIG'] = config_file_path

    data_dir = os.path.join(os.path.dirname(os.path.dirname(config_file_path)), "data", "rapido3pl", "in")

    # init Uploader and app_config module
    processor = RapidoDataDownloader(config_file_path=config_file_path, out_dir=data_dir)
    # processor.scheduled_run()
    processor.download_data()

