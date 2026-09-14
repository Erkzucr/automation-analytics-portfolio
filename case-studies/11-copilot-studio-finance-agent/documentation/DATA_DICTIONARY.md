# Data Dictionary

Fields in the evaluation input and output files. All content is synthetic.

## evaluation/test_conversations.csv

| Field | Meaning | Example |
|---|---|---|
| case_id | Test case identifier | C01 |
| user_message | The synthetic message sent to the agent | Who approves a journal entry of 50000? |
| expected_topic | Topic the message should route to | T01 |

## expected-output/routing_results.csv

| Field | Meaning | Example |
|---|---|---|
| case_id | Test case identifier | C01 |
| expected_topic | Topic from the test set | T01 |
| actual_topic | Topic the router selected | T01 |
| matched_trigger | Trigger phrase that fired, if any | journal entry |
| passed | Whether expected and actual agree | True |

## expected-output/evaluation_summary.csv

| Field | Meaning |
|---|---|
| control_name | Name of the check |
| control_value | Result of the check |

## sample-data/knowledge-base/faq.csv

| Field | Meaning |
|---|---|
| question | Common question in plain language |
| answer | Approved answer |
| source | SOP and section the answer comes from |
