import json

from display import Display


class ResponseHandler:
    def __init__(self):
        self.display = Display()

    def handle_response(self, response):
        try:
            print(response)
            response_json = json.loads(response.replace("\'", "\""))
            if response_json["shiftStatus"] == 0:
                self.display.show_checked_in()
            elif response_json["shiftStatus"] == 1:
                self.display.show_checked_out()
            else:
                self.display.show_error()
        except Exception as e:
            print(f'Error: {e}')
            self.display.show_error()

    def show_loading(self):
        self.display.show_loading()
