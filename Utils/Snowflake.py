#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 4:02 下午
import sys
import threading
import time


class SnowFlake:
    datacenter_id_bits = 5
    worker_id_bits = 5
    sequence_id_bits = 12

    worker_id_shift = sequence_id_bits
    datacenter_id_shift = worker_id_bits + sequence_id_bits
    timestamp_left_shift = (datacenter_id_bits +
                            worker_id_bits + sequence_id_bits)

    max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)
    max_worker_id = -1 ^ (-1 << worker_id_bits)
    max_sequence_id = -1 ^ (-1 << sequence_id_bits)

    def __init__(self, datacenter_id, worker_id):
        # 初始时间戳
        self.twepoch = 1480166465631

        if worker_id > SnowFlake.max_worker_id:
            print('worker_id {} 超过最大值，请重新输入 worker_id。'.format(worker_id))
            sys.exit(1)
        self.worker_id = worker_id
        if datacenter_id > SnowFlake.max_datacenter_id:
            print('datacenter_id {} 超过最大值，请重新输入 datacenter_id'.format(datacenter_id))
            sys.exit(1)
        self.datacenter_id = datacenter_id
        self.last_timestamp = -1
        self.sequence_id = 0
        self.lock = threading.Lock()

    def make_snowflake(self):
        """generate a twitter-snowflake id, based on
        https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
        :param: timestamp_ms time since UNIX epoch in milliseconds"""
        while self.lock:
            now = int(time.time() * 1000)
            if now < self.last_timestamp:
                try:
                    raise ValueError(
                        'Clock moved backwards.Refusing to generate id for {} milliseconds.'.format(
                            self.last_timestamp - now)
                    )
                except ValueError:
                    print(sys.exc_info(2))
            if now == self.last_timestamp:
                self.sequence_id = (self.sequence_id + 1) & self.max_sequence_id
                if self.sequence_id == 0:
                    now = self.tail_next_millis(self.last_timestamp)
            else:
                self.sequence_id = 0
            self.last_timestamp = now
            sid = ((now - self.twepoch) << SnowFlake.timestamp_left_shift |
                   self.datacenter_id << SnowFlake.datacenter_id_shift |
                   self.worker_id << SnowFlake.worker_id_shift |
                   self.sequence_id)

            return sid

    def tail_next_millis(self, last_timestamp):
        now = int(time.time() * 1000)
        while now <= last_timestamp:
            now = int(time.time() * 1000)
        return now

    def get_snowflake(self):
        return self.make_snowflake()


if __name__ == '__main__':
    get_id = SnowFlake(1, 1).make_snowflake
    # for i in range(10000):
    print(get_id())
