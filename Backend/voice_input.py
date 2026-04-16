import speech_recognition as sr
import streamlit as st


def capturar_voz():
    """
    Captura áudio do microfone e converte em texto.
    Retorna o texto falado pelo usuário.
    """
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Fale agora... (aguardando áudio)")
            # Ajusta o ruído ambiente automaticamente
            r.adjust_for_ambient_noise(source, duration=1)
            # Escuta o áudio (timeout de 5 segundos)
            audio = r.listen(source, timeout=5)

        st.info("⏳ Processando áudio...")
        # Converte áudio em texto usando Google
        texto = r.recognize_google(audio, language='pt-BR')
        return texto

    except sr.WaitTimeoutError:
        return "Nenhum áudio detectado. Tente novamente."
    except sr.UnknownValueError:
        return "Não consegui entender o áudio. Tente novamente."
    except sr.RequestError:
        return "Erro ao conectar ao serviço de voz. Verifique sua internet."
    except Exception as e:
        return f"Erro inesperado: {e}"


def exibir_input_voz():
    """
    Exibe o botão de voz no Streamlit.
    Pode ser usado no totem_interface.py como alternativa ao teclado.
    """
    st.markdown("### 🎤 Entrada por Voz")

    if st.button("🎙️ Clique para falar"):
        texto_capturado = capturar_voz()
        if texto_capturado:
            st.success(f"✅ Você disse: **{texto_capturado}**")
            return texto_capturado

    return None