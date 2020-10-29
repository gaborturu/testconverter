
import streamlit as st
from streamlit_ace import st_ace
import json
import re

content = st_ace(
                placeholder = "put your questions here",
                language = "plain_text",
                theme = "iplastic",
                font_size = 12,
                show_gutter = True,
                show_print_margin = False,
                wrap = True,
                auto_update= True,
                key="ace-editor"

 )


def getQuestionsFromText(txt):
    """Splits the text into question blocks"""
    txt = txt[1:-1] # remove extra " - characters from json conversion
    qs = txt.split('\\n\\n')
    qs = [x for x in qs if len(x) > 4]

    return qs

def cleanQuestion(question):
    """drop all lines with no letters or numbers and return question and answers separately"""
    try:
        lines = question.split('\\n')
        lines = [l for l in lines if len("".join(re.findall('\w*', l)))>0] # drop all lines with no letters or numbers
        q = lines[0]
        answers = lines[1:]

        return q, answers
    except:
        placeholder.text(f"oh, shit happend\n{question}")

def prepareQuestions(question, name, tag):
    """prepares questions into GIFT format"""

    q, answers = cleanQuestion(question)

    rights = [True for a in answers if a[0] == "#"]
    if not any(rights):
        placeholder.text(f"""no right answers, please label the right answers with #\n\nWrong question:\n\n{question}""")
        return None
    else:
        score = str(100 / question.count('#'))

        if len(score) > 8:
            score = score[:8]
        else:
            score = score.split('.')[0]

        answertxt = ""

        for a in answers:
            if a[0] == "#":
                answertxt += f"""\t~%{score}%<p>{a.replace('#', '')}<br></p>\n"""
            else:
                answertxt += f"""\t~%-{score}%<p>{a}<br></p>\n"""

        questionbody = f"""// name: {name}\n// [tag:{tag}]\n::{name}::[html]<p>\\n{q}<br></p>{{\n{answertxt}}}\n\n\n"""


        return questionbody

def convert_to_gift(text,name, tag):

    qs = getQuestionsFromText(text)

    qs = [prepareQuestions(q, name, tag) for q in qs]

    if None not in qs:

        gift = "".join(qs)

        return gift

def convert_to_plain(text):

    qs = getQuestionsFromText(text)

    plain_text = ""

    for idx, question in enumerate(qs):
        q, answers = cleanQuestion(question)


        plain_text += f"### Question {idx+1}.: {q}  \n"
        for a in answers:
            if a[0] == "#":
                plain_text += f"__Right Answer__: {a[1:]}  \n"
            else:
                plain_text += f"Wrong Answer: {a}  \n"

        plain_text += f"  \n  \n"

    return plain_text


txt = json.dumps(content, ensure_ascii = False)
txt = convert_to_plain(txt)

text = st.write(txt)
