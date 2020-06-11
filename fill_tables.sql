INSERT INTO master
	(login, password, first_name, last_name)
VALUES
	('petrov', '123456', 'Алексей', 'Петров'),
	('kvakshina', '09876543', 'Алевтина', 'Квакшина');

INSERT INTO cat
	(master, name, sex, color, birth_date, height, mass)
VALUES
	('petrov', 'Мурка', 'женский', 'рыжий', '2020-01-17', 10, 2500),
	('kvakshina', 'Белка', 'женский', 'белый', '2018-07-30', 30, 4490),
	('kvakshina', 'Василий', 'мужской', 'чёрный', '2016-07-12', 35, 5103);

INSERT INTO disease
	(disease)
VALUES
	('ожирение'),
	('недобор веса'),
	('катаракта'),
	('лишай'),
	('сколиоз');

INSERT INTO cat_disease_history
	(disease, cat_id, start_date, end_date)
VALUES
	('ожирение', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Василий'), '2018-12-25', '2019-02-20'),
	('сколиоз', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Белка'), '2020-02-10', NULL);

INSERT INTO vet
	(login, password, first_name, last_name)
VALUES
	('kuznetsov', 'kuznets', 'Фёдор', 'Кузнецов'),
	('kovrizhkin', '182736', 'Александр', 'Коврижкин'),
	('potapova', 'parol', 'Елена', 'Потапова');

INSERT INTO specialty
	(specialty)
VALUES
	('терапевт'),
	('хирург'),
	('офтальмолог'),
	('оториноларинголог'),
	('невролог');

INSERT INTO vet_specialty
	(vet, specialty)
VALUES
	('kuznetsov', 'терапевт'),
	('kuznetsov', 'хирург'),
	('potapova', 'терапевт'),
	('potapova', 'оториноларинголог'),
	('kovrizhkin', 'офтальмолог');

INSERT INTO disease_state
	(disease_state)
VALUES
	('начало'),
	('продолжение'),
	('конец');

INSERT INTO prescription
	(start_date, end_date, directions)
VALUES
	('2018-12-25', '2019-01-25', 'Меньше кормить, следить за подвижностью'),
	('2019-01-28', '2019-02-10', 'Играть с мячом'),
	('2020-02-10', NULL, 'Кормить едой с добавкой кальция');

INSERT INTO examination
	(date_time, cat_id, vet_specialty_id, disease, disease_state, comments, prescription_id)
VALUES
	('2018-12-25 10:00:00', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Василий'), (SELECT vet_specialty_id FROM vet_specialty WHERE vet = 'potapova' AND specialty = 'терапевт'), 'ожирение', 'начало', 'Кот выглядит хорошо, но вяло', (SELECT prescription_id FROM prescription WHERE start_date = '2018-12-25')),
	('2019-01-28 11:15:00', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Василий'), (SELECT vet_specialty_id FROM vet_specialty WHERE vet = 'kuznetsov' AND specialty = 'терапевт'), 'ожирение', 'продолжение', 'Активность повысилась', (SELECT prescription_id FROM prescription WHERE start_date = '2019-01-28')),
	('2019-02-20 13:50:00', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Василий'), (SELECT vet_specialty_id FROM vet_specialty WHERE vet = 'kuznetsov' AND specialty = 'терапевт'), 'ожирение', 'конец', 'Нормальный вес', NULL),
	('2020-02-05 15:20:00', (SELECT cat_id FROM cat WHERE master = 'kvakshina' AND name = 'Белка'), (SELECT vet_specialty_id FROM vet_specialty WHERE vet = 'kuznetsov' AND specialty = 'хирург'), 'сколиоз', 'начало', 'Искривление 1-й степени', (SELECT prescription_id FROM prescription WHERE start_date = '2020-02-10'));
