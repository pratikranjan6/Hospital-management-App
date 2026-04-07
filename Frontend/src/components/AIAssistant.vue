<template>
  <div v-if="isOpen" class="ai-assistant-overlay">
    <div class="ai-assistant-modal">
      <!-- Header -->
      <div class="assistant-header">
        <div class="header-left">
          <div class="ai-icon">
            <i class="fas fa-robot"></i>
          </div>
          <div class="header-info">
            <h2>AI Medical Assistant</h2>
            <p>How can I help you today?</p>
          </div>
        </div>
        <button @click="closeAssistant" class="close-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Language Selector -->
      <div class="language-selector">
        <label>Select Language:</label>
        <select v-model="selectedLanguage" class="language-select">
          <option value="en">English</option>
          <option value="hi">Hindi (हिंदी)</option>
          <option value="es">Spanish (Español)</option>
          <option value="fr">French (Français)</option>
          <option value="de">German (Deutsch)</option>
          <option value="pt">Portuguese (Português)</option>
        </select>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3>Quick Guides</h3>
        <div class="actions-grid">
          <button
            v-for="action in quickActions"
            :key="action.id"
            @click="handleQuickAction(action)"
            class="action-btn"
            :class="{ active: selectedAction === action.id }"
          >
            <i :class="action.icon"></i>
            {{ getTranslatedText(action.label) }}
          </button>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="chat-container">
        <div class="messages-wrapper">
          <div v-for="message in messages" :key="message.id" class="message" :class="message.type">
            <div class="message-content">
              <div v-if="message.type === 'assistant'" class="assistant-avatar">
                <i class="fas fa-robot"></i>
              </div>
              <div class="message-text">
                <p v-html="formatMessage(message.text)"></p>
              </div>
            </div>
          </div>
          <div v-if="isLoading" class="message assistant">
            <div class="message-content">
              <div class="assistant-avatar">
                <i class="fas fa-robot"></i>
              </div>
              <div class="message-text">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <input
            v-model="userMessage"
            type="text"
            class="message-input"
            :placeholder="getTranslatedText('Ask me anything...')"
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage" class="send-btn" :disabled="!userMessage.trim() || isLoading">
            <i class="fas fa-paper-plane"></i>
            <span>📤</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getApiBase } from '../utils/auth'

