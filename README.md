# Simple Logger: a logging library for Python

> This project is a Python based logging library that intends to simplify the process of 
> creating logs. To achieve this, the decorator design pattern is used which allows the user
> to add `@` annotation to any function and log its functionality seamlessly. 
> It also contains few additional features such as resource usage monitoring, exception 
> handling, and dynamic type-checking.

## Table Of Contents

* [General Info](#general-info)
* [Features](#features)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Instructions To Run](#instructions-to-run)
* [Code Examples](#code-examples)
* [Performance](#performance)
* [Future Scope](#future-scope)

## General Info

In programming, beginners resort to using print statements to debug their program for finding flow of control, 
inputs taken, and output returned by the function. While this approach is extremely intuitive to use, 
someone who has worked on even slightly complex projects or in collaboration knows how 
frustrating this approach can become in the long term. It always logs to the output console, 
logs have to be manually removed, and doesn't offer any other advantage.

This is the reason every programming language has its own built-in logging library 
that allows for much better debugging and in general, recording of program's behavior. 
Such libraries provide a rich feature set but at the cost of some complexity. 
Also, even this approach does not solve the problem of cluttering your function with logging statements, 
as seen below.

```python
def api(*args, **kwargs):
    # logging logic
    ...
    # business logic
    ...
    # logging logic
    ...
    return
```

In short, we have identified three problems that the aforementioned approaches do not completely solve,
1. Lack of rich feature set (print statements)
2. Added complexity (built-in logging)
3. Violation of Single-Responsibility Principle (both)

The aim of this library is to address some of these problems, and we will take a look into the implementation
details in the upcoming sections.

## Features
1. Logging
    1. FLow of control - Logs when the function is called, when the execution is finished, etc.
       
    2. Resource monitoring - Allows the user to monitor resources when the decorated functions are called. 
       Note that this will only log the resource use and not manage them.
       
2. Exception handling - The user can provide an anonymous function to run as a backup if any exception occurs.
3. Type-checking - Performs type-checking at runtime for function parameters.

## Project Structure

The project consists of the following files and directories:
* `dist` - This contains the final build file of the project. 
  The `.whl` file inside is a compressed file similar to a `.jar` format in java and
  allows us to easily package, distribute, install, and import the library.
  
* `simpleLogger` - This directory contains code files that form the core logic of the library.
    1. `__init__.py` - Necessary to recognize the parent directory as a Python package, 
    and to expose certain classes and functions of the library.
    2. `main.py` - Contains the Log class which will help the user in creating the logs.
    
* `tests` - Various test files (starting with `test_`) for the library. The other files contain:
    1. `logs` - Used to store the logs generated while testing.
    2. `plots` - Used to store the plots from performance testing.
    3. `config.yaml` - A configuration file used by the library and provided by the user.
    4. `__init__.py` - To identify this directory as a Python package while running tests.
    
* `.gitignore` - Files to ignore in git SCM.
* `LICENSE` - MIT license is used for the project.
* `Pipfile` and `Pipfile.lock` - Files generated by the Pipenv library. 
Pipenv is a package and environment management system for Python. It is similar in some ways 
  to Maven, Gradle in Java or sbt in Scala. Pipenv makes it easy to manage packages, separate 
  development and production environment, upgrade packages, notify of any security or incompatibility issues, etc.
  These files will contain the packages required for this project. Pipenv also separates the environment of each project, 
  along with their dependencies.
  
* `README.md` - The current file contains extensive documentation of the project.
* `setup.py` - Contains metadata necessary for Python to create library build files from the project.

## Technologies

The technologies required to develop the project or to set up a development environment for testing are (for developers):
* Programming language
    * [Python 3 programming language](https://www.python.org/) - The project being based on Python.
    
* Package management library
    * [Pipenv](https://pypi.org/project/pipenv/) - To set up a virtual environment and download all required packages.
    If using other tools, please refer to their respective documentation.
    
* Tools
    * [git SCM](https://git-scm.com/) - To clone the repository from Github to a local system.
    
* IDE
    * [Jetbrains Pycharm](https://www.jetbrains.com/pycharm/) - Pycharm is one of the most advanced IDE for Python and highly recommended for Python based projects.
    It makes setting up the project much easier than other IDE's that are generally meant for other programming languages, 
      or do not contain the necessary features.
    
The technologies required to use the library directly in your code are (for users):
* Programming language
    * [Python 3 programming language](https://www.python.org/) - The library being based on Python.


## Instructions To Run
There are two ways to run this project, by running the test cases or directly importing the library in your code.
Both ways are given in detail in the following instructions.

### For Developers
1. Set up the technologies required, given in the previous section.
2. Clone the project into your local system.
3. Open the project in Pycharm, it will ask you to set up a Pipenv virtual environment for the project.
Follow those instructions to complete the set up (First time users may need to provide path to the Pipenv executable 
   downloaded before).
   
4. To run the test cases,
    1. Click on `Run` in the title bar, then `Edit Configurations`.
    2. Click on the `+` sign in the new window on top left, select `pytest`.
    3. In `target`, type 'tests', and finally apply the configuration by clicking OK.
  
5. You should be able to click on the green play button in the top right to run the tests. 
Please refer to their respective documentation if any problem occurs.
   
### For Users
1. Set up the technologies required, given in the previous section.
2. Download the project zip file from Github and unzip in your local repository.
3. In your command prompt, run `pip install /path/to/whl/file/simpleLogger-0.1.0-py3-none-any.whl`.
NOTE: The `.whl` file is in the dist directory of the project.
   
4. Open any IDE and import the library, for example,
    1. `import simpleLogger` OR
    2. `from simpleLogger import Log`
  
5. Use the library by referring the test cases or code examples in the next section.

## Code Examples
The following code demos will give you an idea of how to use the decorator, 
and the library in general.

1. Sample library use
```python
from simpleLogger import Log

# set the configuration file path, can be relative or absolute.
# if not provided, the library will use the default logging style.
# A yaml config file is common in Python, if not familiar, 
# please refer to https://docs.python.org/3/library/logging.config.html
# or use the sample config file provided in the project test cases, 
# or let the library use the defaults (defaults will ignore INFO logs).
Log.set_config_path('config.yaml')

# clean profile is selected from the config file.
@Log(profile='clean') # this is a decorator with arguments
def dummy(x, y):
    """
    Dummy function to test the functionality of the logging decorator.
    :return: Addition of two variables.
    """

    return x + y
```

2. Sample library use with a backup function
```python
from simpleLogger import Log

Log.set_config_path('config.yaml')

@Log(backup_fn=lambda: -1, profile='clean') # anonymous function acts as a backup
def dummy(x, y):
    return x + y
```

3. Sample YAML config file
```yaml
version: 1

# Sample configuration file. Modified from the template provided by https://zetcode.com/python/logging/.

formatters:
  simple:
    format: "[%(levelname)s] - %(message)s"
  extended:
    format: "%(asctime)s (%(name)s) [%(levelname)s] - %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple

  file_handler:
    class: logging.FileHandler
    level: INFO
    filename: tests/logs/test.log
    formatter: extended

loggers:
  clean:
    handlers: [ file_handler ]
    level: INFO
    propagate: false
  detail:
    handlers: [console, file_handler]
    level: INFO
    propagate: false

root:
  handlers: [file_handler]
```

## Performance

Two important observations were made in the performance testing (NOTE: 
set `run_performance_test` to `True` to run them again, but they will be time-consuming).

### Function complexity
The plot shows that as the model complexity increased the percentage difference between with 
and without the library dropped significantly. The Y axis is how much time reduced when running without the library.
Hence, this library is not suitable for calling responsive functions that are relatively simple.

![Complexity impact](https://github.com/yashchitre03/Simple-Logger/blob/main/tests/plots/impact_plot.png)

### Function calls
This plot shows that the library uses constant extra time, and hence, increases linearly 
with the increase in number of function calls. Hence, more function calls means more penalty on the performance 
(even if constant for each call, it will keep adding up).

![Function call impact](https://github.com/yashchitre03/Simple-Logger/blob/main/tests/plots/num_plot.png)

## Future Scope
1. Support for asynchronous code - This library currently will not run well on async code 
and will require modifications.
   
2. Lighter resource use - Code could be improved to run faster and use less resources. 
It needs these modifications to run well on reactive systems such as web microservices.