# Diplomové práce

## Authors

 * [Peter Tisovčík](https://github.com/mienkofax)
   * [List of created files](CREATED_PETO.md)
   * [Text of Master's thesis](https://www.fit.vutbr.cz/study/DP/DP.php.cs?id=22184)
   
   
 * [Klára Nečasová](https://github.com/Klarksonnek)
   * [List of created files](CREATED_KLARKA.md)
   * [Text of Master's thesis](https://www.fit.vutbr.cz/study/DP/DP.php.cs?id=22183)

## Generovanie API key

```bash
server # echo `pwgen 80 1` "= ja@example.org" >> /etc/beeeon/server/apikeys.properties
```

## Rozsahy prikladov (examples)

* 0000 - priklad s funkciami, ktore sa spustaju a ponukaju prehlad toho, co je v systeme dosutupne

* 0100 - 0199 - priklady pre Klarku

* 0200 - 0299 - priklady pre Peta

## Import DB

```bash
./db_util.sh import
```

## Export DB

```bash
./db_util.sh export
```

## Config file with keys

path: `/etc/dp/config.ini`

content:
```
[ant-work]
api.key =

[rehivetech]
api.key = 

[db]
host =localhost
user =
passwd =
database =statistiky

[rapidminer]
launcher = ./rapidminer-studio/RapidMiner-Studio.sh
repository.processes.path =
```
