###############################################################################
# This file holds the implementations for all the API clients.
#
# If you want to develop a new client, here are some suggestions: Get the fetch
# methods working first, then the push, then the liquidsoap notifier.  You will
# probably want to create a script on your server side to automatically
# schedule a playlist one minute from the current time.
###############################################################################
import logging
import sys
from datetime import datetime, timedelta

from configobj import ConfigObj
from dateutil.parser import isoparse

from .utils import RequestProvider, fromisoformat, time_in_milliseconds, time_in_seconds

LIBRETIME_API_VERSION = "2.0"

api_config = {}
api_endpoints = {}

api_endpoints["version_url"] = "version/"
api_endpoints["schedule_url"] = "schedule/"
api_endpoints["webstream_url"] = "webstreams/{id}/"
api_endpoints["show_instance_url"] = "show-instances/{id}/"
api_endpoints["show_url"] = "shows/{id}/"
api_endpoints["file_url"] = "files/{id}/"
api_endpoints["file_download_url"] = "files/{id}/download/"
api_config["api_base"] = "api/v2"


class AirtimeApiClient:
    def __init__(self, logger=None, config_path="/etc/airtime/airtime.conf"):
        if logger is None:
            self.logger = logging
        else:
            self.logger = logger

        try:
            self.config = ConfigObj(config_path)
            self.config.update(api_config)
            self.services = RequestProvider(self.config, api_endpoints)
        except Exception as e:
            self.logger.exception("Error loading config file: %s", config_path)
            sys.exit(1)

    def get_schedule(self):
        current_time = datetime.utcnow()
        end_time = current_time + timedelta(days=1)

        str_current = current_time.isoformat(timespec="seconds")
        str_end = end_time.isoformat(timespec="seconds")
        data = self.services.schedule_url(
            params={
                "ends__range": (f"{str_current}Z,{str_end}Z"),
                "is_valid": True,
                "playout_status__gt": 0,
            }
        )
        result = {}
        for item in data:
            start = isoparse(item["starts"])
            start_key = start.strftime("%Y-%m-%d-%H-%M-%S")
            end = isoparse(item["ends"])
            end_key = end.strftime("%Y-%m-%d-%H-%M-%S")

            show_instance = self.services.show_instance_url(id=item["instance_id"])
            show = self.services.show_url(id=show_instance["show_id"])

            result[start_key] = {
                "start": start_key,
                "end": end_key,
                "row_id": item["id"],
                "show_name": show["name"],
            }
            current = result[start_key]
            if item["file"]:
                current["independent_event"] = False
                current["type"] = "file"
                current["id"] = item["file_id"]

                fade_in = time_in_milliseconds(fromisoformat(item["fade_in"]))
                fade_out = time_in_milliseconds(fromisoformat(item["fade_out"]))

                cue_in = time_in_seconds(fromisoformat(item["cue_in"]))
                cue_out = time_in_seconds(fromisoformat(item["cue_out"]))

                current["fade_in"] = fade_in
                current["fade_out"] = fade_out
                current["cue_in"] = cue_in
                current["cue_out"] = cue_out

                info = self.services.file_url(id=item["file_id"])
                current["metadata"] = info
                current["uri"] = item["file"]
                current["replay_gain"] = info["replay_gain"]
                current["filesize"] = info["filesize"]
            elif item["stream"]:
                current["independent_event"] = True
                current["id"] = item["stream_id"]
                info = self.services.webstream_url(id=item["stream_id"])
                current["uri"] = info["url"]
                current["type"] = "stream_buffer_start"
                # Stream events are instantaneous
                current["end"] = current["start"]

                result[f"{start_key}_0"] = {
                    "id": current["id"],
                    "type": "stream_output_start",
                    "start": current["start"],
                    "end": current["start"],
                    "uri": current["uri"],
                    "row_id": current["row_id"],
                    "independent_event": current["independent_event"],
                }

                result[end_key] = {
                    "type": "stream_buffer_end",
                    "start": current["end"],
                    "end": current["end"],
                    "uri": current["uri"],
                    "row_id": current["row_id"],
                    "independent_event": current["independent_event"],
                }

                result[f"{end_key}_0"] = {
                    "type": "stream_output_end",
                    "start": current["end"],
                    "end": current["end"],
                    "uri": current["uri"],
                    "row_id": current["row_id"],
                    "independent_event": current["independent_event"],
                }

        return {"media": result}

    def update_file(self, file_id, payload):
        data = self.services.file_url(id=file_id)
        data.update(payload)
        return self.services.file_url(id=file_id, _put_data=data)
