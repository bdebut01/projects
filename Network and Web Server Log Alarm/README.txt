Depending on command line argument, alarm either parses the passed web server log or analyzes live network streams.

Live stream detection:
NULL scans, XMAS scans, leaked credit card numbers (Mastercard, Visa, Discover, and Express)

Web server log detection:
Nmap scans, http errors (there are a lot of these, I'd typically leave this print statement commented out so as to not over-trigger), and any discovered shellcode.