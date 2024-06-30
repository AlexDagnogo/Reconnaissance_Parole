import streamlit as st
import speech_recognition as sr
import time

def transcrire_parole(api, langue='fr-FR'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio_text = r.listen(source)
        st.info("Transcription en cours...")

        try:
            if api == "Google":
                texte = r.recognize_google(audio_text, language=langue)
            elif api == "Sphinx":
                texte = r.recognize_sphinx(audio_text, language=langue)
            # Ajouter d'autres APIs ici
            else:
                texte = "API de reconnaissance vocale non supportée."
            return texte
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris."
        except sr.RequestError as e:
            return f"Impossible de demander les résultats; {e}"
        except Exception as e:
            return f"Une erreur s'est produite : {e}"

def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le micro pour commencer à parler:")

    api = st.selectbox(
        "Sélectionnez l'API de reconnaissance vocale :",
        ["Google", "Sphinx"]
    )

    langue = st.selectbox(
        "Sélectionnez la langue :",
        ["fr-FR", "en-US", "es-ES", "de-DE", "it-IT"]
    )

    # Variables pour suspendre et reprendre l'enregistrement
    global is_recording, is_paused
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'is_paused' not in st.session_state:
        st.session_state.is_paused = False

    if st.button("Commencer l'enregistrement"):
        st.session_state.is_recording = True
        st.session_state.is_paused = False

    if st.session_state.is_recording:
        if st.button("Suspendre l'enregistrement"):
            st.session_state.is_paused = True
        if st.session_state.is_paused:
            if st.button("Reprendre l'enregistrement"):
                st.session_state.is_paused = False
                texte = transcrire_parole(api, langue)
                st.write("Transcription : ", texte)

                if st.button("Enregistrer la transcription"):
                    with open("transcription.txt", "w") as fichier:
                        fichier.write(texte)
                    st.success("Transcription enregistrée avec succès !")
        else:
            texte = transcrire_parole(api, langue)
            st.write("Transcription : ", texte)

            if st.button("Enregistrer la transcription"):
                with open("transcription.txt", "w") as fichier:
                    fichier.write(texte)
                st.success("Transcription enregistrée avec succès !")

if __name__ == "__main__":
    main()
