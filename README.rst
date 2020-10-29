==================
This converter converts raw text to gift-formatted test questions which can be imported into moodle. The application can be run on a server and will be published on port 6123.

At this point, only multiple-choice questions are supported.

Syntax:

first raw is always the question, the next rows are the possible answers. The right answers are labeled with # at the beginning of the line.

The questions are separated with empty lines

Example:

Which of the following numbers are prime numbers?
#3
4
12
#17


Which of the following numbers are not prime numbers?
3
#4
#12
17
