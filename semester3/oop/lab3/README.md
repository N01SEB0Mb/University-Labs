## Auto service parts parser

**_(Outdated code)_**

### Description

This program collects info about parts from different sites and returns formatted response

#### List of supported sites:

- [AsiaPart](https://b2b.asiaparts.ua/)
- [AutoLider](https://online.avtolider-ua.com/)
- [AutoTechnics](https://b2b.ad.ua/)
- [Busmarket](https://bm.parts/)
- [Direct24](https://direct24.com.ua/)
- [InterCars](https://ic-ua.intercars.eu/)
- [Mahina](https://mahina.in.ua/)
- [MasterService](https://steering.com.ua/)
- [XPertAuto](https://xpert-auto.ua/)

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
Name             Connected    Signed in  Time
-------------  -----------  -----------  -------
direct24                 1            1  0.000 s
busmarket                1            1  0.000 s
autotechnics             1            1  0.192 s
intercars                1            1  0.662 s
xpertauto                1            1  1.091 s
mahina                   1            1  1.837 s
asiaparts                1            1  1.868 s
autolider                1            1  3.153 s
masterservice            1            1  3.670 s
Total authorization time: 3.692 s
```

After that you will see server initialization message:

```
 * Serving Flask app "parser.server.server" (lazy loading)
 * Environment: production
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now you can send requests

### Requests format:

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

    **Warning**: If number of articles and brands are different, you will get `400 BAD REQUEST` status code

    Examples:
    - You want to find part using article '115906' and brand 'sachs':
      
      `http://127.0.0.1:5000/parser/search?article=[115906]&brand=[sachs]`
    
    - You want to find '115906 SACHS' and '333368 KYB' only for **_Busmarket_**:
    
      `http://127.0.0.1:5000/parser/search?article=[115906,333368]&brand=[sachs,kyb]&sites=[busmarket]`
    
- If you want to get site currency info:
  
    `GET http://host:post/parser/currency&sites=[<sites>]`
  
