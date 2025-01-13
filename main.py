import streamlit as st
from firebase_admin import db
import firebase_admin


st.set_page_config(page_title='Snowflake', layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
)

st.image("./logo/CodeBuddy.jpg", use_column_width=True)

st.snow()


# //////////////////////////////////////////////////////////////////////////////////////////


#####################################################################################
# Initialising multiple Firebase Realtime Database/projects in the same Python file #
#####################################################################################

# Setting up the Firebase database for the conversations:
if "conversations" not in firebase_admin._apps:
    # Initialize Firebase
    credentials_object_conversations = firebase_admin.credentials.Certificate("firebase_key_conversations.json")
    firebase_admin.initialize_app(credentials_object_conversations, {
        'databaseURL': 'https://urop-telegram-chatbot-default-rtdb.asia-southeast1.firebasedatabase.app/'
    }, name='conversations')

# Get a reference to the database
reference_to_database_conversations = db.reference('/', app=firebase_admin.get_app('conversations'))



# Setting up the Firebase database for the assignments:   
if "assignments" not in firebase_admin._apps:
    # Initialize Firebase
    credentials_object_assignments = firebase_admin.credentials.Certificate("firebase_key_assignments.json")
    firebase_admin.initialize_app(credentials_object_assignments, {
        'databaseURL': 'https://urop-chatbot-assignments-default-rtdb.asia-southeast1.firebasedatabase.app/'
    }, name='assignments')

# Get a reference to the database
reference_to_database_assignments = db.reference('/', app=firebase_admin.get_app('assignments'))


# ////////////////////////////////////////////////////////////////////////////////////////////////////////


###################################################################
# Firebase's Database for assignments to Streamlit website things #
###################################################################

# Read data from the Realtime Database from Firebase
database_data_assignments = reference_to_database_assignments.get()

# Check if the Firebase Realtime database is None or empty
if database_data_assignments is None:
    st.write("No data found in the Firebase Realtime Database.")
else:
    # Converting the Firebase Realtime Database to a list of dictionaries
    if isinstance(database_data_assignments, dict):
        database_data_assignments = list(database_data_assignments.values())

        print(f"Database data assignments variable: {database_data_assignments}")


# ///////////////////////////////////////////////////////////////////////////////////////


########################
# Remvoed this section #
########################
_, exp_col, _ = st.columns([1,3,1])
with exp_col:
    with st.expander("**📖 How to use this Streamlit Website for CodeBuddy Bot**"):
        st.markdown("""                    
                    **What can I do here??** 🤔

                    You, the course instructor, can upload school assignments and the corresponding notes to CodeBuddy Bot here so it is up-to-date with the
                    latest available tasks and information.

                    It also serves as a place for course instructors like you to do learning review and keep track of your students' learning by searching for a particular student or assignment! 🔥🔥
                    """)


# //////////////////////////////////////////////////////////////////////////////////////


cols = st.columns(2)

###########################################
# Student and CodeBuddy Conversation Card #
###########################################
def student_chatbot_conversation(index):
    st.header(f"👨‍🎓 Student ID: {database_data_conversations[index]['student_id']}")
    st.caption(f"{database_data_conversations[index]['assignment']} | {database_data_conversations[index]['date_and_time_of_submission']}")
    student_code_tab, chatbot_response_tab, autograding_score_tab, assignment_question_tab, assignment_notes_tab = \
        st.tabs(["Student's Code", "Codebuddy's Response", "Score", "Question", "Notes"])
    
    with student_code_tab:
        st.code(database_data_conversations[index]['code_submitted'], language="python")

    with chatbot_response_tab:
        st.code(database_data_conversations[index]['telegram_chatbot_chatbase_response'], language="text")

    with autograding_score_tab:
        st.markdown("""🎯 Autograded score:  
                    **6/10**""")

    with assignment_question_tab:
        st.markdown(f"*{database_data_conversations[index]['assignment']}*")

    with assignment_notes_tab:
        st.markdown(f"📖 Lecture notes for the *{database_data_conversations[index]['assignment']}* assignment:")


# /////////////////////////////////////////////////////////////////////////////////////////


