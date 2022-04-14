# Coding Tips
* add requirements.txt / package.json which contains all the dependencies that are required to run the program (requirements.txt will have only the library names in separate line)
so that all the libraries can be installed using 

    ```pip install -r requirements.txt```

example
```pika
psycopg2-binary
iso8601
requests
jinja2
schedule
swifter==1.1.2
pandas==1.4.1
flask
```
* separate code and configs
* break everything into smaller units that are easier to debug
* use debugger frequently , instead of print statement
* make function definition meaningful and pass only the necessary arguments that are required to run the function and do not take any extra parameter in function definition
* maintain doc for everything you are doing so that you don't need to tell everyone what you've done instead handover them the doc
* To make the other person understand your statement in a better way don't overload them with so much of information
* Try to give a gist of everything
* Plan your day with To-Dos
* use lower case in file names, separate using _
* remove everything from main call - dont call most of the things from main
* For selenium - create utils for fetch and click - (generalised function ) (most of the common things which we need later and is common)
create a utils.py file and create reusable functions inside it, eg:
open_url(url)
click(xpath)
* dont use try catch iinstead generalise it for every function call
* use relative xpaths and not absolute paths
* add logger (passing logger to a function is not good practice, like it's added in the periscope auto download , create a separate logger for every class)
* When you are coding, focus on
    * code readability
    * using more configurations (configuration example in your case is periscope UI, pass, mappings of widgets,
say tomorrow values of these changes, this shouldn't result in code changes as well but configuration changes)
    * creating functions for any piece of code you need to write twice or to increase readability
    * for hard coded values
        * declare variables
* 
