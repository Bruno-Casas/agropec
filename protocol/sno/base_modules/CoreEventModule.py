from sno.base_modules.AsyncModule import AsyncModule

class CoreEventModule(AsyncModule):

    def call_event(self, name: str):
        record = self._event_record[name]
        fn = record[1]
        fn()
