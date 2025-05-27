sistema pra simular um hospital

banco de dados local

parametros: 
nome da conta: hospitaldbmanager
senha: QcySaDbWczNupvvl
nome do banco: hospitalDB

-----------------------------------------

prompts do sql para o sistema funcionar:

CREATE TABLE blood_type(

    id SERIAL PRIMARY KEY,
    type VARCHAR(3) UNIQUE NOT NULL

);

CREATE TABLE patient(

    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    sex BOOLEAN NOT NULL,
    phone CHAR(11) NOT NULL,
    address TEXT NOT NULL,
    email TEXT,
    blood_type_id INT REFERENCES blood_type(id),
    allergies TEXT,
    status BOOLEAN NOT NULL DEFAULT FALSE

);

CREATE TABLE doctor(

    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    crm INTEGER UNIQUE NOT NULL,
    phone CHAR(11) NOT NULL,
    email TEXT,
    shift_start TIME NOT NULL,
    shift_finish TIME NOT NULL

);

CREATE TABLE appointment(

    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id) NOT NULL,
    doctor_id INTEGER REFERENCES doctor(id) NOT NULL,
    date_time TIMESTAMP NOT NULL

);

CREATE TABLE user_system(

    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    permission_tier INTEGER NOT NULL

);

CREATE TABLE patient_status_log(

    id SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    user_system_id INTEGER REFERENCES user_system(id) NOT NULL,
    patient_id INTEGER REFERENCES patient(id) NOT NULL,
    reason TEXT NOT NULL

);

CREATE TABLE patient_edit_log(

	id SERIAL PRIMARY KEY,
	date_time TIMESTAMP NOT NULL,
	patient_id INT REFERENCES patient(id) NOT NULL,
	user_system_id INT REFERENCES user_system(id) NOT NULL,
	changes TEXT NOT NULL

)

INSERT INTO blood_type(type) VALUES

    ('A+'),
    ('A-'),
	('AB+'),
	('AB-'),
	('B+'),
	('B-'),
	('O+'),
	('O-')

----------------------------------

inserts de teste:

