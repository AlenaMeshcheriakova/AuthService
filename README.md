# Auth Service

## Overview

This is a Auth Service, which part of telegram project - "DeutschLernen" designed for do registration, login and verification for User. 

## Dependensy

This service provide data from another service: DataServive and HttpService via grpc connection. 

## Features

/login
/register
/validate_token

## Prerequisites

- Python 3.8 or higher
- Use Poetry for a dependency installation from pyproject.toml:
(Install poetry and execute comand "poetry install")

## Environment

For enviroment installetion, you need to create you own .env and .test.env file
In cfg/config.py please write link to your cfg files
For a template use file: .template.env

## Installation

### Clone the Repository

https://github.com/AlenaMeshcheriakova/AuthService.git
cd BotService
