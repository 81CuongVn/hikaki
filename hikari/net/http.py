#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of the V7 HTTP REST API with rate-limiting.
"""
import asyncio
import logging
from typing import Optional

import aiohttp


class HTTP:
    #: The API version to use.
    VERSION = 7
    #: The base Discord URI to use for the HTTP API.
    BASE_URI = ""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self._buckets = {}
        self._logger = logging.getLogger(type(self).__name__)
        self._session = aiohttp.ClientSession(loop=loop)

        #: The asyncio event loop to run on.
        self.loop = loop

    @staticmethod
    def _bucket_name_for(
        uri_format: str,
        guild_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
    ) -> str:
        """
        Generates a unique bucket name for the ratelimit bucket representable by the given arguments.

        Args:
            uri_format: the format string for a URI with named placeholders.
            guild_id: optional guild ID for the request.
            channel_id: optional channel_id for the request.
            webhook_id: optional webhook_id for the request.
        """
        return uri_format.format(
            guild_id=guild_id, channel_id=channel_id, webhook_id=webhook_id
        )