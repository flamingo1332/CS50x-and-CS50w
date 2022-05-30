--유일한 정보
-- july 28th
-- chamberlin street

-- 1. who the theif is,
-- 2. where the theif escaped to,
-- 3. who the thief's accomplice was who helped them escape town


-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports WHERE month = 7 AND year = 2021 AND day = 28 AND street = "Humphrey Street";

Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time –
each of their interview transcripts mentions the bakery. |

3 interviews


SELECT * FROM interviews WHERE month = 7 AND year = 2021 AND day = 28 AND transcript LIKE "%bakery%" ;

| 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
| 193 | Emma    | 2021 | 7     | 28  | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.
ruth -- theif get into a car in the bakery parking lot -- security footage 10:15 ~ 10:25am
engene -- recognized the thief, ATM on leggett street withdrawing some money
Raymond -- earlist flight out of fiftyville tommorow(7/29)
emma -- bakery owner, saw someone whispering into a phone for 30 min



-- ruth : security footage of bakery parking lot
SELECT * FROM bakery_security_logs WHERE hour = 10 AND month = 7 AND day = 28 AND year = 2021;
| id  | year | month | day | hour | minute | activity | license_plate |
| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
| 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58       |

SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE hour = 10 AND month = 7 AND day = 28 AND year = 2021 AND activity = "exit");
+--------+---------+----------------+-----------------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate |
+--------+---------+----------------+-----------------+---------------+
-- | 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
-- | 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
-- | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+---------+----------------+-----------------+---------------+



-- eugene : ATM leggett street morning 7/28 withdraw
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
246 | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 288 | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35

+--------+---------+----------------+-----------------+---------------+----------------+-----------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate | account_number | person_id | creation_year |
+--------+---------+----------------+-----------------+---------------+----------------+-----------+---------------+
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 49610011       | 686048    | 2010          |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | 26013199       | 514354    | 2012          |
-- | 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       | 16153065       | 458378    | 2012          |
-- | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | 28296815       | 395717    | 2014          |
-- | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | 25506511       | 396669    | 2014          |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | 28500762       | 467400    | 2014          |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | 76054385       | 449774    | 2015          |
-- | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       | 81061156       | 438727    | 2018          |
+--------+---------+----------------+-----------------+---------------+----------------+-----------+---------------+



--raymond : earliest flight out of 50ville next morning(7/29) and purchase ticket on (7/28) leaving the bakery, phonecall less than a min
SELECT * FROM airports WHERE city = "Fiftyville";
 +----+--------------+-----------------------------+------------+
| id | abbreviation |          full_name          |    city    |
+----+--------------+-----------------------------+------------+
| 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
+----+--------------+-----------------------------+------------+

SELECT * FROM flights WHERE month = 7 AND day = 29 AND origin_airport_id = 8;
 id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     |
--  43 | 8                 | 1                      | 2021 | 7     | 29  | 9    | 30     |

SELECT * FROM airports WHERE id = 4;
+----+--------------+-------------------+---------------+
| id | abbreviation |     full_name     |     city      |
+----+--------------+-------------------+---------------+
| 4  | LGA          | LaGuardia Airport | New York City |
+----+--------------+-------------------+---------------+

SELECT * FROM passengers WHERE flight_id = 36 OR flight_id = 43;
+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 7214083635      | 2A   |
| 36        | 1695452385      | 3B   |
| 36        | 5773159633      | 4A   |
| 36        | 1540955065      | 5C   |
| 36        | 8294398571      | 6C   |
| 36        | 1988161715      | 6D   |
| 36        | 9878712108      | 7A   |
| 36        | 8496433585      | 7B   |
-- | 43        | 7597790505      | 7B   |
-- | 43        | 6128131458      | 8A   |
-- | 43        | 6264773605      | 9A   |
-- | 43        | 3642612721      | 2C   |
-- | 43        | 4356447308      | 3B   |
-- | 43        | 7441135547      | 4A   |
+-----------+-----------------+------+