INSERT INTO patient (name, cpf, birth_date, sex, phone, address, email, blood_type_id, allergies, status) VALUES 
    
    ('Sr. Miguel Pinto', '91284817636', '1928-04-02', False, '73028098523', 'Largo Barbosa, 574, Alípio De Melo, 02782-128 Melo do Amparo / ES', 'ianrocha@carvalho.net', 7, NULL, FALSE),
    ('Agatha da Conceição', '61931481407', '1948-07-02', False, '29915018815', 'Feira Guilherme Nascimento, 26, Jardim Felicidade, 44520-295 Moreira / BA', 'danielaazevedo@bol.com.br', 7, 'debitis', FALSE),
    ('Caio da Mota', '61455996262', '1928-09-07', False, '48506257650', 'Trecho Cardoso, 25, Manacas, 80113872 Nascimento / CE', 'agatha78@cardoso.org', 3, NULL, FALSE),
    ('Pedro Miguel Aragão', '86666064798', '1947-07-28', False, '67934741965', 'Parque de Silveira, 34, Fernão Dias, 08721049 Barros Paulista / RR', 'pedrocardoso@peixoto.br', 6, NULL, FALSE),
    ('Lara Mendes', '90510493157', '2015-07-06', True, '08367703158', 'Loteamento Monteiro, 10, Nossa Senhora Do Rosário, 78112468 Oliveira Verde / DF', 'antoniooliveira@mendes.com', 7, 'distinctio', FALSE),
    ('Kamilly da Conceição', '32067749692', '1972-01-01', True, '37693785001', 'Estação Azevedo, 30, Santa Tereza, 21560-718 Nunes Verde / RJ', 'rochaesther@goncalves.br', 5, 'esse', FALSE),
    ('Diogo Porto', '41154884414', '2008-11-11', False, '79061890623', 'Praça Heloísa Carvalho, 49, Comiteco, 58216-937 da Cunha / ES', 'cgoncalves@aragao.com', 6, 'rerum', FALSE),
    ('Cauê Cavalcanti', '85353626303', '1989-02-07', True, '58779180078', 'Alameda de Novaes, 24, Etelvina Carneiro, 55581357 da Costa da Praia / RR', 'sda-paz@yahoo.com.br', 1, 'rerum', FALSE),
    ('Caroline Lima', '75170142501', '2011-10-13', True, '53781312474', 'Jardim Vicente Ramos, 19, Inconfidência, 29583-281 Nascimento / SC', 'gomesemanuelly@porto.com', 8, NULL, FALSE),
    ('Levi Mendes', '77177231072', '1927-01-23', True, '11757545926', 'Parque de Castro, 13, Vila Petropolis, 86802-926 Moura / RR', 'duartelucas-gabriel@da.com', NULL, 'reiciendis', FALSE),
    ('Dr. Davi Lucca da Mota', '76586795508', '1939-08-01', True, '52457447526', 'Sítio de Nunes, 40, Coqueiros, 42948525 da Cruz Paulista / MA', NULL, 3, 'unde', FALSE),
    ('Ana Clara Aragão', '28586728900', '1936-07-27', False, '95372473125', 'Parque de Barros, 99, Canadá, 92301-081 Oliveira Verde / PR', 'mirella02@lopes.br', NULL, NULL, FALSE),
    ('Isadora Gonçalves', '26419580900', '2022-08-12', True, '78249495646', 'Praia da Mota, 5, Vila Batik, 97622182 Moraes dos Dourados / PA', NULL, 5, 'labore', FALSE),
    ('Paulo Novaes', '49569633433', '2011-08-29', False, '66266844818', 'Pátio de Cunha, 34, Novo Santa Cecilia, 25760-605 Nunes do Amparo / GO', NULL, NULL, 'consectetur', FALSE),
    ('Yuri Moura', '79198072048', '1993-04-06', True, '16320419753', 'Loteamento Rafaela Gonçalves, Vila Jardim Alvorada, 05418522 Vieira da Mata / ES', 'davi-luccada-cunha@da.br', 7, 'odit', FALSE),
    ('Esther Gomes', '35741981402', '2006-08-08', False, '15711196727', 'Lago da Costa, 39, Custodinha, 22744-067 Rodrigues / CE', 'almeidamarcela@caldeira.br', 5, NULL, FALSE),
    ('Maysa Rodrigues', '90548868034', '1973-04-30', True, '01027314942', 'Quadra de Barros, Vila Nova Cachoeirinha 3ª Seção, 65760-063 Farias de Azevedo / RS', 'oda-rocha@goncalves.org', NULL, 'et', FALSE),
    ('Marcelo Azevedo', '99247962927', '1983-11-26', False, '77533145862', 'Colônia Jesus, 27, Eymard, 86783558 Santos Alegre / PE', 'pintoana-livia@gmail.com', 8, 'officiis', FALSE),
    ('Lucas da Paz', '62651034665', '1989-10-16', False, '78487034787', 'Vale de Araújo, 63, Nova Esperança, 74259-175 Viana da Prata / MA', 'ana-julia60@gmail.com', 8, 'libero', FALSE),
    ('Daniel da Rosa', '43225591076', '1998-09-27', True, '26974064617', 'Setor da Conceição, 6, Santa Rita De Cássia, 83469-191 da Costa / MG', NULL, 2, 'veritatis', FALSE),
    ('Clarice Silveira', '74779698243', '1975-08-16', False, '59710558580', 'Lago de Silveira, 97, Coração Eucarístico, 25325751 Azevedo / SE', 'sda-rocha@da.br', 7, NULL, FALSE),
    ('Luiz Miguel Campos', '95327187705', '1956-08-07', False, '86458343564', 'Distrito Davi Lucas Santos, 4, Sion, 67708937 Nunes de da Conceição / RN', 'limamiguel@da.com', 4, 'possimus', FALSE),
    ('Davi Lucas Castro', '35736657210', '1979-07-29', False, '52867169305', 'Setor Costa, 7, Esplanada, 40238878 Pires do Campo / MS', 'isabelsouza@bol.com.br', 4, 'nulla', FALSE),
    ('João Guilherme Cardoso', '44370830168', '1954-08-19', False, '63628710856', 'Setor de Correia, Serra Do Curral, 53348001 Gomes / ES', 'pedro97@gmail.com', NULL, NULL, FALSE),
    ('Felipe Barros', '17265990781', '1995-01-06', True, '43031069173', 'Trevo da Paz, 6, Unidas, 86755-495 Fogaça / SP', 'maria-fernanda68@ferreira.com', 4, 'corrupti', FALSE),
    ('Ian Monteiro', '39344199094', '1937-03-13', True, '82767616804', 'Vila de Duarte, 74, São Francisco Das Chagas, 38284617 Dias / ES', 'davi-luiz21@porto.net', 8, 'voluptate', FALSE),
    ('Vicente Silveira', '57122371050', '1982-05-24', True, '62846722102', 'Condomínio de da Luz, 66, Candelaria, 30033057 Azevedo dos Dourados / MT', NULL, 7, NULL, FALSE),
    ('Sra. Melissa Cardoso', '97854825025', '1924-10-25', True, '65341846351', 'Rodovia Igor Pereira, 67, Novo Tupi, 67112091 Costela do Galho / RO', 'cviana@yahoo.com.br', 7, 'culpa', FALSE),
    ('Bernardo Moreira', '08611164962', '1970-03-29', True, '73430305932', 'Via de Ferreira, 650, Ápia, 72079-034 Melo do Sul / AM', 'qda-paz@uol.com.br', 4, 'quisquam', FALSE),
    ('Guilherme das Neves', '74503465325', '1936-10-22', True, '03998350900', 'Conjunto de Souza, 36, Ambrosina, 28490069 Viana Grande / AM', 'rfreitas@souza.com', NULL, 'pariatur', FALSE),
    ('Lorena Melo', '81047141558', '1946-09-16', False, '00247611300', 'Avenida Rocha, 86, Satelite, 16409651 Sales de da Luz / PI', 'ryanribeiro@hotmail.com', 8, 'perferendis', FALSE),
    ('Larissa Santos', '77730560720', '2013-10-25', True, '56429559246', 'Loteamento Pereira, 55, Conjunto Floramar, 53312210 Aragão das Flores / AP', 'luiz-henrique05@uol.com.br', 8, NULL, FALSE),
    ('Benício da Cruz', '80907120377', '2000-04-29', True, '38232585602', 'Morro Caio Farias, 33, Cruzeiro, 62293-970 Campos de Castro / MA', 'costaerick@ig.com.br', 4, 'vero', FALSE),
    ('Sra. Helena Fernandes', '82213169039', '1989-07-09', False, '90570649470', 'Largo de da Luz, Horto, 62493-573 Nascimento / AM', 'lunavieira@silva.br', 8, 'tenetur', FALSE),
    ('Eduardo Silveira', '50780305302', '2010-12-11', True, '64648756774', 'Trevo de Silva, 93, Canaa, 86495141 Silva / PI', 'ribeirocarlos-eduardo@ig.com.br', 1, 'quae', FALSE),
    ('Ryan Rodrigues', '88729506948', '2009-10-15', False, '82803622528', 'Campo de Freitas, 22, Vila Nova Gameleira 3ª Seção, 23025615 da Luz / BA', 'evelyn53@jesus.br', 5, 'quis', FALSE),
    ('Bryan Viana', '28734838570', '2008-03-06', True, '38195874070', 'Estação Ana Sophia Silveira, Barro Preto, 36283-540 Lopes da Serra / BA', 'luiza44@bol.com.br', 6, 'voluptate', FALSE),
    ('Emanuella Ferreira', '48090827683', '1966-09-07', True, '48519461747', 'Conjunto Sophie Silva, 77, Marajó, 38947898 Correia / GO', 'qpereira@da.com', 6, NULL, FALSE),
    ('Clara Rezende', '59015824894', '1977-04-20', True, '93014807742', 'Trecho Moura, 71, Minas Caixa, 99507190 Pires Verde / SP', 'pietra78@almeida.com', 6, 'voluptatem', FALSE),
    ('Mariane da Cunha', '84604789126', '1929-02-12', True, '27802037211', 'Passarela João Lucas Santos, 90, Campo Alegre, 24942667 da Cruz do Sul / RN', 'almeidalara@gmail.com', 4, 'ex', FALSE),
    ('Isis da Luz', '12719833622', '1943-04-01', True, '60080228253', 'Vila João Felipe da Rosa, 6, João Pinheiro, 19496103 da Paz de Viana / ES', 'nicole89@ig.com.br', 1, NULL, FALSE),
    ('Cauê Caldeira', '37036699930', '2003-06-30', False, '63346001517', 'Via Benício Freitas, Floramar, 50993-189 Cunha Verde / MG', NULL, 1, 'harum', FALSE),
    ('Srta. Sabrina Barros', '37992175840', '2008-11-28', False, '47181599536', 'Setor Correia, 7, Vila Califórnia, 63999402 Moreira de Dias / RJ', 'sofia18@cardoso.net', 6, 'sit', FALSE),
    ('Luigi Porto', '39615096032', '1979-08-10', True, '08325926556', 'Lagoa Ana Clara Freitas, 4, São Pedro, 58426529 Campos da Prata / AL', 'yda-rosa@gomes.br', 6, NULL, FALSE),
    ('Joaquim Martins', '65020410608', '1949-06-27', False, '65123322042', 'Núcleo Farias, 8, São João Batista, 09940337 Cardoso Paulista / CE', 'alexia11@uol.com.br', NULL, 'voluptate', FALSE),
    ('Vitor Ribeiro', '88881971330', '1990-11-09', False, '74262665490', 'Campo Moreira, 15, Flavio De Oliveira, 68495-688 Gomes / MG', 'kamillymonteiro@uol.com.br', 1, 'quisquam', FALSE),
    ('Juliana Aragão', '14105660802', '1962-10-25', False, '12291578749', 'Conjunto de Ramos, 6, Conjunto Celso Machado, 33672049 Souza da Serra / AL', NULL, 1, NULL, FALSE),
    ('Ana da Costa', '04136337990', '1985-07-17', True, '83842598652', 'Passarela de da Rosa, 59, Vila Coqueiral, 19385898 Silva / AC', 'ribeiroleandro@correia.com', 3, 'facere', FALSE),
    ('Leandro Rezende', '70476464340', '1965-01-10', True, '37456574688', 'Pátio Teixeira, 86, Solar Do Barreiro, 59227232 Sales das Flores / MT', 'nicolas06@da.com', 6, 'voluptatem', FALSE),
    ('Helena Silveira', '61056012471', '1971-06-13', True, '78205050162', 'Favela Vieira, 258, São Cristóvão, 99869-027 Vieira / MS', 'salescarolina@uol.com.br', 1, 'quam', FALSE);

