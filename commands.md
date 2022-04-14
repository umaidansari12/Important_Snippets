# Selenium Utils 
* ## download_dir
```
preferences = {"profile.default_content_setting_values.automatic_downloads": 1,
               'download.default_directory': self.default_download_dir}
chrome_options.add_experimental_option("prefs", preferences)

```

* ## when you have to run in server (no GUI) or in docker
```
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
```

* ## chrome and compatible driver download and install
```
# Install Google Chrome driver
CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
```

* ## using a time.sleep() in selenium to get an element is a quick fix but prone to errors.
    * ### added a method which can do this in fault tolerant way, when action fetch is passed, it will fetch the element

```
def act_on_element_if_exists(driver, xpath, parent_element="", action="click", retry_interval=2,
                             timeout_in_secs=120,
                             refresh_after_error=False, max_retry_limit=30):
```

* ## Advantage of webdriver click vs javascript executor click
 [Link] (https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click)

* ## XPaths Helper
```
contains --> //*[contains(@class,'icon--caret-down')]

not contains --> //div[not(contains(@style,'display:none'))]//button[.='OK']
//*[@class='class_name'] 

for export_csv_item in self.driver.find_elements_by_xpath("//*[@title='Export as CSV']"):
    export_csv_item.click()
//*[@class='mc-modal__action btn btn--success']

drilldown : "//DIV[@id='export']//BUTTON"

contains text --> //*[contains(text(),'ABC')]


//ul[@class='nav navbar-nav navbar__menu--top']//li[@class='dropdown']
//ul[contains(@class,'navbar-nav')]
//ul[not(contains(@class,'navbar-nav'))]
//*[@id='hostsLinks']
//*[@class='headline-highlight'][contains(text(),'impressions')]

child to parent to child --> //div[contains(text(),'Daily Login')]/parent::div//div[@class='controls']//div[@name='expand']

//div[contains(text(),'Daily Login')]/parent::div//div[@class='controls']//div[@name='expand']//div[@name='csv']


```

