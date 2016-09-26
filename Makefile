# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]

# test your application (tests in the tests/ directory)
test: redis_test unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

focus:
	@`which nosetests` -vv --with-yanc --with-focus -i -s tests/

# show coverage in html format
coverage-html: unit
	@coverage html

# run tests against all supported python versions
tox:
	@tox

#docs:
	#@cd smart_sentinel/docs && make html && open _build/html/index.html

# kill the test redis instance (localhost:57575, 57576, 57577, 57574, 57573)
kill_redis_test:
	-redis-cli -p 57575 shutdown
	-redis-cli -p 57576 shutdown
	-redis-cli -p 57577 shutdown
	-redis-cli -p 57574 shutdown
	-redis-cli -p 57573 shutdown

conf-redis-sentinel:
	cp redis-conf/redis_sentinel.conf.template redis-conf/redis_sentinel.conf
	cp redis-conf/redis_sentinel2.conf.template redis-conf/redis_sentinel2.conf

# get a redis instance up for your unit tests (localhost:4448)
redis_test: kill_redis_test conf-redis-sentinel
	redis-sentinel ./redis-conf/redis_sentinel.conf --daemonize yes; sleep 1
	redis-sentinel ./redis-conf/redis_sentinel2.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test2.conf --daemonize yes; sleep 1
	redis-server ./redis-conf/redis_test3.conf --daemonize yes; sleep 1
	redis-cli -p 57574 info > /dev/null
