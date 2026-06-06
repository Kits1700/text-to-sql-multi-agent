# Evaluation Log
**10 passed / 0 failed out of 10 tests**
---
## Test 1 [EN] — PASS
**Question:** How many heads of departments are older than 56?  
**Database:** department_management  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT COUNT(DISTINCT T2.head_ID) AS head_count
FROM department AS T1
JOIN management AS T3 ON T1.Department_ID = T3.department_ID
JOIN head AS T2 ON T3.head_ID = T2.head_ID
WHERE T2.age > 56;
```
### Result
Columns: ['head_count']  
- [3]

---
## Test 2 [CS] — PASS
**Question:** Kolik vedoucích oddělení je starších než 56 let?  
**Database:** department_management  

### Attempts
**Attempt 1 — Local (Ollama) — ✗ FAIL**
```sql
SELECT COUNT(DISTINCT d.Department_ID) AS "Vedoucí oddělení"
FROM department d
WHERE d.Age < 56;
```
> Error: `no such column: d.Age`

**Attempt 2 — Local (Ollama) — ✗ FAIL**
```sql
SELECT COUNT(DISTINCT d.Department_ID) AS "Vedoucí oddělení"
FROM department d
WHERE d.age < 56;
```
> Error: `no such column: d.age`

**Attempt 3 — Local (Ollama) — ✗ FAIL**
```sql
SELECT COUNT(DISTINCT h.Department_ID) AS "Vedoucí oddělení"
FROM head h
WHERE h.age < 56;
```
> Error: `no such column: h.Department_ID`

**Attempt 4 — Claude API — ✓ OK**
```sql
SELECT COUNT(*) 
FROM head h
JOIN management m ON h.head_ID = m.head_ID
WHERE h.age > 56;
```
### Result
Columns: ['COUNT(*)']  
- [3]

---
## Test 3 [EN] — PASS
**Question:** List the creation year, name, and budget of each department.  
**Database:** department_management  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT Creation, Name, Budget_in_Billions FROM department;
```
### Result
Columns: ['Creation', 'Name', 'Budget_in_Billions']  
- ['1789', 'State', 9.96]
- ['1789', 'Treasury', 11.1]
- ['1947', 'Defense', 439.3]
- ['1870', 'Justice', 23.4]
- ['1849', 'Interior', 10.7]
- ['1889', 'Agriculture', 77.6]
- ['1903', 'Commerce', 6.2]
- ['1913', 'Labor', 59.7]
- ['1953', 'Health and Human Services', 543.2]
- ['1965', 'Housing and Urban Development', 46.2]
- ['1966', 'Transportation', 58.0]
- ['1977', 'Energy', 21.5]
- ['1979', 'Education', 62.8]
- ['1989', 'Veterans Affairs', 73.2]
- ['2002', 'Homeland Security', 44.6]

---
## Test 4 [CS] — PASS
**Question:** Vypiš rok založení, název a rozpočet každého oddělení.  
**Database:** department_management  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT Creation, Name, Budget_in_Billions FROM department;
```
### Result
Columns: ['Creation', 'Name', 'Budget_in_Billions']  
- ['1789', 'State', 9.96]
- ['1789', 'Treasury', 11.1]
- ['1947', 'Defense', 439.3]
- ['1870', 'Justice', 23.4]
- ['1849', 'Interior', 10.7]
- ['1889', 'Agriculture', 77.6]
- ['1903', 'Commerce', 6.2]
- ['1913', 'Labor', 59.7]
- ['1953', 'Health and Human Services', 543.2]
- ['1965', 'Housing and Urban Development', 46.2]
- ['1966', 'Transportation', 58.0]
- ['1977', 'Energy', 21.5]
- ['1979', 'Education', 62.8]
- ['1989', 'Veterans Affairs', 73.2]
- ['2002', 'Homeland Security', 44.6]

---
## Test 5 [EN] — PASS
**Question:** Show the name and head ID of the heads who are managing a department.  
**Database:** department_management  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT T2.name, T2.head_ID FROM management AS T1 JOIN head AS T2 ON T1.head_ID = T2.head_ID WHERE T1.department_ID IS NOT NULL;
```
### Result
Columns: ['name', 'head_ID']  
- ['Jeff Maggert', 5]
- ['Billy Mayfair', 6]
- ['K. J. Choi', 3]
- ['Franklin Langham', 10]
- ['Dudley Hart', 4]

