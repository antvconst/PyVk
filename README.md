PyVk
====

###Python wrapper for [VK](http://vk.com) API

####Usage example:
```python
from VkApi import VkApi
api = VkApi(client_id=3869166, scope=['offline', 'audio'], console_auth=True, keep_token=True)
api.request('audio.get')
```
####Constructor arguments:
* _client_id=0_: VK API app identifier.
* _scope=[]_: API methods groups app can call
* _access_token=str()_: API session identifier
* _console_auth=False_: if is True, console auth will be performed (see _Authorization flow_)
* _keep_token=False_: save the _access_token_ into _**auth.json**_ for later use
* _try_loading_token=False_: if is True, tries to load the token from _**auth.json**_

#### Authorization flow:
1. _If ```try_loading_token=True``` is provided, constructor will try to load saved token from **auth.json**_
2. _If access_token argument is provided, it will be saved, no additional auth is required._
3. _If **client_id and scope** are provided, they will be saved and used for manual auth._
    * Create instance with these arguments provided to constructor
    * Call ```get_auth_url()``` method
    * Open the given URL and authorize user
    * Call ```set_token(access_token)``` to save token.
4. _If **console_auth=True** is provided in addition to **client_id and scope** the console auth will be performed: just follow the instructions_

#### Public methods:
* ```set_token(access_token)```: sets the provided token for using in requests
* ```get_token()```: returns _access_token_
* ```is_authorized()```: returns True, if authorized, else returns False
* ```get_auth_url()```: return URL for manual authorization (see _Authorization flow_)
* ```request(api_method, data={})```: processes request to API

#### Error handling:
* Constructor raises IncorrectAuthInfoException, if not enough arguments were provided
* ```request(api_method, data={})``` raises NotAuthorizedException, if not authorized
* ```request(api_method, data={})``` raises RequestErrorException with _error_msg_, if request somewhy fails