INSERT INTO doctor (name, cpf, crm, phone, email, shift_start, shift_finish) VALUES 

    ('João Gabriel Moraes', '13309776883', 50010, '65747822666', 'da-rochathomas@gmail.com', '17:00:00', '20:00:00'),
    ('Luiz Otávio Moreira', '52294286278', 40858, '10398962495', 'yuri41@rocha.org', '13:30:00', '18:30:00'),
    ('Ana Clara Melo', '92206266830', 10591, '65604353673', 'yasmin78@yahoo.com.br', '18:30:00', '00:30:00'),
    ('Sr. Luiz Gustavo da Rosa', '58523684077', 53473, '85002984847', NULL, '16:15:00', '20:15:00'),
    ('Sr. Luiz Henrique Pinto', '32017618691', 78467, '58250990528', NULL, '14:00:00', '16:00:00'),
    ('Marcos Vinicius da Luz', '99390878373', 91762, '38213936565', 'araujothiago@cunha.org', '12:00:00', '15:00:00'),
    ('Maria Vitória Gonçalves', '83039354612', 27487, '25516898806', NULL, '06:15:00', '08:15:00'),
    ('Breno Nogueira', '76777371532', 49687, '12446647826', NULL, '07:00:00', '12:00:00'),
    ('Luiz Miguel da Mota', '77201306774', 53948, '42332858964', 'pmonteiro@bol.com.br', '14:15:00', '17:15:00'),
    ('Yago Moura', '31040317979', 87812, '14699477546', 'igormoura@yahoo.com.br', '16:30:00', '19:30:00'),
    ('Bruno Costela', '17132084909', 13799, '04754916440', NULL, '06:15:00', '08:15:00'),
    ('Gabriela Cunha', '90500125406', 62990, '32796199361', 'agathanascimento@uol.com.br', '10:15:00', '13:15:00'),
    ('Clarice Costa', '34037309564', 56300, '47218352089', NULL, '16:45:00', '17:45:00'),
    ('Lucas Almeida', '50402814479', 17370, '86025097546', 'iduarte@yahoo.com.br', '18:30:00', '20:30:00'),
    ('Catarina Lima', '42727634900', 51660, '72177792939', 'ana-laurada-luz@melo.com', '14:30:00', '15:30:00'),
    ('Gustavo Henrique Almeida', '38834311922', 36245, '85967055389', 'vcosta@rocha.com', '18:30:00', '22:30:00'),
    ('Ana Carvalho', '79434850924', 75345, '08992983068', 'qcampos@azevedo.com', '16:30:00', '20:30:00'),
    ('Larissa Alves', '61040533868', 64880, '09957063820', NULL, '16:15:00', '18:15:00'),
    ('Evelyn Pires', '15550547813', 87428, '69488034026', 'luiz-gustavoda-costa@bol.com.br', '09:30:00', '10:30:00'),
    ('Maria Julia Almeida', '84181119920', 16812, '96997993817', 'cauasilveira@gmail.com', '06:30:00', '10:30:00'),
    ('Joana Costela', '97829721505', 82132, '91314905954', NULL, '15:15:00', '20:15:00'),
    ('Ana Clara Duarte', '72820822940', 80689, '70239691707', 'rebeca94@ig.com.br', '11:45:00', '12:45:00'),
    ('Beatriz da Costa', '47320781417', 99981, '49652048511', 'ana-lauralopes@yahoo.com.br', '18:00:00', '20:00:00'),
    ('João Melo', '04314932511', 58526, '50610255252', 'livianovaes@yahoo.com.br', '17:00:00', '21:00:00'),
    ('João Pedro Viana', '79063003196', 11382, '34773247866', 'yagosales@hotmail.com', '13:30:00', '19:30:00'),
    ('Luiza Nascimento', '88966036414', 19973, '96294482747', 'davi-luizmartins@ig.com.br', '12:30:00', '16:30:00'),
    ('Rebeca Caldeira', '45462175876', 12182, '01900636689', 'renanteixeira@gmail.com', '16:30:00', '21:30:00'),
    ('Ana Vitória Barros', '37551626603', 13448, '63989834251', NULL, '06:30:00', '12:30:00'),
    ('Miguel Jesus', '48123822707', 20047, '50452384793', 'walmeida@costela.com', '18:15:00', '22:15:00'),
    ('Cecília Ramos', '20609039555', 16472, '00820693673', NULL, '07:45:00', '12:45:00'),
    ('Gabrielly Monteiro', '28754887240', 82058, '79867794709', 'mariana80@silva.com', '17:15:00', '23:15:00'),
    ('Luana da Mota', '19899054046', 90579, '81870437498', 'tcosta@moraes.br', '14:45:00', '16:45:00'),
    ('Rafaela Cardoso', '71717456359', 13548, '31596311396', 'caueda-luz@yahoo.com.br', '09:15:00', '10:15:00'),
    ('Lucas Gabriel Farias', '44542708055', 81542, '47444013943', 'cardosonathan@uol.com.br', '14:30:00', '19:30:00'),
    ('Dr. Nathan da Mota', '23214633686', 78545, '80967814252', 'anthonyda-cruz@moraes.br', '18:45:00', '19:45:00'),
    ('Sarah Nascimento', '69532293302', 61479, '51753389891', NULL, '16:45:00', '20:45:00'),
    ('Ana Carolina Pires', '32370420057', 47748, '08739606766', NULL, '18:15:00', '20:15:00'),
    ('Dr. João Lucas Moreira', '03406730280', 16158, '13431968640', 'camposcamila@gmail.com', '14:00:00', '18:00:00'),
    ('Ian Lopes', '50361497504', 79734, '81367609790', 'jcostela@ig.com.br', '07:30:00', '13:30:00'),
    ('Miguel Almeida', '33952476781', 20734, '66820080421', 'goncalvesalicia@barros.com', '12:00:00', '15:00:00'),
    ('Ana Luiza Cardoso', '12398846300', 18914, '56877356309', 'gmoura@gmail.com', '08:45:00', '10:45:00'),
    ('Daniela da Conceição', '21877312274', 34107, '54245762167', NULL, '12:30:00', '16:30:00'),
    ('Raul das Neves', '45362710400', 82995, '13104272130', 'stephany36@gmail.com', '13:15:00', '18:15:00'),
    ('Isabelly Ribeiro', '74345932530', 32935, '38873494167', 'ebarbosa@bol.com.br', '11:45:00', '13:45:00'),
    ('Sr. Felipe Alves', '19266145858', 18878, '78734906746', 'daniloda-rocha@pires.net', '13:30:00', '14:30:00'),
    ('Enzo Ribeiro', '04996130318', 19659, '24549141252', NULL, '17:00:00', '22:00:00'),
    ('Dra. Esther Barros', '62509227416', 88912, '50665090930', 'portocalebe@da.org', '06:00:00', '12:00:00'),
    ('Nicole Porto', '98957590102', 88616, '48171442678', 'lda-mata@gmail.com', '09:30:00', '11:30:00'),
    ('Pedro Dias', '32183751690', 99775, '68235662976', 'zmartins@hotmail.com', '15:30:00', '21:30:00'),
    ('Anthony Cavalcanti', '77548063202', 57480, '53646007796', 'ribeirojoao-lucas@ig.com.br', '13:15:00', '16:15:00');

