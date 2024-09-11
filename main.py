import streamlit as st
from streamlit.runtime.scriptrunner import RerunException
import uuid
import openpyxl
from openpyxl import Workbook
from io import BytesIO

st.set_page_config(page_title="Participant Portal", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .project-name { font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .track-title { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .participant { margin-left: 20px; margin-bottom: 5px; }
    .add-track-btn { margin-top: 20px; }
    .inline-input { display: inline-block; width: auto; }
    .track-container { margin-bottom: 40px; }
    .content-container { 
        max-width: 900px; 
        margin: 0 auto; 
        padding: 20px;
    }
    .stTextInput > div > div > input {
        width: 100%;
    }
    .share-input { width: 60px !important; }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }


</style>
""", unsafe_allow_html=True)

if 'project_name' not in st.session_state:
    st.session_state.project_name = ""

if 'tracks' not in st.session_state:
    st.session_state.tracks = [{
        'id': str(uuid.uuid4()),
        'title': 'TRACK TITLE 1',
        'participants': [{'id': str(uuid.uuid4()), 'name': 'Participant 1', 'share': 100.0, 'artist_name': ''}]
    }]

if 'participants' not in st.session_state:
    st.session_state.participants = [{
        'id': str(uuid.uuid4()),
        'name': 'Participant 1',
        'email': '',
        'pro': '',
        'ipicae': '',
        'artist_name1': '',
        'artist_name2': '',
        'share': None
    }]

def add_participant():
    new_participant = {
        'id': str(uuid.uuid4()),
        'name': f'Participant {len(st.session_state.participants) + 1}',
        'email': '',
        'pro': '',
        'ipicae': '',
        'artist_name1': '',
        'artist_name2': '',
        'share': None
    }
    st.session_state.participants.append(new_participant)


def delete_participant(participant_id):
    st.session_state.participants = [p for p in st.session_state.participants if p['id'] != participant_id]


def add_track():
    new_track_number = len(st.session_state.tracks) + 1
    st.session_state.tracks.append({
        'id': str(uuid.uuid4()),
        'title': f'TRACK TITLE {new_track_number}',
        'participants': [{'id': str(uuid.uuid4()), 'name': 'Participant 1', 'artist_name': ''}]
    })


def delete_track(track_id):
    st.session_state.tracks = [track for track in st.session_state.tracks if track['id'] != track_id]
    if len(st.session_state.tracks) == 0:
        # If all tracks are deleted, add a new default track
        st.session_state.tracks.append({
            'id': str(uuid.uuid4()),
            'title': 'TRACK TITLE 1',
            'participants': [{'id': str(uuid.uuid4()), 'name': 'Participant 1', 'share': 100.0, 'artist_name': ''}]
        })
    st.rerun()


def save_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Participant Portal"

    # Write headers
    ws.append(["Project Name", st.session_state.project_name])
    ws.append([])  # Empty row
    ws.append(["Track", "Participant", "Share", "PRO", "IPI/CAE", "Artist Name1", "Artist Name2"])

    # Write data
    for track in st.session_state.tracks:
        for participant in track['participants']:
            ws.append([
                track['title'],
                participant['name'],
                participant.get('share', ''),
                participant.get('artist_name', '')
            ])

    # Save to BytesIO object
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    return excel_file


# Main app layout
st.markdown("<h1 style='text-align: center;'>PARTICIPANT PORTAL</h1>", unsafe_allow_html=True)

# Create three columns and use the middle one for content
left_col, center_col, right_col = st.columns([1, 4, 1])

with center_col:
    st.markdown("<b>PROJECT NAME<b>", unsafe_allow_html=True)
    new_project_name = st.text_input(
        "",
        value='',
        key="project_name_input",
        label_visibility="collapsed"
    )
    if new_project_name != st.session_state.project_name:
        st.session_state.project_name = new_project_name

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<b>LIST OF PARTICIPANTS</b>", unsafe_allow_html=True)

    if 'participants' not in st.session_state:
        st.session_state.participants = [{
            'id': str(uuid.uuid4()),
            'name': 'Participant 1',
            'email': '',
            'pro': '',
            'ipicae': '',
            'artist_name1': '',
            'artist_name2': '',
            'share': 100  # Add this line
        }]

    for index, participant in enumerate(st.session_state.participants):
        cols = st.columns([0.5, 2, 2, 2, 2, 2, 2])

        with cols[0]:
            # Remove the condition to always show the trash button
            if st.button("🗑", key=f"delete_participant_{participant['id']}", on_click=delete_participant,
                         args=(participant['id'],)):
                # If the button is clicked, delete the participant and rerun
                st.rerun()

        with cols[1]:
            new_name = st.text_input("", value=participant.get('name', ''), key=f"name_{participant['id']}",
                                     placeholder="Name")
            if new_name != participant.get('name', ''):
                participant['name'] = new_name

        with cols[2]:
            new_email = st.text_input("", value=participant.get('email', ''), key=f"email_{participant['id']}",
                                      placeholder="Email")
            if new_email != participant.get('email', ''):
                participant['email'] = new_email

        with cols[3]:
            new_pro = st.text_input("", value=participant.get('pro', ''), key=f"pro_{participant['id']}",
                                    placeholder="PRO")
            if new_pro != participant.get('pro', ''):
                participant['pro'] = new_pro

        with cols[4]:
            new_ipicae = st.text_input("", value=participant.get('ipicae', ''), key=f"ipicae_{participant['id']}",
                                       placeholder="IPI/CAE")
            if new_ipicae != participant.get('ipicae', ''):
                participant['ipicae'] = new_ipicae

        with cols[5]:
            new_artist_name1 = st.text_input("", value=participant.get('artist_name1', ''),
                                             key=f"artist_name1_{participant['id']}", placeholder="Artist Name 1")
            if new_artist_name1 != participant.get('artist_name1', ''):
                participant['artist_name1'] = new_artist_name1

        with cols[6]:
            new_artist_name2 = st.text_input("", value=participant.get('artist_name2', ''),
                                             key=f"artist_name2_{participant['id']}", placeholder="Artist Name 2")
            if new_artist_name2 != participant.get('artist_name2', ''):
                participant['artist_name2'] = new_artist_name2
        # Adding the Spotify and Apple Music links in a new row
        cols = st.columns([2, 2])  # Two columns for the Spotify and Apple Music links

        with cols[0]:
            new_spotify_link = st.text_input("  ", value=participant.get('spotify_link', ''),
                                             key=f"spotify_link_{participant['id']}",
                                             placeholder="Spotify Artist Pag Link")
            if new_spotify_link != participant.get('spotify_link', ''):
                participant['spotify_link'] = new_spotify_link

        with cols[1]:
            new_apple_music_link = st.text_input("",
                                                 value=participant.get('apple_music_link', ''),
                                                 key=f"apple_music_link_{participant['id']}",
                                                 placeholder="Apple Music Artist Page Link")
            if new_apple_music_link != participant.get('apple_music_link', ''):
                participant['apple_music_link'] = new_apple_music_link


    def add_participant():
        new_participant = {
            'id': str(uuid.uuid4()),
            'name': f'Participant {len(st.session_state.participants) + 1}',
            'email': '',
            'pro': '',
            'ipicae': '',
            'artist_name1': '',
            'artist_name2': '',
            'share': 0
        }
        st.session_state.participants.append(new_participant)
        st.rerun()


    # Ensure there's always at least one participant
    if len(st.session_state.participants) == 0:
        add_participant()


    st.button("𝗔𝗗𝗗 𝗣𝗔𝗥𝗧𝗜𝗖𝗜𝗣𝗔𝗡𝗧", on_click=add_participant)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<b>TRACK TITLES<b>", unsafe_allow_html=True)
    # Get list of participant names and artist names
    participant_names = sorted([p['name'] for p in st.session_state.participants])
    artist_names = ["No artist attribution"] + sorted(
        list(set([p['artist_name1'] for p in st.session_state.participants if p['artist_name1']] +
                 [p['artist_name2'] for p in st.session_state.participants if p['artist_name2']])))
    # Inside the loop for tracks

    for track_index, track in enumerate(st.session_state.tracks):
        with st.container():
            st.markdown("<div class='track-container'>", unsafe_allow_html=True)

            col1, col2 = st.columns([0.4, 11.5])
            with col1:
                # Remove the condition to always show the trash button
                if st.button("🗑", key=f"delete_track_{track['id']}", on_click=delete_track, args=(track['id'],)):
                    # If the button is clicked, delete the track and rerun
                    st.rerun()

            with col2:
                new_track_title = st.text_input(
                    "",
                    value=track['title'],
                    key=f"track_title_{track['id']}",
                    label_visibility="collapsed"
                )
                if new_track_title != track['title']:
                    st.session_state.tracks[track_index]['title'] = new_track_title

            # Participant section
            for participant_index, participant in enumerate(track['participants']):
                cols = st.columns([0.4, 5, 2, 3])

                with cols[0]:
                    st.button("🗑", key=f"delete_participant_{track['id']}_{participant['id']}",
                              on_click=delete_participant, args=(track['id'], participant['id']))

                with cols[1]:
                    new_participant_name = st.selectbox(
                        "",
                        options=participant_names,
                        index=participant_names.index(participant['name']) if participant[
                                                                                  'name'] in participant_names else 0,
                        key=f"participant_name_{track['id']}_{participant['id']}",
                    )
                    if new_participant_name != participant['name']:
                        st.session_state.tracks[track_index]['participants'][participant_index][
                            'name'] = new_participant_name

                with cols[2]:
                    current_share = participant.get('share')
                    share_input = st.text_input(
                        "",
                        value=f"{current_share:.2f}" if current_share is not None else "",
                        key=f"participant_share_{track['id']}_{participant['id']}",
                        placeholder="Share %"
                    )
                    try:
                        new_share = float(share_input.strip('%')) if share_input else None
                        if new_share is not None:
                            if 0 <= new_share <= 100:
                                st.session_state.tracks[track_index]['participants'][participant_index][
                                    'share'] = new_share
                            else:
                                st.error("Share must be between 0 and 100")
                    except ValueError:
                        st.error("Invalid input for share. Please enter a number.")

                with cols[3]:
                    default_artist = "No artist attribution"
                    artist_name = participant.get('artist_name', default_artist)
                    if artist_name not in artist_names:
                        artist_name = default_artist

                    new_artist_name = st.selectbox(
                        "",
                        options=artist_names,
                        index=artist_names.index(artist_name),
                        key=f"artist_name_{track['id']}_{participant['id']}",
                    )
                    if new_artist_name != participant.get('artist_name', default_artist):
                        st.session_state.tracks[track_index]['participants'][participant_index][
                            'artist_name'] = new_artist_name


            # Keep your original add_track_participant function
            def add_track_participant(track_id=track['id']):
                for t in st.session_state.tracks:
                    if t['id'] == track_id:
                        new_participant_number = len(t['participants']) + 1
                        t['participants'].append({
                            'id': str(uuid.uuid4()),
                            'name': participant_names[
                                0] if participant_names else f'Participant {new_participant_number}',
                            'share': None,  # This will result in an empty initial field
                            'artist_name': 'No artist attribution'
                        })
                        break
                st.rerun()


            # Add participant button
            st.button("𝗔𝗗𝗗 𝗣𝗔𝗥𝗧𝗜𝗖𝗜𝗣𝗔𝗡𝗧", key=f"add_participant_{track['id']}", on_click=add_track_participant,
                      args=(track['id'],))

            # Display total share information
            total_share = sum(p.get('share', 0) for p in track['participants'] if p.get('share') is not None)
            if all(p.get('share') is not None for p in track['participants']) and abs(total_share - 100) < 0.01:
                st.success("✅ Shares equal 100%")
            else:
                st.warning("❌ Shares don't equal 100%")

        st.markdown("<br>", unsafe_allow_html=True)
    if len(st.session_state.tracks) == 0:
        st.session_state.tracks.append({
            'id': str(uuid.uuid4()),
            'title': 'TRACK TITLE 1',
            'participants': [{'id': str(uuid.uuid4()), 'name': 'Participant 1', 'share': 100.0, 'artist_name': ''}]
        })
        st.rerun()
    # Add track button (outside the track loop)
    st.button("𝗔𝗗𝗗 𝗔𝗡𝗢𝗧𝗛𝗘𝗥 𝗧𝗥𝗔𝗖𝗞", key="add_track", on_click=add_track)







    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("By clicking on SUBMIT, you hereby acknowledge that to the extent that Warner Chappell Production Music (“Company”) distributes master recordings embodying the songs set forth above (“Master(s)”) to digital service providers (“DSP(s)”), Company shall instruct its distributor(s) or DSP(s), as applicable, to provide credits on such DSP(s) to the artist names submitted via this form as recording artists in connection with the Master(s); provided, however, that Company shall in no event be liable in any way to you or any third party in connection with any inadvertent failure to do so. The foregoing shall be subject to Company’s, Company’s distributor(s)’, and each DSP’s standard credit practices and policies. To the extent that Company’s distributor(s) or DSP(s) accord recording artist credit to the provided artist names, Company shall have no obligation to subsequently instruct its distributor(s) or DSP(s), as applicable, to in any way remove or modify such recording artist credits.")

    # Wrap the Export to Excel button in a container with the 'center-button' class
    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("𝗦𝗨𝗕𝗠𝗜𝗧", key="export_to_excel_button"):
            excel_file = save_to_excel()
            st.download_button(
                label="Download Excel file",
                data=excel_file,
                file_name="participant_portal.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        st.markdown('</div>', unsafe_allow_html=True)