---
## Test 6 [CS] — PASS
**Question:** Ukaž jméno a ID vedoucího (head ID) u těch vedoucích, kteří aktuálně řídí nějaké oddělení.  
**Database:** concert_singer  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT Singer_ID AS head_id, Name FROM singer WHERE Singer_ID IN (
    SELECT Singer_ID FROM singer_in_concert
);
```
### Result
Columns: ['head_id', 'Name']  
- [2, 'Timbaland']
- [3, 'Justin Brown']
- [4, 'Rose White']
- [5, 'John Nizinik']
- [6, 'Tribal King']

---
## Test 7 [EN] — PASS
**Question:** What is the total capacity of all stadiums combined?  
**Database:** concert_singer  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT SUM(stadium.Capacity) 
FROM stadium;
```
### Result
Columns: ['SUM(stadium.Capacity)']  
- [95595]

---
## Test 8 [CS] — PASS
**Question:** Jaká je celková kapacita všech stadionů dohromady?  
**Database:** concert_singer  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT SUM(capacity) 
FROM stadium;
```
### Result
Columns: ['SUM(capacity)']  
- [95595]

---
## Test 9 [EN] — PASS
**Question:** Show the names of singers and the themes of concerts they sang in.  
**Database:** concert_singer  

### Attempts
**Attempt 1 — Local (Ollama) — ✓ OK**
```sql
SELECT s.Name, c.Theme FROM singer_in_concert sc JOIN concert c ON sc.concert_ID = c.concert_ID JOIN singer s ON sc.Singer_ID = s.Singer_ID;
```
### Result
Columns: ['Name', 'Theme']  
- ['Timbaland', 'Free choice']
- ['Justin Brown', 'Free choice']
- ['John Nizinik', 'Free choice']
- ['Justin Brown', 'Free choice 2']
- ['Tribal King', 'Free choice 2']
- ['John Nizinik', 'Bleeding Love']
- ['Rose White', 'Wide Awake']
- ['Tribal King', 'Happy Tonight']
- ['Justin Brown', 'Happy Tonight']
- ['Timbaland', 'Party All Night']

---
## Test 10 [CS] — PASS
**Question:** Ukaž jména zpěváků a témata koncertů, na kterých zpívali.  
**Database:** concert_singer  

### Attempts
**Attempt 1 — Local (Ollama) — ✗ FAIL**
```sql
SELECT DISTINCT Singer.Name, Theme
FROM singer AS S
JOIN singer_in_concert AS Sc ON S.Singer_ID = Sc.Singer_ID
JOIN concert AS C ON Sc.concert_ID = C.concert_ID
WHERE S.Age > 0;
```
> Error: `no such column: Singer.Name`

**Attempt 2 — Local (Ollama) — ✗ FAIL**
```sql
SELECT DISTINCT Singer.Name, Theme 
FROM singer AS S
JOIN singer_in_concert AS Sc ON S.Singer_ID = Sc.Singer_ID
JOIN concert AS C ON Sc.concert_ID = C.concert_ID
WHERE S.Age > 0;
```
> Error: `no such column: Singer.Name`

**Attempt 3 — Local (Ollama) — ✓ OK**
```sql
SELECT DISTINCT s.Name, c.Theme 
FROM singer AS s 
JOIN singer_in_concert AS sc ON s.Singer_ID = sc.Singer_ID 
JOIN concert AS c ON sc.concert_ID = c.concert_ID;
```
### Result
Columns: ['Name', 'Theme']  
- ['Timbaland', 'Free choice']
- ['Justin Brown', 'Free choice']
- ['John Nizinik', 'Free choice']
- ['Justin Brown', 'Free choice 2']
- ['Tribal King', 'Free choice 2']
- ['John Nizinik', 'Bleeding Love']
- ['Rose White', 'Wide Awake']
- ['Tribal King', 'Happy Tonight']
- ['Justin Brown', 'Happy Tonight']
- ['Timbaland', 'Party All Night']