* ## Selenium Utilities
```
from logging.handlers import TimedRotatingFileHandler

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from conf.app_properties import ApplicationProperties as props
import logging
import os
import datetime
import time
import uuid

logs_dir = props.logs_dir


# logging setup start
def create_dir_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)


create_dir_if_not_exists(logs_dir)

logger = logging.getLogger("SalesforceUploader")
logger.setLevel(logging.DEBUG)

logname = os.path.join(logs_dir, "salesforce.log")
rotation_handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
rotation_handler.suffix = "%Y-%m-%d"
rotation_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s")
rotation_handler.setFormatter(formatter)
logger.addHandler(rotation_handler)


# logging setup finished

class Utils:

    @staticmethod
    def redirect(driver, url, url_after_redirect='', timeout_in_secs=180, retry_interval=5):
        if '' == url_after_redirect:
            url_after_redirect = url
        start_time = Utils.get_current_time_in_millis()
        finish_time = start_time + timeout_in_secs * 1000
        retry_counter = 0
        while start_time <= finish_time:
            retry_counter += 1
            try:
                start_time = Utils.get_current_time_in_millis()
                if driver.current_url != url_after_redirect:
                    logger.info("opening url " + url + " , Attempt : " + str(retry_counter))
                    driver.get(url)
                    time.sleep(retry_interval)
                else:
                    break
            except:
                logger.error("get url failed : " + url + " , Attempt : " + str(retry_counter))
                logger.exception('')
                time.sleep(retry_interval)

        if Utils.get_current_time_in_millis() > finish_time:
            raise Exception("Timeout error on url : " + url)

    @staticmethod
    def act_on_element_if_exists(driver, xpath, parent_element="", action="click", retry_interval=2,
                                 timeout_in_secs=120,
                                 refresh_after_error=False, max_retry_limit=30):
        start_time = Utils.get_current_time_in_millis()
        finish_time = start_time + timeout_in_secs * 1000
        retry_counter = 0

        while start_time <= finish_time and retry_counter < max_retry_limit:
            retry_counter += 1
            try:
                start_time = Utils.get_current_time_in_millis()
                logger.info("fetching element with xpath : " + xpath + " , Attempt : " + str(retry_counter))

                if "click" == action:
                    if "" == parent_element:
                        driver.execute_script("arguments[0].scrollIntoView();",
                                              driver.find_element_by_xpath(xpath))
                        driver.find_element_by_xpath(xpath).click()
                    else:
                        driver.execute_script("arguments[0].scrollIntoView();",
                                              parent_element.find_element_by_xpath(xpath))
                        parent_element.find_element_by_xpath(xpath).click()
                    break
                elif "fetch" == action:
                    if "" == parent_element:
                        return driver.find_element_by_xpath(xpath)
                    else:
                        return parent_element.find_element_by_xpath(xpath)
                elif "fetch_list" == action:
                    if "" == parent_element:
                        return driver.find_elements_by_xpath(xpath)
                    else:
                        return parent_element.find_elements_by_xpath(xpath)
                else:
                    logger.error("unknown action : " + action + ", on xpath : " + xpath)
                    break
            except:
                logger.error("Xpath fetch failed : " + xpath + " , Attempt : " + str(retry_counter))
                if retry_counter > 2:
                    print()
                logger.exception('')
                time.sleep(retry_interval)
                if refresh_after_error:
                    driver.refresh()

        if Utils.get_current_time_in_millis() > finish_time or retry_counter >= max_retry_limit:
            message = "Timeout error or max retrial limit reached on xpath : " + xpath + ", action : " + action
            logger.error(message)
            raise Exception(message)

    @staticmethod
    def get_current_time_in_millis():
        return int(round(time.time() * 1000))

    @staticmethod
    def get_path_of_new_file(files_in_download_dir_before_download, files_in_download_dir_after_download,
                             download_dir):
        diff = list(set(files_in_download_dir_after_download) - set(files_in_download_dir_before_download))
        if len(diff) > 1:
            message = "Fatal error, file got downloaded after timeout, files : " + str(diff)
            logger.error(message)

        if len(diff) == 1:
            file_name = diff[0]
            return (file_name, os.path.join(download_dir, file_name))

        logger.info("no new files found, returning empty")
        return ""

    @staticmethod
    def delete_if_file_exists(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def retry(function_to_retry, function_to_check_status, max_retry=3, retry_interval_in_secs=15,
              first_retry_then_check=True):
        if not first_retry_then_check:
            time.sleep(5)
        retry_attempt = 0
        status_success = False

        while retry_attempt < (max_retry - 1) and not status_success:
            retry_attempt += 1
            if retry_attempt > 1:
                logger.info("Retrial attempt : " + str(retry_attempt))
            else:
                logger.info("Execution attempt : " + str(retry_attempt))
            try:
                if first_retry_then_check:
                    function_to_retry()
                    status_success = function_to_check_status()
                else:
                    status_success = function_to_check_status()
                    if not status_success: function_to_retry()
            except:
                logger.exception('')
                logger.error("Exception occured in retrial attempt : " + str(retry_attempt))
            if not status_success:
                time.sleep(retry_interval_in_secs)

        if retry_attempt >= (max_retry - 1):
            logger.info("Retrial attempt : " + str(retry_attempt))
            function_to_retry()

        return function_to_check_status()

    @staticmethod
    def does_element_with_xpath_exists(driver, xpath, parent_element = "",
                                       max_retry=5, timeout_in_secs=10, retry_interval=2,
                                       refresh_after_error=False):
        start_time = Utils.get_current_time_in_millis()
        finish_time = start_time + timeout_in_secs * 1000
        retry_counter = 0

        while start_time <= finish_time and retry_counter < max_retry:
            retry_counter += 1
            try:
                start_time = Utils.get_current_time_in_millis()
                logger.info("fetching element with xpath : " + xpath + " , Attempt : " + str(retry_counter))
                if "" == parent_element:
                    driver.find_element_by_xpath(xpath)
                else:
                    parent_element.find_element_by_xpath(xpath)
                return True
            except:
                logger.error("Xpath fetch failed : " + xpath + " , Attempt : " + str(retry_counter))
                logger.exception('')
                time.sleep(retry_interval)
                if refresh_after_error:
                    driver.refresh()
        return False

    @staticmethod
    def wait_for_file_download(prev_count_of_files, watch_dir, retry_interval=2, timeout_in_secs=60):
        start_time = Utils.get_current_time_in_millis()
        finish_time = start_time + timeout_in_secs * 1000

        while start_time <= finish_time and len(os.listdir(watch_dir)) <= prev_count_of_files:
            time.sleep(retry_interval)
            start_time = Utils.get_current_time_in_millis()

        if len(os.listdir(watch_dir)) <= prev_count_of_files and Utils.get_current_time_in_millis() > finish_time:
            logger.error("File didn't download after a wait of " + str(timeout_in_secs) + " sec")

    @staticmethod
    def refactor_column_names(df):
        df.columns = df.columns.str.strip() \
            .str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        return df

    @staticmethod
    def wait_for_tmp_files_to_be_removed_and_get_files(directory_path, max_wait_secs=60,
                                                       check_interval=1, tmp_file_formats=["crdownload"]):

        start_time = Utils.get_current_time_in_millis()
        finish_time = start_time + max_wait_secs * 1000

        time.sleep(check_interval)
        while start_time <= finish_time:
            list_of_files = os.listdir(directory_path)

            if Utils.does_tmp_file_exists(list_of_files, tmp_file_formats):
                logger.info('temporary files exist after a waiting for secs : ' + str(check_interval))
                time.sleep(check_interval)
            else:
                return os.listdir(directory_path)

            start_time = Utils.get_current_time_in_millis()

        logger.error('temporary files exist after a waiting for secs : ' + str(max_wait_secs))
        return os.listdir(directory_path)


    @staticmethod
    def does_tmp_file_exists(list_of_files, tmp_file_formats):
        for file_name in list_of_files:
            for tmp_file_format in tmp_file_formats:
                if file_name.endswith(tmp_file_format):
                    return True
        return False
```



