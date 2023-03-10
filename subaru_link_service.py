from subarulink import Controller
from subarulink import SubaruException
from aiohttp import ClientSession
import os
import asyncio
import logging 

SUBARU_USERNAME=""
SUBARU_PASSWORD=""
SUBARU_DEVICE_ID=""
SUBARU_DEVICE_NAME="subarulink"
SUBARU_VIN=""
SUBARU_PIN=""


LOGGER = logging.getLogger("subarulink")
STREAMHANDLER = logging.StreamHandler()
STREAMHANDLER.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
LOGGER.addHandler(STREAMHANDLER)
LOOP = asyncio.get_event_loop()

class SubaruLinkService():
    def __init__(self):
        self._current_vin = SUBARU_VIN
        self.__ctrl = None
        self.attributes = None
        self._pin = None
        self._car_data = None
        self._car_info = None
    
    @property
    def _ctrl(self):
        if self.__ctrl is None:
            self._session = ClientSession()
            self._cars = []
            self.__ctrl = Controller(
                self._session, # aiohttp
                SUBARU_USERNAME,
                SUBARU_PASSWORD,
                SUBARU_DEVICE_ID,
                self._pin,
                SUBARU_DEVICE_NAME,
            )
        return self.__ctrl
    
    async def connect(self, pin):
        LOGGER.info("Connecting to Subaru Remote Services API")
        self._pin = pin 
        try:
            if await self._ctrl.connect():
                self._current_hasEV = self._ctrl.get_ev_status(self._current_vin)
                self._current_hasRES = self._ctrl.get_res_status(self._current_vin)
                self._current_hasRemote = self._ctrl.get_remote_status(self._current_vin)
                self._current_api_gen = self._ctrl.get_api_gen(self._current_vin)
                LOGGER.info("Successfully connected")
            if self._current_api_gen == "g2":
                await self._fetch()
            else:
                LOGGER.error("Unsupprted telematics version: %s" % self._current_api_gen)
                return False
        except SubaruException:
            LOGGER.error("Unable to connect.  Check Username/Password.")
            await self._session.close()
            return False
        return True

    async def disconnect(self):
        await self._session.close()

    async def _fetch(self):
        LOGGER.info("Fetching data for %s..." % self._ctrl.vin_to_name(self._current_vin))
        self._car_data = await self._ctrl.get_data(self._current_vin)
        return True

    async def update(self):
        LOGGER.info("Requesting update for %s..." % self._ctrl.vin_to_name(self._current_vin))
        await self._ctrl.update(self._current_vin)
        await self._fetch()
        return True

    async def unlock(self):
        LOGGER.info("Requesting door unlock for %s..." % self._ctrl.vin_to_name(self._current_vin))
        if await self._ctrl.unlock(self._current_vin):
            self._car_data['doors'] = 'unlocked'
            return True
        else:
            return False
    
    async def lock(self):
        LOGGER.info("Requesting door lock for %s..." % self._ctrl.vin_to_name(self._current_vin))
        if await self._ctrl.lock(self._current_vin):
            self._car_data['doors'] = 'locked'
            return True
        else:
            return False

    async def start_engine(self):
        LOGGER.info("Requesting engine START for %s..." % self._ctrl.vin_to_name(self._current_vin))
        if self._car_data.get("climate") is None:
            await self._ctrl.get_climate_settings(self._current_vin)
            self._car_data = await self._ctrl.get_data(self._current_vin)
        await self._ctrl.remote_start(self._current_vin, self._car_data["climate"])
    
    async def stop_engine(self):
        LOGGER.info("Requesting engine STOP for %s..." % self._ctrl.vin_to_name(self._current_vin))
        await self._ctrl.remote_stop(self._current_vin)

    @property
    def car_data(self):
        return self._car_data
    
async def test():
    sls = SubaruLinkService()
    if await sls.connect(SUBARU_PIN):
        print(sls._car_data)
    await sls.disconnect()

if __name__ == '__main__':
    LOOP.run_until_complete(test())