# Popis zařízení a událostí

Popis zařízení i událostí je v JSON formátu. Příkladem detekovatelné události může být 
otevření, zavření okna nebo sprchování.
 
## Příklad popisu zařízení

Popis zařízení se nachází v souboru devices.json.

```json
{
	"devices": [{
		"id": "jablotron",
		"name": "Jablotron open/close sensor",
		"gateway": "1908402624139667",
		"device": "0x900000000197053"
	}]
}
```

* **devices** - seznam zařízení
  * **id** - identifikátor zařízení (například řetězec) v rámci JSONu
  * **name** - název zařízení
  * **gateway** - identifikátor brány
  * **device** - identifikátor zařízení v rámci BeeeOnu
  
## Příklad popisu události

Popis událostí se nachází v souboru events.json.

```json
{
	"events": [{
		"description": "...",
		"location": "...",
		"people": 2,
		"type": "...",
		"event": {
			"start": "MM/DD/YYYY HH:MM:SS",
			"end": "MM/DD/YYYY HH:MM:SS",
			"devices": {
				"id": ["module_type"]
			},
			"params": {
				"name": "value"
			}
		}
	}]
}
```

* **events** - seznam událostí
  * **description** - popis události
  * **location** - umístění zařízení v rámci místnosti
  * **people** - počet lidí (číslo)
  * **type** - typ události (open_closed_window, showering, cooking)
  * **event** - detailní popis události 
    * **start** - začátek události (datum a čas)
    * **end** - konec události (datum a čas)
    * **devices** - identifikátor zařízení (id) : seznam typů modulů (typy modulů [zde](https://ant-work.fit.vutbr.cz:8010/tester.html#))
    * **params** - parametry události (specifické pro daný typ události)
    
    (**otevření nebo zavření okna** - počasí (calm, light breeze, moderate breeze, strong breeze;
    sunny, partly cloudy, cloudy, rain); **sprchování** - sprchovací zařízení (shower_enclosure, bath))


### Typ události: otevření nebo zavření okna

Hodnota parametru **weather** udává počasí:
* sunny
* partly cloudy
* cloudy
* thunderstorm
* drizzle
* rain
* snowfall

Hodnota parametru **wind** udává sílu větru: 
* calm
* light breeze
* moderate breeze
* strong breeze

```json
"type": "open_closed_window",
...
"params": {
    "weather": "sunny",
    "wind": "calm"  
}
```

### Typ události: sprchování

Hodnota parametru **equipment** definuje typ zařízení, které bylo použito pro sprchování:
* shower enclosure
* bath

```json
"type": "showering",
...
"params": {
    "equipment": "shower_enclosure"
}
```

# Popis třídy DataStorage

* načtení informací o zařízeních a událostech
  * ze souborů devices.json a events.json
* stažení dat o počasí, o události a o "neudálosti"

## Interní reprezentace dat o zařízeních a událostech

Pro vytvoření interní reprezentace dat o zařízeních a událostech se používají funkce `read_meta_data` a `set_no_event_time`.

### Výpis po zavolání funkce `read_meta_data`

```json
[
    {
        "description": "...",
        "event": {
            "devices": {
                "jablotron": {
                    "device": "0x900000000197053",
                    "gateway": "1908402624139667",
                    "id": "jablotron",
                    "modules": [
                        {
                            "id": "0",
                            "type_id": "open_close"
                        }
                    ],
                    "name": "Jablotron open/close sensor"
                },
                "protronix": {
                    "description": "Protronix senzor co2",
                    "device": "0xa9004a4a147d0001",
                    "gateway": "1816820318180747",
                    "id": "protronix",
                    "modules": [
                        {
                            "id": "2",
                            "type_id": "co2"
                        }
                    ]
                }
            },
            "end": 1525241103.0,
            "params": {
                "name": "value"
            },
            "start": 1525240920.0
        },
        "location": "...",
        "people": 2,
        "type": "..."
    },
    ...
]
```

* **description** - popis události
* **event** - identifikace zařízení, začátek a konec události, parametry události
* **location** - umístění zařízení v rámci místnosti
* **people** - počet lidí (číslo)
* **type** - typ události (open_closed_window, showering, cooking)

### Výpis po zavolání funkce `set_no_event_time`

```json
[
    {
        "description": "...",
        "event": {
            "devices": {
                ...
            },
            ...
            "end_no_event_time": 1525241113.0,
            "start_no_event_time": 1525240930.0
        },
       ...
    },
    ...
]
```

* **start_no_event_time** - časová značka začátku intervalu, kdy nedošlo k žádné události
* **end_no_event_time** - časová značka konce intervalu, kdy nedošlo k žádné události

## Funkce `download_data`

Funkce **doplní informace do načtených informací o zařízeních a událostech** (metadat) (viz Výpis po zavolání funkce set_no_event_time). 
Nejdříve vypočítá **časové značky před a po události a "neudálosti"**. Poté tyto značky použije **ke stažení
dat z BeeeOn serveru** a **pro specifikaci mezí intervalu**, ze kterého se **stáhnou informace o počasí** (tlak, relativní vlhkost, teplota a síla větru).

### Ukázka stažených dat
Následující stažená data v JSON formátu jsou dostupná uživateli, který s nimi může provádět chtěné operace.

```json
[
    {
        "description": "...",
        "event": {
            "devices": {
                "jablotron": {
                    "device": "0x900000000197053",
                    "gateway": "1908402624139667",
                    "id": "jablotron",
                    "modules": [
                        {
                            "id": "0",
                            "measured_value_event_end": [],
                            "measured_value_event_start": [
                                {
                                    "at": 1525240923,
                                    "value": "1.000000"
                                }
                            ],
                            "measured_value_no_event_end": [],
                            "measured_value_no_event_start": [],
                            "type_id": "open_close",
                            "weather_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.34888888889087,
                                    "temperature": 57,
                                    "time": 1525241093,
                                    "wind_speed": 14.325555555555606
                                }
                            ],
                            "weather_no_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.30666666666878,
                                    "temperature": 57,
                                    "time": 1525241112,
                                    "wind_speed": 14.34666666666672
                                }
                            ]
                        }
                    ],
                    "name": "Jablotron open/close sensor"
                },
                "protronix": {
                    "name": "Protronix senzor co2",
                    "device": "0xa9004a4a147d0001",
                    "gateway": "1816820318180747",
                    "id": "protronix",
                    "modules": [
                        {
                            "id": "2",
                            "measured_value_event_end": [
                                {
                                    "at": 1525241094,
                                    "value": "810.000000"
                                }
                            ],
                            "measured_value_event_start": [
                                {
                                    "at": 1525240914,
                                    "value": "967.000000"
                                }
                            ],
                            "measured_value_no_event_end": [],
                            "measured_value_no_event_start": [
                                {
                                    "at": 1525240929,
                                    "value": "968.000000"
                                }
                            ],
                            "type_id": "co2",
                            "weather_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.34888888889087,
                                    "temperature": 57,
                                    "time": 1525241093,
                                    "wind_speed": 14.325555555555606
                                }
                            ],
                            "weather_no_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.30666666666878,
                                    "temperature": 57,
                                    "time": 1525241112,
                                    "wind_speed": 14.34666666666672
                                }
                            ]
                        }
                    ]
                }
            },
            "end": 1525241103.0,
            "end_no_event_time": 1525241113.0,
            "params": {
                "name": "value"
            },
            "start": 1525240920.0,
            "start_no_event_time": 1525240930.0
        },
        "location": "...",
        "people": 2,
        "type": "..."
    },
    {
        "description": "...",
        "event": {
            "devices": {
                "jablotron": {
                    "device": "0x900000000197053",
                    "gateway": "1908402624139667",
                    "id": "jablotron",
                    "modules": [
                        {
                            "id": "0",
                            "measured_value_event_end": [],
                            "measured_value_event_start": [
                                {
                                    "at": 1525240923,
                                    "value": "1.000000"
                                }
                            ],
                            "measured_value_no_event_end": [],
                            "measured_value_no_event_start": [],
                            "type_id": "open_close",
                            "weather_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.34888888889087,
                                    "temperature": 57,
                                    "time": 1525241093,
                                    "wind_speed": 14.325555555555606
                                }
                            ],
                            "weather_no_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.30666666666878,
                                    "temperature": 57,
                                    "time": 1525241112,
                                    "wind_speed": 14.34666666666672
                                }
                            ]
                        }
                    ],
                    "name": "Jablotron open/close sensor"
                },
                "protronix": {
                    "name": "Protronix senzor co2",
                    "device": "0xa9004a4a147d0001",
                    "gateway": "1816820318180747",
                    "id": "protronix",
                    "modules": [
                        {
                            "id": "2",
                            "measured_value_event_end": [
                                {
                                    "at": 1525241094,
                                    "value": "810.000000"
                                }
                            ],
                            "measured_value_event_start": [
                                {
                                    "at": 1525240914,
                                    "value": "967.000000"
                                }
                            ],
                            "measured_value_no_event_end": [],
                            "measured_value_no_event_start": [
                                {
                                    "at": 1525240929,
                                    "value": "968.000000"
                                }
                            ],
                            "type_id": "co2",
                            "weather_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.34888888889087,
                                    "temperature": 57,
                                    "time": 1525241093,
                                    "wind_speed": 14.325555555555606
                                }
                            ],
                            "weather_no_event_start": [
                                {
                                    "pressure": 29.05,
                                    "relative_humidity": 66.30666666666878,
                                    "temperature": 57,
                                    "time": 1525241112,
                                    "wind_speed": 14.34666666666672
                                }
                            ]
                        }
                    ]
                }
            },
            "end": 1525241103.0,
            "end_no_event_time": 1525241113.0,
            "params": {
                "name": "value"
            },
            "start": 1525240920.0,
            "start_no_event_time": 1525240930.0
        },
        "location": "...",
        "people": 2,
        "type": "..."
    }
]
```

# Popis třídy `WeatherData`

Historická data o počasí v **JSON formátu** se stáhnou ze stránky xxx. Z těchto dat se uloží jen užitečné informace, tedy **časová značka, teplota, relativní vlhkost, tlak a síla větru**. Jelikož jsou historická data o počasí dostupná jen v **půlhodinových časových intervalech**, jsou **data nagenerována** tak, aby byla k dispozici hodnota daných veličin **každou sekundu**.

## Poznámky k implementaci nagenerování historických dat o počasí

* historická data o počasí každou půlhodinu (0,5 hodiny = 30 minut = 1800 sekund)
* po nagenerování historických dat o počasí 1800 dat za půlhodinu
* data občas mimo pravidelné časové intervaly (1-2 záznamů navíc)
* příklad
  * out_general: 49 záznamů za den
  * out_detailed: 86400:1800 = 48 (ALE 49 záznamů za den!)
  * zdůvodnění:
    * cyklus `for i in range(0, len(out_general) - 1):` způsobí, že dat je 48
    * příklad: `for i in range(0, 1):`, tzn. 2 záznamy jsou k dispozici, nageneruje se jen 1800 hodnot (data se generují v rámci intervalu)
