## Auto service parts parser

### Description

This program collects info about parts from different sites and returns formatted response

#### List of supported sites:

- [AsiaPart](https://b2b.asiaparts.ua/)
- [AutoLider](https://online.avtolider-ua.com/)
- [AutoTechnics](https://b2b.ad.ua/)
- [Busmarket](https://bm.parts/)
- [Direct24](https://direct24.com.ua/)
- [FormParts](https://b2b.ad.ua/)

### Usage

Install required packages:

`
$ python3 -m pip install -r requirements.txt
`

Run server from terminal using following command:

`
$ python3 run.py
`

Before using, wait until program is authorized on all sites
You will see message with authorization status

Example:
```
Name          Connected    Signed in    Time
------------  -----------  -----------  -------
busmarket     True         True         0.000 s
autolider     True         True         0.284 s
autotechnics  True         True         0.301 s
formparts     True         True         0.555 s
direct24      True         True         0.698 s
asiaparts     True         True         3.411 s
Total authorization time: 3.413 s
```

After that you will see server initialization message:

```
 * Serving Flask app "parser.server.app" (lazy loading)
 * Environment: production
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now you can send requests

Requests format:

`GET http://host:port/parser/search?article=[<articles>]&brand=[<brands>]&sites=[<sites>]`

- If you want to search parts using only article, your requests is:
  
  `GET http://host:port/parser/search?article=[<articles>]`

  Examples:
   - You want to find parts using article - '_115906_':
     
     `http://127.0.0.1:5000/parser/search?article=[115906]`
    
   - You want to find few parts, '_115907_' and '_333368_':
    
     `http://127.0.0.1:5000/parser/search?article=[115907,333368]`
    
   - You want to find parts using article - '_115906_' only for **_AutoTechnics_**:
    
     `http://127.0.0.1:5000/parser/search?article=[115906]&sites[autotechnics]`
    
- If you want to search parts using article and brand, just add `brands` parameter:

   `GET http://host:port/parser/search?article=[<articles>]&brand=[<brands>]`

    **Warning**: If number of articles and brands are different, you will get `400 METHOD NOT ALLOWED` status code

    Examples:
    - You want to find part using article '115906' and brand 'sachs':
      
      `http://127.0.0.1:5000/parser/search?article=[115906]&brand=[sachs]`
    
    - You want to find '115906 SACHS' and '333368 KYB' only for **_Busmarket_**:
    
      `http://127.0.0.1:5000/parser/search?article=[115906,333368]&brand=[sachs,kyb]&sites=[busmarket]`
    
- If you want to get site currency info:
  
    `GET http://host:post/parser/currency&sites=[<sites>]`
  