# Tips to manage Config file 

* scope of optimization, learn to optimize configurations, only put the things which are necessary as external output
infer what can be inferred, if something is not going to change you can hard code in variable
This is the config you added

* Example : Original -> modified
```
# Original
{
  "output_download_dir": "/home/umaid/Vahan_Codes/data-scratchpad/periscope/Staffing Data Output",
  "default_download_dir": "/home/umaid/Downloads",
  "logs_dir": "/home/umaid/Vahan_Codes/data-scratchpad/periscope/Staffing Logs",
  "logs_name": "Staffing Data Download",
  "logs_file_name": "staffing_data_download.log",
  "preferences": {
    "profile.default_content_setting_values.automatic_downloads": 1
  },
  "credentials": {
    "url": "https://app.periscopedata.com/shared/a2ed0a8e-2083-4e7f-90d5-399b3d270cef",
    "password": "Vahan01"
  },
  "mapping": {
    "widget_names": [
      "Daily Login",
      "Onboarding Base",
      "order_base"
    ],
    "file_names": [
      "daily_login",
      "onboarding_base",
      "order_base"
    ]
  },
  "webdriver_path": "/home/umaid/.local/bin/ChromeDriver/chromedriver_linux64/chromedriver"
}
```
```
# Modified
{
  "login_url" : "https://app.periscopedata.com/shared/a2ed0a8e-2083-4e7f-90d5-399b3d270cef",
  "password" : "Vahan01",
  "entity_and_widgets" : {
    "daily_login" : "Daily Login",
    "onboarding_base" : "Onboarding Base",
    "order_base" : "order_base",
    "tips" : ""
  }
} 
```

* # File Name Replacements
```
out_file_name = file_name.replace("Orderbase", "order_base")
out_file_name = out_file_name.replace("orderbaseeditted", "order_base")
out_file_name = out_file_name.replace("order_baseD3", "order_base")
out_file_name = file_name.replace("OnboardingBase", "onboarding_base")
out_file_name = file_name.replace("DailyLoginHrsBasefile", "daily_login")
``` 

* # Google Sheets Utils
* ### Read Google Sheets
[Google Sheet Reader] (https://towardsdatascience.com/read-data-from-google-sheets-into-pandas-without-the-google-sheets-api-5c468536550)
    
* ### Import Google Sheets into Pandas Dataframe
[Google Sheets to Pandas DataFrame] (https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530)

* ### Generate Service Account
[Service Account] (https://docs.google.com/document/d/1L3IugVkThz9sxuMxNtwC1dx5ZmkYGOhijiitbYl9yFM/edit)


* # Conda
* ### Create an environment in conda 
```
conda create -n staffing310 python=3.10
```

* # Safe Executor (used to generalise try catch for a function call)

```
def safe_execute(func, log_exception=True, **kwargs):
    '''
    :param func: any executable function
    :param kwargs: function parameters
    :return: exception_message(str), func's response
    '''
    exception_msg = None
    response = None
    try:
        response = func(**kwargs) if kwargs else func()
    except Exception as e:
        if log_exception:
            log.exception(e)
        exception_msg = str(e)
    return exception_msg, response
```
* # RabbitMQ
* ### connect with RabbitMQ
```

def create_channel(self, exchange_name):
    credentials = pika.PlainCredentials(self.app_config.get_rabbitmq_connection_config('username'),
                                        self.app_config.get_rabbitmq_connection_config('password'))
    parameters = pika.ConnectionParameters(self.app_config.get_rabbitmq_connection_config('hostname'),
                                           int(self.app_config.get_rabbitmq_connection_config('port')),
                                           self.app_config.get_rabbitmq_connection_config('virtual_host'),
                                           credentials, heartbeat=600)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type=self.app_config.get_staffing_rabbitmq_config('exchange_type'),
                             durable=bool(self.app_config.get_staffing_rabbitmq_config('exchange_durable')))
    # channel.confirm_delivery()
    return channel
```



* # SQL Important 
* ### Working with Date objects
```
SELECT to_date(split_part('3/23/2022 13:49:06', ' ',1), 'MM/DD/YYYY') ;

SELECT split_part('3/23/2022 13:49:06', ' ',1);

SELECT to_timestamp('12/28/2021 8:35:15', 'MM-DD-YYYY HH24:MI:SS') ;

CASE WHEN to_timestamp(CONCAT(order_date, ' ', SUBSTRING(order_time, 1, 2), ':00:00'), 'YYYY-MM-DD HH24:MI:SS') > '1990-01-01' THEN to_timestamp(CONCAT(order_date, ' ', SUBSTRING(order_time, 1, 2), ':00:00'), 'YYYY-MM-DD HH24:MI:SS') ELSE NULL END

SELECT to_date(split_part('3/23/2022 13:49:06', ' ',1), 'MM/DD/YYYY') ;
SELECT to_date(split_part('3/23/2022', ' ',1), 'MM/DD/YYYY') ;
```