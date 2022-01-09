# Create an asynchronous request to the Revolut Sandbox API
# to authenticate the user.
import asyncio

# TODO: Change to Utils logging
import logging
import requests


from fastapi import APIRouter, Body, Depends, HTTPException, Query
from app import models
from sqlmodel import Session

from app.utils import deps


# Create Authentication Client
class AuthenticationClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://xs2a-sandbox.ubs.com",
    ):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self, username: str, password: str):
        """
        Get a token from the Revolut API.
        """
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(
            f"{self.base_url}/xs2a/v1/auth/token", data=payload
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )
