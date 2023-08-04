from threading import Thread
from time import sleep

from utils.decorator_with_args import decorator_with_args

class Queuer:
    '''
    Allows you to multithread a function and specify amount of threads to be ran at once

    All calls will be stored and ran when a slot opens up.
    if two calls have equal identifiers the most recent one will be ran.
    identifier is auto generated from the function we are wrapping. can be further specified by a lambda
    '''
    running_threads = {}
    threads_to_run = {}
    unique_id = 0

    def run_function(fun, identifier, max_threads, unique_id, update_threads, xs, kws):
        fun(*xs, **kws)
        Queuer.running_threads[identifier].pop(unique_id)
        update_threads(identifier, max_threads)

    def update_threads(self, identifier, max_threads):
        if Queuer.threads_to_run[identifier]:
            if len(Queuer.running_threads[identifier].keys()) < max_threads:
                key = list(Queuer.threads_to_run[identifier].keys())[0]
                fun = Queuer.threads_to_run[identifier].pop(key)
                Queuer.running_threads[identifier][key] = None
                thread = Thread(target=Queuer.run_function, args=(fun))
                thread.start()

    @decorator_with_args
    def queue(fun, self, max_threads, identifier=None, *args, **kwargs):
        def aux(*xs, **kws):
            ident = str(fun)
            if identifier:
                ident += str(identifier(*xs, **kws))
            unique_id = Queuer.unique_id
            Queuer.unique_id += 1

            if ident not in Queuer.threads_to_run.keys():
                Queuer.threads_to_run[ident] = {}
            Queuer.threads_to_run[ident][unique_id] = [fun, ident, max_threads, unique_id, self.update_threads, xs, kws]
            if ident not in Queuer.running_threads.keys():
                Queuer.running_threads[ident] = {}

            self.update_threads(ident, max_threads)

            return None
        return aux

queue = Queuer().queue
