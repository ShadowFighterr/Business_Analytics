-- Шаг 1: Добавляем новые столбцы в таблицу customers, если их еще нет
ALTER TABLE classicmodels.customers ADD COLUMN IF NOT EXISTS latitude NUMERIC(10, 6);
ALTER TABLE classicmodels.customers ADD COLUMN IF NOT EXISTS longitude NUMERIC(10, 6);

-- Шаг 2: Обновляем строки, добавляя координаты для известных городов
UPDATE classicmodels.customers SET latitude = 40.7128,  longitude = -74.0060  WHERE city = 'NYC';
UPDATE classicmodels.customers SET latitude = 34.0522,  longitude = -118.2437 WHERE city = 'Los Angeles';
UPDATE classicmodels.customers SET latitude = 48.8566,  longitude = 2.3522    WHERE city = 'Paris';
UPDATE classicmodels.customers SET latitude = 51.5074,  longitude = -0.1278   WHERE city = 'London';
UPDATE classicmodels.customers SET latitude = 35.6895,  longitude = 139.6917  WHERE city = 'Tokyo';
UPDATE classicmodels.customers SET latitude = -33.8688, longitude = 151.2093  WHERE city = 'Sydney';
UPDATE classicmodels.customers SET latitude = 45.4215,  longitude = -75.6972  WHERE city = 'Ottawa';
UPDATE classicmodels.customers SET latitude = 45.5017,  longitude = -73.5673  WHERE city = 'Montreal';
UPDATE classicmodels.customers SET latitude = 41.3851,  longitude = 2.1734    WHERE city = 'Barcelona';
UPDATE classicmodels.customers SET latitude = 40.4168,  longitude = -3.7038   WHERE city = 'Madrid';
UPDATE classicmodels.customers SET latitude = 52.5200,  longitude = 13.4050   WHERE city = 'Berlin';
