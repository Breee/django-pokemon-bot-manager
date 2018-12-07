import base64

from google.protobuf import text_format
from idna import unicode

from pogoprotos.networking.responses import get_map_objects_response_pb2, fort_search_response_pb2
from pogoprotos.networking.responses import encounter_response_pb2
from pogoprotos.networking.responses import fort_details_response_pb2
from pogoprotos.networking.responses import gym_get_info_response_pb2
from pogoprotos.networking.responses import disk_encounter_response_pb2


class Pogoprotos:
    messages = {}

    def parse(self, protos: dict, base64_encoded: bool = True):
        for key, value in protos.items():
            if key == 'GetMapObjects':
                message = get_map_objects_response_pb2.GetMapObjectsResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            elif key == 'EncounterResponse':
                message = encounter_response_pb2.EncounterResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            elif key == 'FortDetailsResponse':
                message = fort_details_response_pb2.FortDetailsResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            elif key == 'GymGetInfoResponse':
                message = gym_get_info_response_pb2.GymGetInfoResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            elif key == 'DiskEncounterMessage':
                message = disk_encounter_response_pb2.DiskEncounterResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            elif key == 'FortSearchResponse':
                message = fort_search_response_pb2.FortSearchResponse()
                message.ParseFromString(self._get_message_data(value, base64_encoded))
            else:
                raise NotImplementedError(' '.join(['progoprotos:', str(key), str(value)]))

            if message is not None:
                self.messages[key] = message

    @staticmethod
    def _get_message_data(message, base64_encoded: bool):
        if base64_encoded:
            message = base64.b64decode(message)
        return message

    def __str__(self):
        messages_str = []
        for key, message in self.messages.items():
            messages_str.append(text_format.MessageToString(message))
        return " ".join(messages_str)
