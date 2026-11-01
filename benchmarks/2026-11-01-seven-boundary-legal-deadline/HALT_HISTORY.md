# Preserved initial halt

The earlier setup used paths beginning deadline_candidate/ while the process was already in that directory. Both file-creation commands failed with No such file or directory. The two attempted demo commands could not open demo.py. The initial test log recorded one import error: ModuleNotFoundError: No module named 'test_demo'. The enclosing shell exited zero only because its final cat succeeded. No replay result existed in that attempt. The original local logs and original contract remain preserved outside this public candidate; this is a summary of their contents with local system paths omitted.

The present attempt uses a separate candidate and creates files in the correct directory. Actual individual process statuses are recorded in run1.log, run2.log and test.log. It retains the frozen contract and input unchanged.
