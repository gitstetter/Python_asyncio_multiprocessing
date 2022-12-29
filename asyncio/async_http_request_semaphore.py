import aiohttp
import asyncio


def chunked_http_client(num_chunks):
    """
    Returns a function that can fetch from a URL, ensuring that only
    "num_chunks" of simultaneous connects are made.
    """
    semaphore = asyncio.Semaphore(num_chunks)  # <- define limit of requests

    async def http_get(url, client_session):  # <- new coroutine to download files files asynchonously using semaphore
        nonlocal semaphore #<- nonlocal keyword is used to work with variables inside nested functions, where the variable should not belong to the inner function.
        async with semaphore:
            async with client_session.request("GET", url) as response:
                return await response.text()#<- return futures

    return http_get

async def main():
    urls = ["https://binaryjazz.us/wp-json/genrenator/v1/genre/"]*1_00 #<- input lists to get from
    responses = [] #<- putput list of hettp responses

    http_client = chunked_http_client(100) #<- set async http client wit limit of parallel requests

    async with aiohttp.ClientSession() as client_session: #<- use aiohttp.ClientSession to call nonblocking get function in http_get()
        tasks = [http_client(url, client_session) for url in urls]  # save returned futures as list
        for future in asyncio.as_completed(tasks):  # wait for futures to complete
            data = await future
            responses.append(data)

    return responses

if __name__ =="__main__":
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(main())
    print(responses)
    print(len(responses))
