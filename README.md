# HangPy
HangPy is a simple background job manager for Python.

[![Build, Lint and Test](https://github.com/luizfernandomeier/hangpy/actions/workflows/python-package.yml/badge.svg)](https://github.com/luizfernandomeier/hangpy/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/luizfernandomeier/hangpy/branch/master/graph/badge.svg?token=OPS9QCQ6TQ)](https://codecov.io/gh/luizfernandomeier/hangpy)

Its main purpose is to allow scheduling and distribution of asynchronous tasks.

It is being developed as a study project for Python. Nevertheless, it is completely functional.

# Requirements

- Python 3.9 (it is not tested on older versions)
- Redis

# Usage

In order to use HangPy on your project, it is necessary to install its package using the command below:

```bash
pip install hangpy
```

It is possible to create a standalone application to use as a server, importing both HangPy and the modules containing the tasks that will be scheduled.
Another possibility is to use HangPy on a thread inside an already existing application.

This next code snippet shows a very basic example of the commands necessary in order to start a HangPy server instance:

```python
import hangpy
import redis

# Instantiating a regular Redis client
redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

# Instantiating the server and job repositories
server_repository = hangpy.RedisServerRepository(redis_client)
job_repository = hangpy.RedisJobRepository(redis_client)

# Configuring the HangPy server instance
server_configuration = hangpy.ServerConfigurationDto(slots=10)

# Defining the log output
log_service = hangpy.PrintLogService()

# Instantiating the server
server_service = hangpy.ServerService(server_configuration, server_repository, job_repository, log_service)

# Initializing the server
server_service.start()
```

# Log

There is a builtin log class called `PrintLogService` that can be injected in the `ServerService` constructor. This logger will print the messages on the console. It is possible to build custom loggers inheriting from the abstract class `LogService`.

# Stopping the server

It is possible to use the function `stop` available on the `ServerService` class.

When the HangPy server is signaled to stop, it will wait for the jobs that are running on that instance to end, without fetching any new tasks from the queue.

# Creating jobs

In order to create a job that can be executed by HangPy, it is necessary to create a class that inherits from `JobActivityBase`.

It is necessary to override the function `action`, placing the commands to be executed inside.

The code snippet below shows the scheduling of a simple job.

Suppose that exists a module named `job_delay`, containing the following class:

```python
import hangpy
import time


# Creating a job that does nothing but sleep for 10 seconds
class JobDelay(hanpy.JobActivityBase):

    def action(self):
        time.sleep(10)

```

A simple script to schedule the execution of this job would look something like this next snippet:

```python
import hangpy
import redis
from job_delay import JobDelay

# Instantiating a regular Redis client
redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

# Instantiating the job repository
job_repository = hangpy.RedisJobRepository(redis_client)

# Scheduling the execution of the job
job_service = hangpy.JobService(job_repository)
job_service.enqueue_job(JobPrintDateTime())

```

# Examples

In the `examples` folder there are some scripts that show in a simple way how to use HangPy.

The examples include a simple implementation of a standalone HangPy server that runs on the console.

# Scalability

HangPy was developed to scale. It is possible to run many instances of servers using the same repositories, to allow the distribution of the jobs processing load.

Each server instance can use a different configuration, choosing what best suits the environment.

# Configuration

Using the class `ServerConfigurationDto` is possible to configure the details of each server instance.

- `slots`: Set the maximum number of jobs that can be executed in parallel on each server instance.
- `cycle_interval_milliseconds`: Sets the time the system sleeps between each processing cycle on the server instance. This sleep time only occurs when a cycle ends and there are no jobs enqueued.

# Custom Repositories

HangPy was built in a way to allow that any repository could be used to store its internal data.

Although there is builtin support for using Redis, all calls are made through the abstract classes `JobRepository` and `ServerRepository`.

For example, if someone wants to use HangPy with its internal data stored in a relational database, it would be enough to implement the methods described on those both interfaces, passing these implementations as arguments to the class `ServerService`.