INSERT INTO appointment (patient_id, doctor_id, date_time) VALUES

    (52, 8, '2025-07-05 14:11:41'),
    (23, 10, '2025-07-06 10:26:41'),
    (9, 41, '2025-06-01 06:56:41'),
    (7, 31, '2025-07-04 13:11:41'),
    (47, 20, '2025-06-25 08:11:41'),
    (53, 39, '2025-07-27 15:56:41'),
    (8, 23, '2025-06-24 10:26:41'),
    (46, 42, '2025-06-09 13:11:41'),
    (6, 49, '2025-06-11 14:26:41'),
    (19, 4, '2025-07-25 15:11:41'),
    (22, 42, '2025-07-11 15:11:41'),
    (30, 45, '2025-07-25 08:41:41'),
    (24, 4, '2025-07-05 14:11:41'),
    (18, 12, '2025-05-30 16:11:41'),
    (49, 15, '2025-06-10 14:11:41'),
    (12, 36, '2025-07-14 12:11:41'),
    (47, 51, '2025-07-12 07:26:41'),
    (16, 20, '2025-06-04 10:56:41'),
    (43, 30, '2025-07-11 09:56:41'),
    (14, 41, '2025-07-26 13:11:41'),
    (42, 16, '2025-07-17 07:11:41'),
    (26, 33, '2025-06-14 09:41:41'),
    (22, 36, '2025-06-03 10:56:41'),
    (31, 27, '2025-06-28 12:56:41'),
    (30, 7, '2025-06-07 06:56:41'),
    (40, 33, '2025-06-13 07:26:41'),
    (21, 35, '2025-06-15 07:26:41'),
    (34, 2, '2025-07-23 11:11:41'),
    (25, 45, '2025-07-15 10:26:41'),
    (32, 30, '2025-06-03 11:11:41'),
    (15, 25, '2025-07-11 13:56:41'),
    (22, 51, '2025-07-10 13:26:41'),
    (19, 9, '2025-07-09 09:41:41'),
    (10, 13, '2025-06-24 14:11:41'),
    (50, 37, '2025-06-02 12:56:41'),
    (44, 12, '2025-06-22 06:26:41'),
    (53, 11, '2025-06-20 07:26:41'),
    (33, 38, '2025-06-27 07:41:41'),
    (53, 19, '2025-06-06 15:41:41'),
    (26, 33, '2025-07-17 10:11:41'),
    (17, 4, '2025-06-12 13:11:41'),
    (55, 9, '2025-07-24 12:56:41'),
    (29, 25, '2025-06-27 09:56:41'),
    (29, 14, '2025-06-01 11:11:41'),
    (35, 17, '2025-07-12 09:26:41'),
    (41, 39, '2025-06-06 15:11:41'),
    (41, 7, '2025-06-07 08:11:41'),
    (11, 14, '2025-06-29 14:11:41'),
    (19, 20, '2025-07-25 11:41:41'),
    (49, 20, '2025-06-04 12:41:41');

