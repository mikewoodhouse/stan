from datetime import datetime
from time import perf_counter


class StopWatch:
    def __init__(self, msg: str = "", decimals: int = 8, report_every: int = 1000) -> None:
        self.msg = msg
        self.start_time = 0
        self.last_split = 0.0
        self.decimals = decimals
        self.ticks: int = 0
        self.report_every = report_every

    def __enter__(self):
        self.start_time = perf_counter()
        self.last_split = self.start_time
        if len(self.msg):
            print(f"{datetime.now():%H:%M:%S} {self.msg} entered")
        return self

    def __exit__(self, type, value, traceback):
        if self.msg:
            print(f"{datetime.now():%H:%M:%S} {self.formatted(self.elapsed)} {self.msg} exited")

    @property
    def elapsed(self) -> float:
        return perf_counter() - self.start_time

    def formatted(self, secs: float) -> str:
        return f"{secs:.{self.decimals}f}"

    def report_split(self, msg: str = ""):
        time_now = perf_counter()
        split_time = time_now - self.last_split
        self.last_split = time_now
        print(
            f"{datetime.now():%H:%M:%S} split={self.formatted(split_time)}"
            f" total={self.formatted(self.elapsed)} {msg}{f' {str(self.ticks)}' if self.ticks else ''} "
        )

    def tick(self) -> None:
        self.ticks += 1
        if self.ticks % self.report_every == 0:
            self.report_split()
