# Diplomova praca

## Generovanie API key

```bash
server # echo `pwgen 80 1` "= ja@example.org" >> /etc/beeeon/server/apikeys.properties
```

## Rozsahy prikladov (examples)

* 0000 - priklad s funkciami, ktore sa spustaju a ponukaju prehlad toho, co je v systeme dosutupne

* 0100 - 0199 - priklady pre Klarku

* 0200 - 0299 - priklady pre Peta

## Import DB

### Full db

```bash
mysql -u root -p statistiky  < measured_peto.sql; \
	mysql -u root -p statistiky  < measured_klarka.sql
```

### Reduced db

```bash
mysql -u root -p statistiky  < measured_peto_reduced.sql; \
	mysql -u root -p statistiky  < measured_klarka_reduced.sql
```

## Export DB

### Full db

```bash
mysqldump -uroot -p statistiky measured_peto  > measured_peto.sql; \
	mysqldump -uroot -p statistiky measured_klarka  > measured_klarka.sql
```

### Reduced db

```bash
mysqldump -uroot -p statistiky measured_peto_reduced  > measured_peto_reduced.sql; \
	mysqldump -uroot -p statistiky measured_klarka_reduced  > measured_klarka_reduced.sql
```

## Config file with keys

path: `/etc/dp/config.ini`

content:
```
[beeeon]
api.key = thaegeshecaz1EN9lutho0laeku1ahsh9eec5waeg0aiqua2buo7ieyoo0Shoow9ahpoosomie0weiqu

[rehivetech]
api.key = jaixai1ohhee2Koohah5IeXae6wuvah7Fohhai9ohZ1AethoiRo7Ooth2Aic1EiSai3Iung6wai4Ahng

[db]
host =localhost
user =
passwd =
database =statistiky
```
