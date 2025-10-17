-- Шаг 1: Добавляем новые столбцы в таблицу customers, если их еще нет
ALTER TABLE classicmodels.customers ADD COLUMN IF NOT EXISTS latitude NUMERIC(10, 6);
ALTER TABLE classicmodels.customers ADD COLUMN IF NOT EXISTS longitude NUMERIC(10, 6);

-- Шаг 2: Обновляем строки, добавляя координаты для ВСЕХ уникальных городов
-- Северная Америка
UPDATE classicmodels.customers SET latitude = 40.7128,  longitude = -74.0060  WHERE city = 'NYC';
UPDATE classicmodels.customers SET latitude = 42.3601,  longitude = -71.0589  WHERE city = 'Boston';
UPDATE classicmodels.customers SET latitude = 42.7325,  longitude = -84.5555  WHERE city = 'Lansing';
UPDATE classicmodels.customers SET latitude = 34.0522,  longitude = -118.2437 WHERE city = 'Los Angeles';
UPDATE classicmodels.customers SET latitude = 37.7749,  longitude = -122.4194 WHERE city = 'San Francisco';
UPDATE classicmodels.customers SET latitude = 37.3541,  longitude = -121.9552 WHERE city = 'San Jose';
UPDATE classicmodels.customers SET latitude = 37.2333,  longitude = -121.7833 WHERE city = 'Campbell';
UPDATE classicmodels.customers SET latitude = 34.1478,  longitude = -118.1445 WHERE city = 'Pasadena';
UPDATE classicmodels.customers SET latitude = 34.1561,  longitude = -118.2553 WHERE city = 'Glendale';
UPDATE classicmodels.customers SET latitude = 33.6846,  longitude = -117.8265 WHERE city = 'Irvine';
UPDATE classicmodels.customers SET latitude = 37.8715,  longitude = -122.2730 WHERE city = 'Berkeley';
UPDATE classicmodels.customers SET latitude = 36.1699,  longitude = -115.1398 WHERE city = 'Las Vegas';
UPDATE classicmodels.customers SET latitude = 44.9778,  longitude = -93.2650  WHERE city = 'Minneapolis';
UPDATE classicmodels.customers SET latitude = 43.1566,  longitude = -77.6088  WHERE city = 'Rochester';
UPDATE classicmodels.customers SET latitude = 40.2737,  longitude = -74.7430  WHERE city = 'Trenton';
UPDATE classicmodels.customers SET latitude = 40.0583,  longitude = -74.4057  WHERE city = 'Philadelphia';
UPDATE classicmodels.customers SET latitude = 41.4993,  longitude = -81.6944  WHERE city = 'Cleveland';
UPDATE classicmodels.customers SET latitude = 42.4440,  longitude = -76.5019  WHERE city = 'Ithaca';
UPDATE classicmodels.customers SET latitude = 43.0481,  longitude = -76.1474  WHERE city = 'Syracuse';
UPDATE classicmodels.customers SET latitude = 42.8864,  longitude = -78.8784  WHERE city = 'Buffalo';
UPDATE classicmodels.customers SET latitude = 41.7658,  longitude = -72.6734  WHERE city = 'Hartford';
UPDATE classicmodels.customers SET latitude = 41.3083,  longitude = -72.9279  WHERE city = 'New Haven';
UPDATE classicmodels.customers SET latitude = 43.6532,  longitude = -79.3832  WHERE city = 'Toronto';
UPDATE classicmodels.customers SET latitude = 49.2827,  longitude = -123.1207 WHERE city = 'Vancouver';

-- Европа
UPDATE classicmodels.customers SET latitude = 48.8566,  longitude = 2.3522    WHERE city = 'Paris';
UPDATE classicmodels.customers SET latitude = 43.7000,  longitude = 7.2667    WHERE city = 'Nice';
UPDATE classicmodels.customers SET latitude = 44.8378,  longitude = -0.5792   WHERE city = 'Bordeaux';
UPDATE classicmodels.customers SET latitude = 47.2184,  longitude = -1.5536   WHERE city = 'Nantes';
UPDATE classicmodels.customers SET latitude = 50.8503,  longitude = 4.3517    WHERE city = 'Bruxelles';
UPDATE classicmodels.customers SET latitude = 51.5074,  longitude = -0.1278   WHERE city = 'London';
UPDATE classicmodels.customers SET latitude = 53.4808,  longitude = -2.2426   WHERE city = 'Manchester';
UPDATE classicmodels.customers SET latitude = 53.4084,  longitude = -2.9916   WHERE city = 'Liverpool';
UPDATE classicmodels.customers SET latitude = 53.5511,  longitude = 9.9937    WHERE city = 'Hamburg';
UPDATE classicmodels.customers SET latitude = 52.5200,  longitude = 13.4050   WHERE city = 'Berlin';
UPDATE classicmodels.customers SET latitude = 48.1351,  longitude = 11.5820   WHERE city = 'Munich';
UPDATE classicmodels.customers SET latitude = 50.1109,  longitude = 8.6821    WHERE city = 'Frankfurt';
UPDATE classicmodels.customers SET latitude = 40.4168,  longitude = -3.7038   WHERE city = 'Madrid';
UPDATE classicmodels.customers SET latitude = 45.4642,  longitude = 9.1900    WHERE city = 'Milan';
UPDATE classicmodels.customers SET latitude = 46.2044,  longitude = 6.1432    WHERE city = 'Geneve';
UPDATE classicmodels.customers SET latitude = 59.3293,  longitude = 18.0686   WHERE city = 'Stockholm';
UPDATE classicmodels.customers SET latitude = 59.9139,  longitude = 10.7522   WHERE city = 'Oslo';
UPDATE classicmodels.customers SET latitude = 55.6761,  longitude = 12.5683   WHERE city = 'Copenhagen';
UPDATE classicmodels.customers SET latitude = 53.3498,  longitude = -6.2603   WHERE city = 'Dublin';

-- Азия и Австралия
UPDATE classicmodels.customers SET latitude = 35.6895,  longitude = 139.6917  WHERE city = 'Tokyo';
UPDATE classicmodels.customers SET latitude = 34.6937,  longitude = 135.5023  WHERE city = 'Osaka';
UPDATE classicmodels.customers SET latitude = 22.3193,  longitude = 114.1694  WHERE city = 'Hong Kong';
UPDATE classicmodels.customers SET latitude = 1.3521,   longitude = 103.8198  WHERE city = 'Singapore';
UPDATE classicmodels.customers SET latitude = -33.8688, longitude = 151.2093  WHERE city = 'Sydney';
UPDATE classicmodels.customers SET latitude = -37.8136, longitude = 144.9631  WHERE city = 'Melbourne';
