drop table if exists bookingfee;
drop table if exists booking;
drop table if exists vehicles;
drop table if exists client;
drop table if exists company;


CREATE TABLE client(
first_name varchar(225),
last_name varchar(225),
DOB DATE,    /* format YYYY-MM-DD */
email varchar(225),
password varchar(225),
PRIMARY KEY (email)
);

CREATE TABLE company(
name varchar(225),
city varchar(225),
st varchar(225),   /*state */
ISIN varchar(225),
password varchar(225),
PRIMARY KEY (ISIN)
);

CREATE TABLE vehicles(
v_id varchar(15),
ISIN varchar(225),
brand varchar(225),
model varchar(225),
year YEAR,          /*yyyy */
price numeric(10, 2),
C BOOLEAN,
seat_num int,
load_capacity int,
PRIMARY KEY (v_id)
);

CREATE TABLE booking(
client_email varchar(225),
booking_id int AUTO_INCREMENT,
start_date DATE,
end_date DATE,
v_id varchar(15),
PRIMARY KEY (booking_id)
);

CREATE TABLE bookingfee(
booking_id int AUTO_INCREMENT,
amount_fee numeric(10, 2),
PRIMARY KEY (booking_id)
);

/* FOREIGN key */ 

ALTER TABLE `booking` ADD FOREIGN KEY (`client_email`) REFERENCES `client`(`email`) ON DELETE CASCADE ON UPDATE CASCADE; 
ALTER TABLE `booking` ADD FOREIGN KEY (`v_id`) REFERENCES `vehicles`(`v_id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `vehicles` ADD FOREIGN KEY (`ISIN`) REFERENCES `company`(`ISIN`) ON DELETE CASCADE ON UPDATE CASCADE;



INSERT INTO client VALUES ('Jasper', 'Wang','1999-03-01', '2942@qq.com','2942');
INSERT INTO client VALUES ('Pelli', 'Roi', '1964-01-01', '4539583@qq.com', 'xs34');
INSERT INTO client VALUES ('Jame', 'Wang','1994-03-01', '29423@qq.com','294e2');
INSERT INTO client VALUES ('Bob', 'Wang','1989-03-01', '29425@qq.com','29432');
INSERT INTO client VALUES ('Jang', 'Huang','1979-03-01', '29426@qq.com','29422');

INSERT INTO company VALUES ('Fast Company', 'Canberra','Australia Capital Territory', 'XM37492','w2942');
INSERT INTO company VALUES ('First Company', 'Sydney','New South Wales', 'XM37493','w2943');
INSERT INTO company VALUES ('Nice Company', 'Brisbane','Queensland', 'XM37494','w2944');
INSERT INTO company VALUES ('Safe Company', 'Perth','Western Australia', 'XM37495','w2945');
INSERT INTO company VALUES ('Forever Company', 'Melbourne','Victoria', 'XM37496','w2946');

INSERT INTO vehicles VALUES ('XT080', 'XM37493', 'TOYOTA', 'GTM7240G','2012', 260.00, 1, 5, NULL);
INSERT INTO vehicles VALUES ('XT070', 'XM37493', 'Volkswagen', 'Touareg','2016', 280.00, 1, 5, NULL);
INSERT INTO vehicles VALUES ('XT060', 'XM37495', 'TOYOTA', 'GTM7240G','2010', 230.00, 1, 5, NULL);
INSERT INTO vehicles VALUES ('XT050', 'XM37495', 'TOYOTA', 'Tundra','2014', 280.00, 0, NULL, 714);
INSERT INTO vehicles VALUES ('XT040', 'XM37495', 'Chevrolet', 'SILVERADO','2012', 240.00, 0, NULL, 540);


INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES ('2942@qq.com', '2022-07-01', '2022-07-03', 'XT080');
INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES ('2942@qq.com', '2022-07-04', '2022-07-06', 'XT080');
INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES ('29426@qq.com', '2022-06-01', '2022-06-03', 'XT070');
INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES ('29426@qq.com', '2022-06-01', '2022-06-03', 'XT060');
INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES ('29426@qq.com', '2022-06-01', '2022-06-03', 'XT050');

INSERT INTO bookingfee(amount_fee) VALUES (520.00);
INSERT INTO bookingfee(amount_fee) VALUES (520.00);
INSERT INTO bookingfee(amount_fee) VALUES (560.00);
INSERT INTO bookingfee(amount_fee) VALUES (460.00);
INSERT INTO bookingfee(amount_fee) VALUES (560.00);
