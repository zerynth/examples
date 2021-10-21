class StatVar:
    def __init__(self):
        self.cnt = 0
        self.avg = 0
        self.min = 0
        self.max = 0
        self.last = 0

    def add(self, v):
        self.cnt += 1
        self.last = v
        self.avg += (v-self.avg)/self.cnt

        if self.cnt == 1:
            self.min = v
            self.max = v
        else:
            if v < self.min:
                self.min = v
            elif v > self.max:
                self.max = v

    def get(self):
        avg, min, max = self.avg, self.min, self.max
        self.cnt, self.avg, self.min, self.max  = 0, 0, 0, 0

        return avg*1.0, min*1.0, max*1.0


def get_publish_ts(now, publish_period, ts_last_publish, offset=0):
    publish_ts = False

    delta = now%publish_period
    if delta < offset:
        delta += publish_period

    if (ts_last_publish < now-delta + offset) :
        publish_ts = now - delta + offset
        # if publish_ts != now:
        #     print("send2 dirty")
        # else:
        #     print("send2 clean")
    return publish_ts
