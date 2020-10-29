import streamlit as st
import base64
import re

st.set_page_config(page_title= "Test converter", layout='wide')

def download_gift(gift):
    """Generates a link allowing the gift file to be downloaded
    in:  test string data
    out: href string to gift formatted test
    """
    b64 = base64.b64encode(gift.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/txt;base64,{b64}" download = "{name}.gift" >Download GIFT file</a>'
    return href

def getQuestionsFromText(txt):
    """Splits the text into question blocks"""
    qs = txt.split('\n\n')
    qs = [x for x in qs if len(x) > 4]

    return qs

def cleanQuestion(question):
    """drop all lines with no letters or numbers and return question and answers separately"""
    try:
        lines = question.split('\n')
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

### Layout
st.header("Plain-text-multiple-choice test - to GIFT converter")
st.markdown("The converter converts raw text to gift-formatted test questions which can be imported into moodle. Paste your test questions below and preview them on the right. Mark the right answers with '#', leave at least one empy row between questions. If everything seems alright, click the 'Convert to GIFT' button and the donwload link will appear. If it does not, check your text and the outputs for errors.")

head1, head2, head3 = st.beta_columns([2,2, 8])

with head1:
    name = st.text_input("Name: (e.g. date)", "name")

with head2:
    tag = st.text_input("Tag: (e.g. chapter)", "tag")

col1, col2 = st.beta_columns([6,6])

with col1:
    st.header("Paste / write your questions here:")
    input = st.text_area(label = '', value="Which of the following numbers are prime numbers? (Example question, replace it with your questions)\n#3\n4\n12\n#17", height= 300)

    button = st.button("Convert to GIFT!")

    link_placeholder = st.empty()

with col2:
    st.header("Output preview:")
    radio = st.radio("Select Format", ['plain text', 'gift'])
    placeholder = st.empty()
    placeholder.text("Which of the following numbers are prime numbers?\n3\n4\n12\n17")


#### The app logic

if radio == 'gift':
    gift = convert_to_gift(input, name, tag)
    if gift is not None:
        placeholder.text(gift)

else:
    plain = convert_to_plain(input)
    if plain is not None:
        placeholder.markdown(plain)


### Convert and download

link_placeholder.empty()

if button:
    gift = convert_to_gift(input, name, tag)
    if gift is not None:
        href = download_gift(gift)
        link_placeholder.markdown(href, unsafe_allow_html=True)
