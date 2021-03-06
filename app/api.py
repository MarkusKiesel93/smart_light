from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import control
from app.config import config
from app.sheduler import Sheduler


app = FastAPI(title='API - Smartlight')

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_allowed_origins,
    allow_methods=config.cors_allowed_methods,
    allow_headers=config.cors_allowed_headers,
)


@app.get('/light/on/', status_code=status.HTTP_200_OK)
async def light_on():
    control.light_on()
    return {'light_on': True}


@app.get('/light/off/', status_code=status.HTTP_200_OK)
async def light_off():
    control.light_off()
    return {'light_on': False}


@app.get('/ambient-light/on/', status_code=status.HTTP_200_OK)
async def abient_light_on():
    control.ambient_light_on()
    return {'ambient_light_on': True}


@app.get('/ambient-light/off/', status_code=status.HTTP_200_OK)
async def ambient_light_off():
    control.ambient_light_off()
    return {'ambient_light_on': False}


@app.get('/light/{hour}/{minute}', status_code=status.HTTP_200_OK)
async def wakeup_light(hour: int, minute: int):
    if hour < 0 or hour > 24 or minute < 0 or minute > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not a correct time.'
        )
    Sheduler().set(hour, minute)
    return {'hour': hour, 'minute': minute}