INSERT INTO user_system (email, password, permission_tier) VALUES

    ('joao-guilherme61@gmail.com', 'IeE0PogupfD3', 1),
    ('enzo-gabriel65@bol.com.br', '8n8aDwEscB2Q', 2),
    ('lucca12@das.com', '575PF1yqf9Zq', 3),
    ('vitoria88@araujo.net', 'HozCOog22Lnv', 3),
    ('das-nevesluiz-miguel@gmail.com', 'A5uc4TRc7NKL', 2),
    ('limamaria-fernanda@oliveira.br', '9ZZLPc43N59j', 3),
    ('gabriellymoraes@fogaca.com', 'yhYMQylqW6Qt', 3),
    ('fernandocarvalho@cunha.com', 'Ol2FHpesKsln', 3),
    ('diogo55@farias.com', 'rO0EQUfq3xoO', 1),
    ('luiz-otavio27@da.com', 'igvlG9g4U78V', 2),
    ('cmonteiro@uol.com.br', 'yKSJXxnqJ96X', 2),
    ('antonioda-rocha@cunha.org', 'E7oPgc42p0MK', 1),
    ('lunamendes@bol.com.br', 'IfhRPcwG7KI9', 3),
    ('vitormendes@silveira.br', 'K1ltDOrJMks1', 3),
    ('rafaelacardoso@ig.com.br', '3kWCwI0SO7As', 3),
    ('camilagomes@nascimento.br', '98YgNn1VG4X2', 1),
    ('felipe68@dias.com', '8ZKH1PciSUAO', 3),
    ('amanda64@ig.com.br', 'g22Fe6UaZNmb', 1),
    ('maiteramos@yahoo.com.br', 'uZKuxo9RQ4yl', 3),
    ('clarice67@ig.com.br', 'i3J7tP8UOxly', 3),
    ('dsantos@yahoo.com.br', '8XCXpCGopDMj', 3),
    ('correiamelissa@freitas.br', '54j7qqwfHaJu', 1),
    ('renan51@bol.com.br', 'X0IgrSnnm2Mt', 1),
    ('vicentedas-neves@hotmail.com', 'f3oYpExyfJ7L', 2),
    ('lbarbosa@da.com', '1DI2vnXIYnEw', 1),
    ('qda-rocha@ig.com.br', 'HxE9xX7rKY95', 2),
    ('yagopereira@yahoo.com.br', 'i8B6B0fbEucV', 1),
    ('bsilva@novaes.org', '50q7CeVUBPzs', 3),
    ('lnunes@almeida.org', 'k1Qt2X2zy5HB', 2),
    ('pmoura@fogaca.net', 'mtz2DvzeJITz', 1),
    ('moreirabianca@cardoso.br', '29Jv1tiENP2Y', 1),
    ('peixotodavi-lucas@rocha.br', 'yX7UvhbDFArR', 3),
    ('ncaldeira@uol.com.br', 'Hf0bwWbe4osx', 2),
    ('dcampos@silva.br', 'aVn8XVc3529q', 3),
    ('umoraes@aragao.com', 'q0E5vAlyuneu', 2),
    ('ana86@uol.com.br', 'wnOyFlyUY8pF', 2),
    ('lais99@hotmail.com', '13TlzxtSOS4N', 3),
    ('rodriguesmaria-fernanda@bol.com.br', 'xDBJ6aceE8ZM', 3),
    ('thiago64@correia.br', 'YLzrCo2L3ZS4', 2),
    ('enzodas-neves@uol.com.br', 'qIWtkqkx57nE', 2),
    ('brenomoura@uol.com.br', 'hoJByIVxt2aH', 3),
    ('yfarias@bol.com.br', '9RuRABgf1Ytm', 1),
    ('nathan35@bol.com.br', 'aMUXYyeI0wGz', 2),
    ('agathacosta@bol.com.br', '9eTiilWR45B6', 3),
    ('meloerick@bol.com.br', 'F8zHsVjv8WkT', 2),
    ('yurilima@ig.com.br', 'JUx5dRYh68fc', 3),
    ('yporto@gmail.com', '1WDn8FJo59yL', 3),
    ('ramoscaue@rezende.com', '62AAKGz3DREL', 3),
    ('irodrigues@bol.com.br', '61EUJMiIjq1U', 1),
    ('jesusfrancisco@ig.com.br', '2jApXuBlGALY', 1);