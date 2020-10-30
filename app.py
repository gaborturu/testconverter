import streamlit as st
import base64
import re
from streamlit_ace import st_ace
import json

st.set_page_config(page_title="Test converter", layout='wide')

########################################################
#########  test converting functions ###################
########################################################


def download_gift(gift):
    """Generates a link allowing the gift file to be downloaded
    in:  test string data
    out: href string to gift formatted test
    """
    b64 = base64.b64encode(gift.encode()).decode(
    )  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/txt;base64,{b64}" download = "{name}.gift" >Download GIFT file</a>'
    return href


def getQuestionsFromText(txt):
    """Splits the text into question blocks"""
    qs = txt.split('\\n\\n')
    qs = [x for x in qs if len(x) > 4]

    return qs


def cleanQuestion(question):
    """drop all lines with no letters or numbers and return question and answers separately"""
    try:
        lines = question.split('\\n')
        lines = [l for l in lines if len("".join(re.findall('\w*', l))) > 0
                 ]  # drop all lines with no letters or numbers
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
        txt = """no right answers, please label the right answers with #\n\nWrong question:\n\n{}\n{}""".format(
            q, '\n'.join(answers))
        with col2:
            preview = st_ace(value=txt,
                             language="plain_text",
                             theme="iplastic",
                             font_size=14,
                             show_gutter=False,
                             show_print_margin=False,
                             wrap=True,
                             auto_update=True,
                             readonly=True)

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


def convert2Gift(text, name, tag):
    """iterates through questions and converts them all to GIFT format"""
    qs = getQuestionsFromText(text)

    qs = [prepareQuestions(q, name, tag) for q in qs]

    if None not in qs:

        gift = "".join(qs)

        return gift


def convert2Plain(text):
    """converts question to a human-readable format, labeling rigth and wrong answers"""

    qs = getQuestionsFromText(text)

    plain_text = ""

    for idx, question in enumerate(qs):
        q, answers = cleanQuestion(question)

        plain_text += f"Question {idx+1}.: {q}\n\n"
        for a in answers:
            if a[0] == "#":
                plain_text += f"Right Answer: {a[1:]}\n"
            else:
                plain_text += f"Wrong Answer: {a}\n"

        plain_text += f"  \n ------------------------------------------------------ \n"

    return plain_text


##########################################################
############## Layout ###################################
##########################################################

st.header("Plain-text-multiple-choice test - to GIFT converter")
st.markdown(
    "The converter converts raw text to gift-formatted test questions which can be imported into moodle. Paste your test questions below and preview them on the right. Mark the right answers with '#', leave at least one empy row between questions. If everything seems alright, click the 'Convert to GIFT' button and the donwload link will appear. If it does not, check your text and the outputs for errors."
)

#####   top row conatining the controls

head1, head2, head3, head4, head5, head6, head7 = st.beta_columns(
    [2, 2, 2, 1, 1, 1, 3])

with head1:
    name = st.text_input("Name: (e.g. date)", "name")

with head2:

    tag = st.text_input("Tag: (e.g. chapter)", "tag")

with head3:

    radio = st.radio("Preview mode:", ['plain text', 'gift'])

with head4:
    font_size = st.slider("Font size", 5, 24, 14)

with head6:
    st.write(' ')
    button = st.button("Convert to GIFT!")

with head7:
    st.write(' ')
    link_placeholder = st.empty()

##  columns for the editors

col1, col2 = st.beta_columns([6, 6])

with col1:
    st.header("Paste / write your questions here:")
    input = st_ace(
        value=
        "Which of the following numbers are prime numbers? (Example question, replace it with your questions)\n#3\n4\n12\n#17",
        language="plain_text",
        theme="iplastic",
        font_size=font_size,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        key="ace-editor")

with col2:
    st.header("Preview (plain text or GIFT-formatted):")

input = json.dumps(
    input, ensure_ascii=False
)[1:
  -1]  # get the text from the editor. First and last strings are quotation marks in the json.dumps

if radio == 'gift':
    gift = convert_to_gift(input, name, tag)
    if gift is not None:
        with col2:
            preview = st_ace(value=gift,
                             language="plain_text",
                             theme="iplastic",
                             font_size=font_size,
                             show_gutter=False,
                             show_print_margin=False,
                             wrap=True,
                             auto_update=True,
                             readonly=True)

else:
    plain = convert_to_plain(input)
    if plain is not None:
        with col2:
            preview = st_ace(value=plain,
                             language="plain_text",
                             theme="iplastic",
                             font_size=font_size,
                             show_gutter=False,
                             show_print_margin=False,
                             wrap=True,
                             auto_update=True,
                             readonly=True)

### Convert and download options

link_placeholder.empty()

if button:
    gift = convert_to_gift(input, name, tag)
    if gift is not None:
        href = download_gift(gift)
        link_placeholder.markdown(href, unsafe_allow_html=True)