#################
# Sidebar codes #
#################
st.sidebar.title("📚 CodeBuddy Bot for *Beginner Programming Courses* 💻")
st.sidebar.write("**Your Personal Coding Assistant to kickstart your programming journey!**")
st.sidebar.caption("Made by [WindJammer6](https://github.com/WindJammer6)")
st.sidebar.caption("Made possible with:")

sidebar_content = """
<div style="display: flex; align-items: center;">
    <img src="https://companieslogo.com/img/orig/SNOW-35164165.png?t=1634190631" width="25" style="margin-right: 10px;">
    <span style="font-size: 14px; margin-right: 10px;">|</span>
    <img src="https://mistral.ai/images/news/announcing-mistral.png" width="50" style="margin-right: 10px;">
    <span style="font-size: 14px; margin-right: 10px;">|</span>
    <img src="https://miro.medium.com/v2/resize:fit:628/1*MpZGG5oPHVFlFDTu4b_1IA.png" width="35">
</div>
"""

st.sidebar.markdown(sidebar_content, unsafe_allow_html=True)
st.sidebar.caption("")


# ///////////////////////////////////////////////////////////////////////////////////////////


# Search by Student ID section
search_by_student_id = st.sidebar.text_input("🔍👨‍🎓 **Search by Student ID:**", placeholder="Type student's ID here...")

if st.sidebar.button("Search", key=1):


    # ////////////////////////////////////////////////////////////////////////////////////////////////////////


    # Firebase's Database for conversations to Streamlit website things

    # Read data from the Realtime Database from Firebase
    database_data_conversations = reference_to_database_conversations.get()


    # Check if the Firebase Realtime database is None or empty
    if database_data_conversations is None:
        st.write("No data found in the Firebase Realtime Database.")
    else:
        # Converting the Firebase Realtime Database to a list of dictionaries
        if isinstance(database_data_conversations, dict):
            database_data_conversations = list(database_data_conversations.values())

            print(f"Database data conversations variable: {database_data_conversations}")
        

        # Main content
        for i in range(len(database_data_conversations)-1, -1, -1):
            if database_data_conversations[i]['student_id'] == search_by_student_id:
                if i % 2 == 0:
                    with cols[0]:
                        student_chatbot_conversation(i)
                
                else:
                    with cols[1]:
                        student_chatbot_conversation(i)


# Search by Assignment section
search_by_assignment = st.sidebar.text_input("🔍📝 or... **Search by Assignment (caps sensitive):**", placeholder="Type assignment here...")
# st.sidebar.button("Search", key=2)

if st.sidebar.button(f"Search", key=2):


    # ////////////////////////////////////////////////////////////////////////////////////////////////////////


    # Firebase's Database for conversations to Streamlit website things

    # Read data from the Realtime Database from Firebase
    database_data_conversations = reference_to_database_conversations.get()


    # Check if the Firebase Realtime database is None or empty
    if database_data_conversations is None:
        st.write("No data found in the Firebase Realtime Database.")
    else:
        # Converting the Firebase Realtime Database to a list of dictionaries
        if isinstance(database_data_conversations, dict):
            database_data_conversations = list(database_data_conversations.values())

            print(f"Database data conversations variable: {database_data_conversations}")

        
        # Main content
        for i in range(len(database_data_conversations)-1, -1, -1):
            if database_data_conversations[i]['assignment'] == search_by_assignment:
                if i % 2 == 0:
                    with cols[0]:
                        student_chatbot_conversation(i)
                
                else:
                    with cols[1]:
                        student_chatbot_conversation(i)


# ////////////////////////////////////////////////////////////////////////////////


