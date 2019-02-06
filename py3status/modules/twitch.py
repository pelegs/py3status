# -*- coding: utf-8 -*-
"""
Display status on a given Twitch streamer.

Checks if a streamer is online using the Twitch Kraken API to see
if a channel is currently streaming or not.

Configuration parameters:
    cache_timeout: how often we refresh this module in seconds
        (default 60)
    client_id: Your client id. Create your own key at https://dev.twitch.tv
        (default None)
    format: Display format when online
        (default "{stream_name} is live!")
    format_offline: Display format when offline
        (default "{stream_name} is offline.")
    stream_name: name of streamer(twitch.tv/<stream_name>)
        (default None)

Format placeholders:
    {stream_name} name of the streamer

Color options:
    color_bad: Stream offline or error
    color_good: Stream is live

Client ID:
    Example settings when creating your app at https://dev.twitch.tv

    Name: <your_name>_py3status
    OAuth Redirect URI: https://localhost
    Application Category: Application Integration


@author Alex Caswell horatioesf@virginmedia.com
@license BSD

SAMPLE OUTPUT
{'color': '#00FF00', 'full_text': 'exotic_bug is live!'}

offline
{'color': '#FF0000', 'full_text': 'exotic_bug is offline!'}
"""

import requests

STRING_MISSING = "missing {}"


class Py3status:
    """
    """

    # available configuration parameters
    cache_timeout = 60
    client_id = None
    format = "{stream_name} is live!"
    format_offline = "{stream_name} is offline."
    stream_name = None

    class Meta:
        deprecated = {"remove": [{"param": "format_invalid", "msg": "obsolete"}]}

    def post_config_hook(self):
        for config_name in ["client_id", "stream_name"]:
            if not getattr(self, config_name, None):
                raise Exception(STRING_MISSING.format(config_name))
        self._display_name = None

    def _get_display_name(self):
        url = "https://api.twitch.tv/kraken/users/" + self.stream_name
        display_name_request = requests.get(url, headers={"Client-ID": self.client_id})
        self._display_name = display_name_request.json().get("display_name")

    def twitch(self):
        if not self._display_name:
            self._get_display_name()

        r = requests.get(
            "https://api.twitch.tv/kraken/streams/" + self.stream_name,
            headers={"Client-ID": self.client_id},
        )
        if r.json().get("stream"):
            color = self.py3.COLOR_GOOD
            format = self.format
        else:
            color = self.py3.COLOR_BAD
            format = self.format_offline

        full_text = self.py3.safe_format(format, {"stream_name": self._display_name})

        response = {
            "cached_until": self.py3.time_in(self.cache_timeout),
            "full_text": full_text,
            "color": color,
        }
        return response


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
