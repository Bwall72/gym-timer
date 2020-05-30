from threading import Thread
from datetime import timedelta
from tkinter import StringVar
from strings_en import Strings
from copy import deepcopy
import time


def timedelta_str(td: timedelta):
    return ":".join(map(lambda s: s[:4], str(td).split(":")))


class Timer:
    def __init__(
        self,
        timer_length: timedelta,
        print_prefix: str = "",
        tk_string_var: StringVar = None,
    ):
        self.clock = 0
        self.kill = False
        # backup to allow restarting timer
        self.__backup_length = deepcopy(timer_length)
        self.timer_thread: Thread = None
        self.print_prefix = print_prefix
        # used to implement the timer
        self.time_remaining = deepcopy(timer_length)
        self.prefix = print_prefix
        self.running = False
        self.finished = False
        self.string_var = tk_string_var

    def pause(self) -> timedelta:
        if not self.timer_thread:
            return timedelta(seconds=0)
        self.kill = True
        self.timer_thread.join()
        self.timer_thread = None
        self.running = False
        self.finished = False
        return self.time_remaining

    def resume(self) -> None:
        self.kill = False
        self.start()

    def output_timer(self) -> None:
        if self.string_var is not None:
            self.string_var.set(
                f"{self.prefix}{timedelta_str(self.time_remaining)}")
        print(f"{self.prefix}{timedelta_str(self.time_remaining)}", end="\r")

    def reset_output(self) -> None:
        if self.string_var is not None:
            self.string_var.set(Strings.timer_text)
        print("00:00:00.0", end="\r")

    def start(self) -> None:
        # Fork a process to start the timer
        def __run_timer(self) -> None:
            last_tick = time.monotonic()
            self.running = True
            while not self.kill:
                if self.time_remaining.total_seconds() <= 0:
                    self.reset_output()
                    self.running = False
                    self.finished = True
                    return
                current = time.monotonic()
                delta = current - last_tick
                self.time_remaining -= timedelta(seconds=delta)
                last_tick = current
                self.output_timer()
            self.running = False

        self.timer_thread = Thread(target=__run_timer, args=(self,))
        self.timer_thread.start()

    def restart(self):
        if self.timer_thread is not None:
            self.kill = True
            self.timer_thread.join()
            self.kill = False
        self.time_remaining = deepcopy(self.__backup_length)
        self.running = False
        self.finished = False

    def join(self):
        if not self.timer_thread:
            return
        self.timer_thread.join()


class EmomTimer(Timer):
    def __init__(self, rounds: int, round_lengths: [timedelta]):
        self.timers = []
        for round in range(rounds):
            for round_length in round_lengths:
                self.timers.append(
                    Timer(round_length,
                          print_prefix=f"Round {round+1}/{rounds}:")
                )

    def restart(self):
        for timer in self.timers:
            timer.restart()

    def start(self):
        for timer in self.timers:
            timer.start()
            timer.join()


if __name__ == '__main__':
    t = Timer(timedelta(seconds=10))
    t.start()
    time.sleep(1)
    t.pause()
    time.sleep(1)
    t.resume()
    input()
    t.join()