const translations = {
  en: {
    'Ask me anything...': 'Ask me anything...',
    'Complete Your Profile': 'Complete Your Profile',
    'Explore Departments': 'Explore Departments',
    'Find a Doctor': 'Find a Doctor',
    'Book Appointment': 'Book Appointment',
    'Check My History': 'Check My History',
    profileGuide:
      '<b>How to Complete Your Profile:</b><br/>1. Click on "Edit Profile" from your dashboard<br/>2. Fill in your personal information (Name, Age, DOB)<br/>3. Select your Gender and Blood Group<br/>4. Add your Address (optional)<br/>5. Click "Save Changes"<br/><br/>This helps doctors understand your medical background better.',
    departmentGuide:
      '<b>How to Explore Departments:</b><br/>1. Go to your Dashboard<br/>2. You\'ll see "Available Departments" card<br/>3. Browse through departments like Cardiology, Neurology, etc.<br/>4. Click "View Details" to see specialists<br/>5. Each department has expert doctors<br/><br/>Choose based on your medical need.',
    doctorGuide:
      '<b>How to Find a Doctor:</b><br/>1. Select a Department from the dashboard<br/>2. View all available doctors in that department<br/>3. Check their qualifications and experience<br/>4. Read their specialization<br/>5. Click on a doctor to see their availability<br/><br/>You can book appointments with any available doctor.',
    appointmentGuide:
      '<b>How to Book an Appointment:</b><br/>1. Find and click on your preferred doctor<br/>2. View "Next 7 Days Availability"<br/>3. Select a date that works for you<br/>4. The appointment status will show available slots<br/>5. Click "Book Now" to confirm<br/>6. Check confirmation in your history<br/><br/>You can cancel anytime if needed.',
    historyGuide:
      '<b>How to Check Your Medical History:</b><br/>1. Click "History" from the navigation<br/>2. View all your past appointments<br/>3. See doctor notes and diagnoses<br/>4. Check prescribed medicines<br/>5. Export your history as CSV<br/><br/>Keep your records safe for future reference.'
  },
  hi: {
    'Ask me anything...': 'मुझसे कोई भी सवाल पूछें...',
    'Complete Your Profile': 'अपनी प्रोफाइल पूरी करें',
    'Explore Departments': 'विभागों को देखें',
    'Find a Doctor': 'एक डॉक्टर खोजें',
    'Book Appointment': 'अपॉइंटमेंट बुक करें',
    'Check My History': 'मेरा इतिहास देखें',
    profileGuide:
      '<b>अपनी प्रोफाइल कैसे पूरी करें:</b><br/>1. अपने डैशबोर्ड से "Edit Profile" पर क्लिक करें<br/>2. अपनी व्यक्तिगत जानकारी भरें (नाम, आयु, जन्मतिथि)<br/>3. अपना लिंग और रक्त समूह चुनें<br/>4. अपना पता जोड़ें (वैकल्पिक)<br/>5. "Save Changes" पर क्लिक करें<br/><br/>यह डॉक्टरों को आपकी चिकित्सा पृष्ठभूमि समझने में मदद करता है।',
    departmentGuide:
      '<b>विभागों को कैसे देखें:</b><br/>1. अपने डैशबोर्ड पर जाएं<br/>2. आप "Available Departments" कार्ड देखेंगे<br/>3. कार्डियोलॉजी, न्यूरोलॉजी आदि विभागों को ब्राउज करें<br/>4. विवरण देखने के लिए "View Details" पर क्लिक करें<br/>5. प्रत्येक विभाग में विशेषज्ञ डॉक्टर हैं<br/><br/>अपनी चिकित्सा आवश्यकता के अनुसार चुनें।',
    doctorGuide:
      '<b>डॉक्टर कैसे खोजें:</b><br/>1. डैशबोर्ड से एक विभाग चुनें<br/>2. उस विभाग में सभी उपलब्ध डॉक्टरों को देखें<br/>3. उनकी योग्यता और अनुभव देखें<br/>4. उनकी विशेषज्ञता पढ़ें<br/>5. उपलब्धता देखने के लिए डॉक्टर पर क्लिक करें<br/><br/>आप किसी भी उपलब्ध डॉक्टर के साथ अपॉइंटमेंट बुक कर सकते हैं।',
    appointmentGuide:
      '<b>अपॉइंटमेंट कैसे बुक करें:</b><br/>1. अपने पसंदीदा डॉक्टर को खोजें और क्लिक करें<br/>2. "Next 7 Days Availability" देखें<br/>3. एक तारीख चुनें जो आपके लिए काम करे<br/>4. अपॉइंटमेंट स्थिति उपलब्ध स्लॉट दिखाएगी<br/>5. "Book Now" पर क्लिक करके पुष्टि करें<br/>6. आपके इतिहास में पुष्टि की जांच करें<br/><br/>यदि आवश्यकता हो तो आप किसी भी समय रद्द कर सकते हैं।',
    historyGuide:
      '<b>अपने चिकित्सा इतिहास को कैसे देखें:</b><br/>1. नेविगेशन से "History" पर क्लिक करें<br/>2. अपनी सभी पिछली अपॉइंटमेंट देखें<br/>3. डॉक्टर के नोट्स और निदान देखें<br/>4. निर्धारित दवाएं देखें<br/>5. अपने इतिहास को CSV के रूप में निर्यात करें<br/><br/>भविष्य के संदर्भ के लिए अपने रिकॉर्ड सुरक्षित रखें।'
  },
  es: {
    'Ask me anything...': 'Pregúntame cualquier cosa...',
    'Complete Your Profile': 'Completa Tu Perfil',
    'Explore Departments': 'Explora Departamentos',
    'Find a Doctor': 'Encuentra un Doctor',
    'Book Appointment': 'Reservar Cita',
    'Check My History': 'Ver Mi Historial',
    profileGuide:
      '<b>Cómo completar tu perfil:</b><br/>1. Haz clic en "Edit Profile" desde tu panel<br/>2. Completa tu información personal (Nombre, Edad, Fecha de Nacimiento)<br/>3. Selecciona tu género y grupo sanguíneo<br/>4. Añade tu dirección (opcional)<br/>5. Haz clic en "Save Changes"<br/><br/>Esto ayuda a los doctores a entender mejor tu historial médico.',
    departmentGuide:
      '<b>Cómo explorar departamentos:</b><br/>1. Ve a tu Dashboard<br/>2. Verás la tarjeta "Available Departments"<br/>3. Explora departamentos como Cardiología, Neurología, etc.<br/>4. Haz clic en "View Details" para ver especialistas<br/>5. Cada departamento tiene doctores expertos<br/><br/>Elige según tu necesidad médica.',
    doctorGuide:
      '<b>Cómo encontrar un doctor:</b><br/>1. Selecciona un departamento del panel<br/>2. Ve todos los doctores disponibles en ese departamento<br/>3. Verifica sus calificaciones y experiencia<br/>4. Lee su especialización<br/>5. Haz clic en un doctor para ver su disponibilidad<br/><br/>Puedes reservar citas con cualquier doctor disponible.',
    appointmentGuide:
      '<b>Cómo reservar una cita:</b><br/>1. Encuentra y haz clic en tu doctor preferido<br/>2. Ve "Next 7 Days Availability"<br/>3. Selecciona una fecha que te funcione<br/>4. El estado de la cita mostrará espacios disponibles<br/>5. Haz clic en "Book Now" para confirmar<br/>6. Verifica la confirmación en tu historial<br/><br/>Puedes cancelar en cualquier momento si es necesario.',
    historyGuide:
      '<b>Cómo ver tu historial médico:</b><br/>1. Haz clic en "History" de la navegación<br/>2. Ve todas tus citas anteriores<br/>3. Consulta notas del doctor y diagnósticos<br/>4. Verifica medicinas prescritas<br/>5. Exporta tu historial como CSV<br/><br/>Guarda tus registros para futuras referencias.'
  },
  fr: {
    'Ask me anything...': 'Posez-moi n\'importe quelle question...',
    'Complete Your Profile': 'Complétez Votre Profil',
    'Explore Departments': 'Explorez les Départements',
    'Find a Doctor': 'Trouvez un Docteur',
    'Book Appointment': 'Réserver un Rendez-vous',
    'Check My History': 'Voir Mon Historique',
    profileGuide:
      '<b>Comment compléter votre profil:</b><br/>1. Cliquez sur "Edit Profile" depuis votre tableau de bord<br/>2. Remplissez vos informations personnelles (Nom, Âge, Date de Naissance)<br/>3. Sélectionnez votre sexe et groupe sanguin<br/>4. Ajoutez votre adresse (facultatif)<br/>5. Cliquez sur "Save Changes"<br/><br/>Cela aide les médecins à mieux comprendre vos antécédents médicaux.',
    departmentGuide:
      '<b>Comment explorer les départements:</b><br/>1. Allez à votre tableau de bord<br/>2. Vous verrez la carte "Available Departments"<br/>3. Parcourez les départements comme Cardiologie, Neurologie, etc.<br/>4. Cliquez sur "View Details" pour voir les spécialistes<br/>5. Chaque département dispose de docteurs experts<br/><br/>Choisissez en fonction de vos besoins médicaux.',
    doctorGuide:
      '<b>Comment trouver un docteur:</b><br/>1. Sélectionnez un département du tableau de bord<br/>2. Voir tous les docteurs disponibles dans ce département<br/>3. Vérifiez leurs qualifications et expérience<br/>4. Lisez leur spécialisation<br/>5. Cliquez sur un docteur pour voir sa disponibilité<br/><br/>Vous pouvez réserver des rendez-vous avec n\'importe quel docteur disponible.',
    appointmentGuide:
      '<b>Comment réserver un rendez-vous:</b><br/>1. Trouvez et cliquez sur votre docteur préféré<br/>2. Consultez "Next 7 Days Availability"<br/>3. Sélectionnez une date qui vous convient<br/>4. Le statut du rendez-vous affichera les créneaux disponibles<br/>5. Cliquez sur "Book Now" pour confirmer<br/>6. Vérifiez la confirmation dans votre historique<br/><br/>Vous pouvez annuler à tout moment si nécessaire.',
    historyGuide:
      '<b>Comment consulter votre historique médical:</b><br/>1. Cliquez sur "History" dans la navigation<br/>2. Consultez tous vos rendez-vous précédents<br/>3. Consultez les notes du docteur et les diagnostics<br/>4. Vérifiez les médicaments prescrits<br/>5. Exportez votre historique en CSV<br/><br/>Gardez vos dossiers en sécurité pour référence ultérieure.'
  },
  de: {
    'Ask me anything...': 'Fragen Sie mich alles...',
    'Complete Your Profile': 'Ihr Profil Vervollständigen',
    'Explore Departments': 'Abteilungen Erkunden',
    'Find a Doctor': 'Finden Sie Einen Arzt',
    'Book Appointment': 'Termin Buchen',
    'Check My History': 'Mein Verlauf Ansehen',
    profileGuide:
      '<b>So vervollständigen Sie Ihr Profil:</b><br/>1. Klicken Sie auf "Edit Profile" in Ihrem Dashboard<br/>2. Füllen Sie Ihre persönlichen Informationen aus (Name, Alter, Geburtsdatum)<br/>3. Wählen Sie Ihr Geschlecht und Ihre Blutgruppe<br/>4. Fügen Sie Ihre Adresse hinzu (optional)<br/>5. Klicken Sie auf "Save Changes"<br/><br/>Dies hilft Ärzten, Ihre medizinische Geschichte besser zu verstehen.',
    departmentGuide:
      '<b>So erkunden Sie Abteilungen:</b><br/>1. Gehen Sie zu Ihrem Dashboard<br/>2. Sie sehen die Karte "Available Departments"<br/>3. Erkunden Sie Abteilungen wie Kardiologie, Neurologie usw.<br/>4. Klicken Sie auf "View Details", um Spezialisten anzuzeigen<br/>5. Jede Abteilung hat erfahrene Ärzte<br/><br/>Wählen Sie je nach Ihrem medizinischen Bedarf.',
    doctorGuide:
      '<b>So finden Sie einen Arzt:</b><br/>1. Wählen Sie eine Abteilung aus dem Dashboard<br/>2. Sehen Sie alle verfügbaren Ärzte in dieser Abteilung<br/>3. Überprüfen Sie ihre Qualifikationen und Erfahrung<br/>4. Lesen Sie ihre Spezialisierung<br/>5. Klicken Sie auf einen Arzt, um seine Verfügbarkeit zu sehen<br/><br/>Sie können Termine mit jedem verfügbaren Arzt buchen.',
    appointmentGuide:
      '<b>So buchen Sie einen Termin:</b><br/>1. Finden Sie Ihren bevorzugten Arzt und klicken Sie darauf<br/>2. Sehen Sie "Next 7 Days Availability"<br/>3. Wählen Sie ein Datum, das Ihnen passt<br/>4. Der Termin-Status zeigt verfügbare Zeitfenster an<br/>5. Klicken Sie auf "Book Now", um zu bestätigen<br/>6. Überprüfen Sie die Bestätigung in Ihrem Verlauf<br/><br/>Sie können jederzeit stornieren, wenn nötig.',
    historyGuide:
      '<b>So überprüfen Sie Ihre medizinische Geschichte:</b><br/>1. Klicken Sie auf "History" in der Navigation<br/>2. Sehen Sie alle Ihre früheren Termine<br/>3. Überprüfen Sie Ärzte-Notizen und Diagnosen<br/>4. Überprüfen Sie verschriebene Medikamente<br/>5. Exportieren Sie Ihren Verlauf als CSV<br/><br/>Bewahren Sie Ihre Unterlagen für zukünftige Referenzen auf.'
  },
  pt: {
    'Ask me anything...': 'Pergunte-me qualquer coisa...',
    'Complete Your Profile': 'Complete Seu Perfil',
    'Explore Departments': 'Explore Departamentos',
    'Find a Doctor': 'Encontre um Médico',
    'Book Appointment': 'Marcar Consulta',
    'Check My History': 'Ver Meu Histórico',
    profileGuide:
      '<b>Como completar seu perfil:</b><br/>1. Clique em "Edit Profile" no seu painel<br/>2. Preencha suas informações pessoais (Nome, Idade, Data de Nascimento)<br/>3. Selecione seu sexo e grupo sanguíneo<br/>4. Adicione seu endereço (opcional)<br/>5. Clique em "Save Changes"<br/><br/>Isso ajuda os médicos a entender melhor seu histórico médico.',
    departmentGuide:
      '<b>Como explorar departamentos:</b><br/>1. Vá ao seu Painel<br/>2. Você verá o card "Available Departments"<br/>3. Explore departamentos como Cardiologia, Neurologia, etc.<br/>4. Clique em "View Details" para ver especialistas<br/>5. Cada departamento tem médicos experientes<br/><br/>Escolha de acordo com sua necessidade médica.',
    doctorGuide:
      '<b>Como encontrar um médico:</b><br/>1. Selecione um departamento do painel<br/>2. Veja todos os médicos disponíveis nesse departamento<br/>3. Verifique suas qualificações e experiência<br/>4. Leia sua especialização<br/>5. Clique em um médico para ver sua disponibilidade<br/><br/>Você pode marcar consultas com qualquer médico disponível.',
    appointmentGuide:
      '<b>Como marcar uma consulta:</b><br/>1. Encontre e clique no seu médico preferido<br/>2. Veja "Next 7 Days Availability"<br/>3. Selecione uma data que funcione para você<br/>4. O status da consulta mostrará horários disponíveis<br/>5. Clique em "Book Now" para confirmar<br/>6. Verifique a confirmação no seu histórico<br/><br/>Você pode cancelar a qualquer momento se necessário.',
    historyGuide:
      '<b>Como verificar seu histórico médico:</b><br/>1. Clique em "History" na navegação<br/>2. Veja todas as suas consultas anteriores<br/>3. Verifique as anotações do médico e diagnósticos<br/>4. Verifique medicamentos prescritos<br/>5. Exporte seu histórico como CSV<br/><br/>Guarde seus registros com segurança para referência futura.'
  }
}