##############################
# Manage Assignments section #
##############################
add_remove_assignments = st.sidebar.expander("📝 Manage Assignments")
with add_remove_assignments:
    st.title("Available Assignments:")
    st.caption("These assignments will be publicly available to the students in the CodeBuddy Bot 🤖.")
    side_left_col, side_right_col = st.columns(2)

    if database_data_assignments is not None:
        for i, assignment in enumerate(database_data_assignments):
            if i % 2 == 0:
                if side_left_col.write(f"*{assignment['assignment_name']}*"):
                    search_by_assignment = f"*{assignment['assignment_name']}*"
                    print(search_by_assignment)


                    # ////////////////////////////////////////////////////////////////////////////////////////////////////////


                    # Firebase's Database for conversations to Streamlit website things

                    # Read data from the Realtime Database from Firebase
                    database_data_conversations = reference_to_database_conversations.get()


                    # Check if the Firebase Realtime database is None or empty
                    if database_data_conversations is None:
                        st.write("No data found in the Firebase Realtime Database.")
                    else:
                        # Converting the Firebase Realtime Database to a list of dictionaries
                        if isinstance(database_data_conversations, dict):
                            database_data_conversations = list(database_data_conversations.values())

                            print(f"Database data conversations variable: {database_data_conversations}")

            else:
                if side_right_col.write(f"*{assignment['assignment_name']}*"):
                    search_by_assignment = f"*{assignment['assignment_name']}*"
                    print(search_by_assignment)


                    # ////////////////////////////////////////////////////////////////////////////////////////////////////////


                    # Firebase's Database for conversations to Streamlit website things

                    # Read data from the Realtime Database from Firebase
                    database_data_conversations = reference_to_database_conversations.get()


                    # Check if the Firebase Realtime database is None or empty
                    if database_data_conversations is None:
                        st.write("No data found in the Firebase Realtime Database.")
                    else:
                        # Converting the Firebase Realtime Database to a list of dictionaries
                        if isinstance(database_data_conversations, dict):
                            database_data_conversations = list(database_data_conversations.values())

                            print(f"Database data conversations variable: {database_data_conversations}")

    with st.popover("➕Add Assignment"):
        st.markdown(
            """
            <style>
            .big-font {
                font-size:30px !important;
            }
            </style>
            <p class="big-font">Add Assignment:</p>
            """,
            unsafe_allow_html=True
        )
        st.caption("Just click the 'Add Assignment' button once! Then click the 'Refresh' button for the added assignment to show up!")
        assignment_name = st.text_input("Name of assignment:")
        assignment_link = st.text_area("Assignment notes:")

        if st.button("Add"):
            #If confirmation add assignment button is pressed in the Streamlit (Python) web application, the program will 'push' 
            #basically add this new pieces of user data into the Realtime database in Firebase  
            reference_to_database_assignments.push({"assignment_name" : assignment_name, "assignment_link" : assignment_link})    
    
    with st.popover("➖Remove Assignment"):
        st.caption("Just click the 'Remove Assignment' button once! Then click the 'Refresh' button for the assignment to be removed!")
        st.markdown(
            """
            <style>
            .big-font {
                font-size:30px !important;
            }
            </style>
            <p class="big-font">Add Assignment:</p>
            """,
            unsafe_allow_html=True
        )

        options_list = []
        for key, value in reference_to_database_assignments.get().items():
            options_list.append(value['assignment_name'])

        select_box_option = st.selectbox("➖Remove Assignment:", options_list)
    
        if st.button("Remove"):
            for key, value in reference_to_database_assignments.get().items():
                if value.get('assignment_name') == select_box_option:
                    # Remove the data based on the key
                    reference_to_database_assignments.child(key).delete()
                    print(f"Removed assignment: {assignment['assignment_name']}")
                    break
            else:
                print("No matching records found.")

    st.button("Refresh")

st.sidebar.success("""
                   **What is CodeBuddy Bot?**  
                   CodeBuddy Bot is a Telegram Chatbot that allows novice programmers to get instant feedback for errors/quality of their code 
                   for their school assignments based on the given school notes before submission to their respective school assignment submission 
                   portals. In addition, it allows course instructors/teachers to upload their assignments and notes for each assignment, as well as 
                   review conversations between the students and the Telegram Chatbot (as teaching review to what troubles the students are facing) 
                   via a Streamlit website.
"""
)

st.sidebar.info("""
                **What is this Streamlit website for?**  
                This online Streamlit website is for course instructors to control the settings of CodeBuddy Bot, including:  
                1. Add and Remove Course Assignments
                2. Upload Corresponding Notes for the Assignments
                3. Review Code Submitted by Students as well as the Corresponding Responses from CodeBuddy Bot
"""
)

with st.sidebar.expander("Acknowledgments"):
    st.markdown("""
    I am incredibly grateful to my university professor [Oka Kurniawan](https://www.linkedin.com/in/oka-kurniawan-6314479/?originalSubdomain=sg), who inspired me to come up with this project idea. 
    """)