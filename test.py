import asyncio
import time

async def asincrono(t):
    print(f'Corutina')
    time.sleep(t)
    print('Termino la corutina')


async def main():
    await asyncio.gather(asincrono(2), asincrono(3))

asyncio.run(main())


