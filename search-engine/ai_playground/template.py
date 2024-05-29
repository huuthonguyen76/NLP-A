from langchain_core.prompts import ChatPromptTemplate
 
from langchain_core.prompts import  SystemMessagePromptTemplate, AIMessagePromptTemplate,HumanMessagePromptTemplate


sql_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template( "You're expert in biology research have many years experience."),
    HumanMessagePromptTemplate.from_template(template="""
Given a 【Database schema】 description and the 【Question】, you need to use valid SQL and understand the database and knowledge, and then decompose the question into subquestions for text-to-SQL generation.
When generating SQL, we should always consider constraints:
【Constraints】
- In `SELECT "patient_id", "demographic-age-age", "demographic-gender-gender", "physiology-bmi-bmi", "race_maternal"`, just select all the columns in the data schema.
- In `FROM <table>` or `JOIN <table>`, do not include unnecessary table
- If use max or min func, `JOIN <table>` FIRST, THEN use `SELECT MAX(<column>)` or `SELECT MIN(<column>)`
- If [Value examples] of <column> has 'None' or None, use `JOIN <table>` or `WHERE <column> is NOT NULL` is better. The <column> should be wrapped into "<column".
- If use `ORDER BY <column> ASC|DESC`, add `GROUP BY <column>` before to select distinct values

==========
【Database schema】
# Table: observation
[
  (patient_id, Patient ID. Value examples: [None, 1, 2, 3].),
  (demographic-age-age, Age of Patient. Value examples: [None, 55, 67, 45].),
  (demographic-gender-gender, Gender of Patient. Value examples: [None, Male, Female, Prefer not to say].),
  (physiology-bmi-bmi, Gender of Patient. Value examples: [None, Male, Female, Prefer not to say].),
  (race_maternal, Patient human race. All of its value: [Ceylonese, Filipino, European, Javanese, Indian, Brazilian, Viet Nam, European / Dutch, French, Iban, Indian Chinese, Thai, Burmese, Caucasion, Korean, Punjabi, British, Russian, Russian Jew, Sikh, caucasian, Malay, vietnamese, Chinese, Mongolian, japanese, Indonesian, Arab, Pakistani, Portguese, Chinese, Peranakan, Caucasian Australian, English, Sinhalese, Japan, Batak, Kyrgyz (Kyrgyzstan), Indonesian-Malay, Turkish, Scandinavian, Malaylee, White European, Japanese, Pakistan, Guyanese, Portuguese, Chinese, White, Caucasian, Australian, Singhalese, Caucasian (North American), CAUCASIAN, Italian, polish, White (European), South Asian (non-Indian), Europe, Vietnamese, Finnish, Myanmar, Viet Name, South African, Eurasian, Austrian, 3/4 chinese 1/4 portuguese])
]
【Question】
Give me a list of the patient with age more than 55, should be Male and age < 45 gender Female

Decompose the question into sub questions, considering 【Constraints】, and generate the SQL after thinking step by step:
Sub question 1: Get the list of patients with age more than 55 and gender be Male
SQL
```sql
SELECT "patient_id", "demographic-age-age", "demographic-gender-gender", "physiology-bmi-bmi", "race_maternal"
	FROM public.observation where "demographic-age-age" > 55 and "demographic-gender-gender" = 'Male';
```

Sub question 2: List of patients age < 45 gender Female
SQL
```sql
SELECT "patient_id", "demographic-age-age", "demographic-gender-gender", "physiology-bmi-bmi", "race_maternal"
	FROM public.observation where "demographic-age-age" < 45 and "demographic-gender-gender" = 'Female';
```

Sub question 3: Give me a list of the patient with age more than 55, should be Male and age < 45 gender Female
SQL
```sql
SELECT "patient_id", "demographic-age-age", "demographic-gender-gender", "physiology-bmi-bmi", "race_maternal"
	FROM public.observation where ("demographic-age-age" < 45 and "demographic-gender-gender" = 'Female') or ("demographic-age-age" > 55 and "demographic-gender-gender" = 'Male');
```

Question Solved.

==========

【Question】
{query}

{special_instruction}

Decompose the question into sub questions, considering 【Constraints】, and generate the SQL after thinking step by step:


""")
])


refiner_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template( "You're expert in biology research have many years experience."),
    HumanMessagePromptTemplate.from_template(template="""【Instruction】
When executing SQL below, some errors occurred, please fix up SQL based on query and database info.
Solve the task step by step if you need to. Using SQL format in the code block, and indicate script type in the code block.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
【Constraints】
- In `SELECT "patient_id", "demographic-age-age", "demographic-gender-gender", "physiology-bmi-bmi", "race_maternal"`, just select all the columns in the data info.
- In `FROM <table>` or `JOIN <table>`, do not include unnecessary table
- If use max or min func, `JOIN <table>` FIRST, THEN use `SELECT MAX(<column>)` or `SELECT MIN(<column>)`
- If [Value examples] of <column> has 'None' or None, use `JOIN <table>` or `WHERE <column> is NOT NULL` is better
- If use `ORDER BY <column> ASC|DESC`, add `GROUP BY <column>` before to select distinct values
【Query】
-- {query}
{special_instruction}
【Database info】
# Table: observation
[
  (patient_id, Patient ID. Value examples: [None, 1, 2, 3].),
  (demographic-age-age, Age of Patient. Value examples: [None, 55, 67, 45].),
  (demographic-gender-gender, Gender of Patient. Value examples: [None, Male, Female, Prefer not to say].),
  (physiology-bmi-bmi, Gender of Patient. Value examples: [None, Male, Female, Prefer not to say].),
  (race_maternal, Patient human race. All of its value: [Ceylonese, Filipino, European, Javanese, Indian, Brazilian, Viet Nam, European / Dutch, French, Iban, Indian Chinese, Thai, Burmese, Caucasion, Korean, Punjabi, British, Russian, Russian Jew, Sikh, caucasian, Malay, vietnamese, Chinese, Mongolian, japanese, Indonesian, Arab, Pakistani, Portguese, Chinese, Peranakan, Caucasian Australian, English, Sinhalese, Japan, Batak, Kyrgyz (Kyrgyzstan), Indonesian-Malay, Turkish, Scandinavian, Malaylee, White European, Japanese, Pakistan, Guyanese, Portuguese, Chinese, White, Caucasian, Australian, Singhalese, Caucasian (North American), CAUCASIAN, Italian, polish, White (European), South Asian (non-Indian), Europe, Vietnamese, Finnish, Myanmar, Viet Name, South African, Eurasian, Austrian, 3/4 chinese 1/4 portuguese])
]
【old SQL】
```sql
{sql}
```
【SQL error】 
{sql_error}
Now please fixup old SQL and generate new SQL again.
【correct SQL】

""")
])
