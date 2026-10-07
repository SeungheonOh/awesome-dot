# Report received for the synthetic fixture

Report ID: SAVE-17. Component revision: controller-fixture-1. Environment:
dependency-free Python fixture with manually released save callbacks.

Reporter statement: "I began at title Base and limit 5. I changed title to Nova,
clicked Save title, changed limit to 0, and clicked Save limit. The limit save
finished first. Then the title save finished and I saw 'Saved title: Nova'.
I think my limit reverted to 5 because the last message only mentioned title."

Supplied artifact: a status-message capture transcribed as "Saved title: Nova".
No persisted-record read, limit-field capture, or production logs accompany the
report. The reporter's data-loss interpretation is a hypothesis. The fixture
and contract are the only permitted experiment environment and requirements.