SELECT * FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE people.passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36 OR flight_id = 43) ORDER BY flight_id;
+--------+---------+----------------+-----------------+---------------+-----------+-----------------+------+
|   id   |  name   |  phone_number  | passport_number | license_plate | flight_id | passport_number | seat |
+--------+---------+----------------+-----------------+---------------+-----------+-----------------+------+
-- | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | 36        | 9878712108      | 7A   |
-- | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       | 36        | 1695452385      | 3B   |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | 36        | 1988161715      | 6D   |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | 36        | 8496433585      | 7B   |
-- | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       | 36        | 8294398571      | 6C   |
-- | 651714 | Edward  | (328) 555-1152 | 1540955065      | 130LD9Z       | 36        | 1540955065      | 5C   |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 36        | 5773159633      | 4A   |
-- | 953679 | Doris   | (066) 555-9701 | 7214083635      | M51FA04       | 36        | 7214083635      | 2A   |
-- | 210641 | Heather | (502) 555-6712 | 4356447308      |               | 43        | 4356447308      | 3B   |
-- | 341739 | Rebecca | (891) 555-5672 | 6264773605      |               | 43        | 6264773605      | 9A   |
-- | 354903 | Marilyn | (568) 555-3190 | 7441135547      | 0R0FW39       | 43        | 7441135547      | 4A   |
-- | 423393 | Carol   | (168) 555-6126 | 6128131458      | 81MNC9R       | 43        | 6128131458      | 8A   |
-- | 745650 | Sophia  | (027) 555-1068 | 3642612721      | 13FNH73       | 43        | 3642612721      | 2C   |
-- | 750165 | Daniel  | (971) 555-6468 | 7597790505      | FLFN3W0       | 43        | 7597790505      | 7B   |
+--------+---------+----------------+-----------------+---------------+-----------+-----------------+------+





-- phonecall less than a minute
SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND duration <60;
+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
| 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
| 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
| 261 | (031) 555-6622 | (910) 555-3251 | 2021 | 7     | 28  | 38       |
| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
| 281 | (338) 555-6650 | (704) 555-2131 | 2021 | 7     | 28  | 54       |
+-----+----------------+----------------+------+-------+-----+----------+
SELECT * FROM people JOIN phone_calls ON phone_number = caller WHERE phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration <60) ORDER BY duration;
+--------+---------+----------------+-----------------+---------------+-----+----------------+----------------+------+-------+-----+----------+
|   id   |  name   |  phone_number  | passport_number | license_plate | id  |     caller     |    receiver    | year | month | day | duration |
+--------+---------+----------------+-----------------+---------------+-----+----------------+----------------+------+-------+-----+----------+
-- | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 395 | (367) 555-5533 | (455) 555-5315 | 2021 | 7     | 30  | 31       |
-- | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       | 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
-- | 907148 | Carina  | (031) 555-6622 | 9628244268      | Q12B3Z3       | 261 | (031) 555-6622 | (910) 555-3251 | 2021 | 7     | 28  | 38       |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
-- | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       | 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
-- | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       | 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
-- | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       | 281 | (338) 555-6650 | (704) 555-2131 | 2021 | 7     | 28  | 54       |
-- | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |


-- the accomplice (receiver's name)
SELECT * FROM people WHERE phone_number = "(375) 555-8161";
+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 |                 | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+



-- emma : saw someone whispering to a phone for 30min, never bought anything
| id  |     caller     |    receiver    | year | month | day | duration |
| 103 | (869) 555-6696 | (971) 555-2231 | 2021 | 7     | 26  | 600      |
| 172 | (994) 555-3373 | (328) 555-9658 | 2021 | 7     | 27  | 600      |
| 381 | (006) 555-0505 | (666) 555-5774 | 2021 | 7     | 30  | 600      |
+-----+----------------+----------------+------+-------+-----+----------+