export default {
  name: 'AIAssistant',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      messages: [],
      userMessage: '',
      selectedLanguage: 'en',
      selectedAction: null,
      isLoading: false,
      messageId: 0,
      quickActions: [
        {
          id: 'profile',
          label: 'Complete Your Profile',
          icon: 'fas fa-user-edit',
          key: 'profileGuide'
        },
        {
          id: 'departments',
          label: 'Explore Departments',
          icon: 'fas fa-hospital',
          key: 'departmentGuide'
        },
        {
          id: 'doctor',
          label: 'Find a Doctor',
          icon: 'fas fa-stethoscope',
          key: 'doctorGuide'
        },
        {
          id: 'appointment',
          label: 'Book Appointment',
          icon: 'fas fa-calendar-check',
          key: 'appointmentGuide'
        },
        {
          id: 'history',
          label: 'Check My History',
          icon: 'fas fa-history',
          key: 'historyGuide'
        }
      ]
    }
  },
  mounted() {
    if (this.isOpen && this.messages.length === 0) {
      this.addMessage(
        'Hello! 👋 I\'m your AI Medical Assistant. I can guide you through our hospital management system. Select a quick guide below or ask me anything!',
        'assistant'
      )
    }
  },
  methods: {
    getTranslatedText(text) {
      if (text.includes('Guide:')) {
        return translations[this.selectedLanguage][text] || text
      }
      return translations[this.selectedLanguage][text] || text
    },

    handleQuickAction(action) {
      this.selectedAction = action.id
      const guidText = translations[this.selectedLanguage][action.key]
      this.addMessage(action.label, 'user')
      setTimeout(() => {
        this.addMessage(guidText, 'assistant')
      }, 500)
    },

    async sendMessage() {
      if (!this.userMessage.trim()) return

      const userMsg = this.userMessage
      this.addMessage(userMsg, 'user')
      this.userMessage = ''
      this.isLoading = true

      try {
        // TODO: Replace with Gemini API call
        // For now, using predefined responses
        const response = await this.getAIResponse(userMsg)
        setTimeout(() => {
          this.addMessage(response, 'assistant')
          this.isLoading = false
        }, 1000)
      } catch (error) {
        console.error('Error:', error)
        this.addMessage(
          'Sorry, I encountered an error. Please try again or select a quick guide above.',
          'assistant'
        )
        this.isLoading = false
      }
    },

    async getAIResponse(userMessage) {
      // TODO: Integrate Gemini API here
      // Example structure for Gemini API call:
      /*
      const response = await fetch('https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': YOUR_GEMINI_API_KEY
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `${userMessage} (Please respond in ${this.selectedLanguage === 'en' ? 'English' : this.selectedLanguage}. User is asking about a hospital management system with features for booking appointments, finding doctors, and checking medical history.)`
            }]
          }]
        })
      })
      
      const data = await response.json()
      return data.candidates[0].content.parts[0].text
      */

      // Fallback responses
      const lowerMessage = userMessage.toLowerCase()
      const responses = {
        en: {
          default:
            'I\'m here to help! Please select one of the quick guides above or ask me a specific question about booking appointments, finding doctors, or managing your profile.',
          profile: translations.en.profileGuide,
          department: translations.en.departmentGuide,
          doctor: translations.en.doctorGuide,
          appointment: translations.en.appointmentGuide,
          history: translations.en.historyGuide
        },
        hi: {
          default:
            'मैं आपकी मदद करने के लिए यहाँ हूँ! कृपया ऊपर दिए गए त्वरित मार्गदर्शन में से एक चुनें या मुझसे कोई विशिष्ट प्रश्न पूछें।',
          profile: translations.hi.profileGuide,
          department: translations.hi.departmentGuide,
          doctor: translations.hi.doctorGuide,
          appointment: translations.hi.appointmentGuide,
          history: translations.hi.historyGuide
        }
      }

      const activeResponses = responses[this.selectedLanguage] || responses.en

      if (
        lowerMessage.includes('profile') ||
        lowerMessage.includes('profi')
      ) {
        return activeResponses.profile
      } else if (
        lowerMessage.includes('department') ||
        lowerMessage.includes('depart')
      ) {
        return activeResponses.department
      } else if (lowerMessage.includes('doctor') || lowerMessage.includes('doc')) {
        return activeResponses.doctor
      } else if (
        lowerMessage.includes('appointment') ||
        lowerMessage.includes('appoint') ||
        lowerMessage.includes('book')
      ) {
        return activeResponses.appointment
      } else if (
        lowerMessage.includes('history') ||
        lowerMessage.includes('record')
      ) {
        return activeResponses.history
      }

      return activeResponses.default
    },

    addMessage(text, type) {
      this.messages.push({
        id: this.messageId++,
        text,
        type
      })
      this.$nextTick(() => {
        const messagesWrapper = document.querySelector('.messages-wrapper')
        if (messagesWrapper) {
          messagesWrapper.scrollTop = messagesWrapper.scrollHeight
        }
      })
    },

    formatMessage(text) {
      return text
        .replace(/\n/g, '<br/>')
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/__(.*?)__/g, '<u>$1</u>')
    },

    closeAssistant() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.ai-assistant-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.ai-assistant-modal {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 600px;
  height: 80vh;
  max-height: 800px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.assistant-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.ai-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.header-info h2 {
  font-size: 1.2rem;
  margin: 0;
  font-weight: 700;
}

.header-info p {
  font-size: 0.85rem;
  opacity: 0.9;
  margin: 0.25rem 0 0 0;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

/* Language Selector */
.language-selector {
  padding: 1rem 1.5rem;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.language-selector label {
  font-weight: 600;
  color: #2c3e50;
  white-space: nowrap;
}

.language-select {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  background: white;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s ease;
}

.language-select:hover {
  border-color: #667eea;
}

.language-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Quick Actions */
.quick-actions {
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.quick-actions h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.action-btn {
  padding: 0.75rem 1rem;
  background: #f0f2f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7f8c8d;
  white-space: nowrap;
}

.action-btn i {
  font-size: 1.2rem;
  color: #667eea;
}

.action-btn:hover {
  background: #e8eef7;
  border-color: #667eea;
  color: #667eea;
}

.action-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.action-btn.active i {
  color: white;
}

/* Chat Container */
.chat-container {
  flex: 1;
  display: flex;
  color: white;
  flex-direction: column;
  overflow: hidden;
}

.messages-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  justify-content: flex-start;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  display: flex;
  gap: 0.75rem;
  max-width: 85%;
  animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.assistant-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.message-text {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 0.95rem;
}

.message.assistant .message-text {
  background: #f0f2f9;
  color: #2c3e50;
}

.message.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-text p {
  margin: 0;
}

.message-text b {
  font-weight: 700;
}

.typing-indicator {
  display: flex;
  gap: 0.3rem;
  align-items: center;
  height: 1rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-10px);
  }
}

/* Input Area */
.input-area {
  padding: 1rem 1.5rem;
  background: white;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 0.75rem;
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  color: white;
  transition: all 0.3s ease;
}

.message-input:hover {
  border-color: #667eea;
}

.message-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.send-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-size: 1rem;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .ai-assistant-modal {
    max-width: 95vw;
    height: 90vh;
  }

  .assistant-header {
    padding: 1rem;
  }

  .header-info h2 {
    font-size: 1rem;
  }

  .header-info p {
    font-size: 0.75rem;
  }

  .ai-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
  }

  .action-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.7rem;
  }

  .message-content {
    max-width: 90%;
  }
}

@media (max-width: 480px) {
  .ai-assistant-modal {
    max-width: 100vw;
    height: 100vh;
    border-radius: 0;
  }

  .assistant-header {
    padding: 0.75rem 1rem;
  }

  .header-info h2 {
    font-size: 0.95rem;
  }

  .close-btn {
    width: 36px;
    height: 36px;
  }

  .language-selector {
    padding: 0.75rem 1rem;
  }

  .quick-actions {
    padding: 0.75rem 1rem;
  }

  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(75px, 1fr));
    gap: 0.5rem;
  }

  .action-btn {
    padding: 0.5rem 0.5rem;
    font-size: 0.65rem;
  }

  .action-btn i {
    font-size: 1rem;
  }

  .messages-wrapper {
    padding: 1rem;
    gap: 0.75rem;
  }

  .message-content {
    max-width: 95%;
  }

  .message-text {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }

  .input-area {
    padding: 0.75rem 1rem;
    gap: 0.5rem;
  }

  .message-input {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }

  .send-btn {
    width: 36px;
    height: 36px;
  }
}
</style>
