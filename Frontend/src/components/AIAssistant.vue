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
          <i class="fas fa-times">❌</i>
        </button>
      </div>

      <div class="language-selector">
        <label>Select Language:</label>
        <select v-model="selectedLanguage" class="language-select">
          <option value="en">English</option>
          <option value="hi">Hindi (हिंदी)</option>
          <option value="od">Odia (ଓଡ଼ିଆ)</option>
          <option value="ta">Tamil (தமிழ்)</option>
          <option value="te">Telugu (తెలుగు)</option>
          <option value="ml">Malayalam (മലയാളം)</option>
          <option value="bn">Bengali (বাংলা)</option>
        </select>
      </div>

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
  od: {
    'Ask me anything...': 'ମୋତେ ଯେକୌଣସି ପ୍ରଶ୍ନ ପୁଛ...',
    'Complete Your Profile': 'ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ ସମ୍ପୂର୍ଣ୍ଣ କରନ୍ତୁ',
    'Explore Departments': 'ବିଭାଗଗୁଡ଼ିକ ଅନ୍ବେଷଣ କରନ୍ତୁ',
    'Find a Doctor': 'ଜଣେ ଡାକ୍ତର ଖୋଜନ୍ତୁ',
    'Book Appointment': 'ଅପଏଣ୍ଟମେଣ୍ଟ ବୁକ କରନ୍ତୁ',
    'Check My History': 'ମୋ ଇତିହାସ ଯାଞ୍ଚ କରନ୍ତୁ',
    profileGuide:
      '<b>ଆପଣଙ୍କ ପ୍ରୋଫାଇଲ କିପରି ସମ୍ପୂର୍ଣ୍ଣ କରବେ:</b><br/>1. ଆପଣଙ୍କ ଡ୍ୟାସବୋର୍ଡରୁ "Edit Profile" ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/>2. ଆପଣଙ୍କ ବ୍ୟକ୍ତିଗତ ସୂଚନା ଭର୍ତ୍ତି କରନ୍ତୁ (ନାମ, ବୟସ, ଜନ୍ମତାରିଖ)<br/>3. ଆପଣଙ୍କ ଲିଙ୍ଗ ଏବଂ ରକ୍ତ ଗୋଷ୍ଠୀ ବାଛନ୍ତୁ<br/>4. ଆପଣଙ୍କ ଠିକାଣା ଯୋଗ କରନ୍ତୁ (ଐଚ୍ଛିକ)<br/>5. "Save Changes" ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/><br/>ଏହା ଡାକ୍ତରମାନଙ୍କୁ ଆପଣଙ୍କ ଚିକିତ୍ସା ପଟଭୂମି ଭଲ ବୁझିବାରେ ସାହାଯ୍ୟ କରେ।',
    departmentGuide:
      '<b>ବିଭାଗଗୁଡ଼ିକ କିପରି ଅନ୍ବେଷଣ କରବେ:</b><br/>1. ଆପଣଙ୍କ ଡ୍ୟାସବୋର୍ଡକୁ ଯାଆନ୍ତୁ<br/>2. ଆପେ "Available Departments" କାର୍ଡ ଦେଖିବେ<br/>3. କାର୍ଡିଓଲୋଜି, ନ୍ୟୁରୋଲୋଜି ଆଦି ବିଭାଗ ବ୍ରାଉଜ କରନ୍ତୁ<br/>4. ବିଶେଷଜ୍ଞ ଦେଖିବା ପାଇଁ "View Details" ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/>5. ପ୍ରତ୍ୟେକ ବିଭାଗରେ ବିଶେଷଜ୍ଞ ଡାକ୍ତର ଅଛନ୍ତି<br/><br/>ଆପଣଙ୍କ ଚିକିତ୍ସା ଆବଶ୍ୟକତା ଅନୁସାରେ ବାଛନ୍ତୁ।',
    doctorGuide:
      '<b>ଜଣେ ଡାକ୍ତର କିପରି ଖୋଜିବେ:</b><br/>1. ଡ୍ୟାସବୋର୍ଡରୁ ଏକ ବିଭାଗ ବାଛନ୍ତୁ<br/>2. ସେହି ବିଭାଗରେ ସମସ୍ତ ଉପଲବ୍ଧ ଡାକ୍ତର ଦେଖନ୍ତୁ<br/>3. ତାଙ୍କର ଯୋଗ୍ୟତା ଏବଂ ଅଭିଜ୍ଞତା ପରୀକ୍ଷା କରନ୍ତୁ<br/>4. ତାଙ୍କର ବିଶେଷତ୍ବ ପଢ଼ନ୍ତୁ<br/>5. ସେମାନଙ୍କ ଉପଲବ୍ଧତା ଦେଖିବା ପାଇଁ ଡାକ୍ତର ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/><br/>ଆପେ ଯେକୌଣସି ଉପଲବ୍ଧ ଡାକ୍ତରଙ୍କ ସହ ଅପଏଣ୍ଟମେଣ୍ଟ ବୁକ କରିପାରିବେ।',
    appointmentGuide:
      '<b>ଅପଏଣ୍ଟମେଣ୍ଟ କିପରି ବୁକ କରବେ:</b><br/>1. ଆପଣଙ୍କ ପସନ୍ଦର ଡାକ୍ତର ଖୋଜନ୍ତୁ ଏବଂ ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/>2. "Next 7 Days Availability" ଦେଖନ୍ତୁ<br/>3. ଆପଣଙ୍କ ପାଇଁ ଉପଯୁକ୍ତ ଏକ ତାରିଖ ବାଛନ୍ତୁ<br/>4. ଅପଏଣ୍ଟମେଣ୍ଟ ସ୍ଥିତି ଉପଲବ୍ଧ ସ୍ଲଟ ଦେଖାଇବ<br/>5. ନିଶ୍ଚିତ କରିବାକୁ "Book Now" ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/>6. ଆପଣଙ୍କ ଇତିହାସରେ ନିଶ୍ଚିତକରଣ ଯାଞ୍ଚ କରନ୍ତୁ<br/><br/>ଆବଶ୍ୟକ ହେଲେ ଆପେ ଯେକୌଣସି ସମୟରେ ରଦ୍ଦ କରିପାରିବେ।',
    historyGuide:
      '<b>ଆପଣଙ୍କ ଚିକିତ୍ସା ଇତିହାସ କିପରି ଯାଞ୍ଚ କରବେ:</b><br/>1. ନେଭିଗେସନ ଠାରୁ "History" ଉପରେ କ୍ଲିକ କରନ୍ତୁ<br/>2. ଆପଣଙ୍କ ସମସ୍ତ ପୂର୍ବତନ ଅପଏଣ୍ଟମେଣ୍ଟ ଦେଖନ୍ତୁ<br/>3. ଡାକ୍ତରଙ୍କ ଟିପ୍ପଣୀ ଏବଂ ରୋଗ ନିର୍ଣ୍ଣୟ ଯାଞ୍ଚ କରନ୍ତୁ<br/>4. ନିର୍ଦ୍ଧାରିତ ଔଷଧ ଯାଞ୍ଚ କରନ୍ତୁ<br/>5. ଆପଣଙ୍କ ଇତିହାସ CSV ଭାବରେ ରପ୍ତାନି କରନ୍ତୁ<br/><br/>ଭବିଷ୍ୟତ ରେଫରେନ୍ସ ପାଇଁ ଆପଣଙ୍କ ରେକର୍ଡ ସୁରକ୍ଷିତ ରଖନ୍ତୁ।'
  },
  ta: {
    'Ask me anything...': 'எனக்கு எதையும் கேளுங்கள்...',
    'Complete Your Profile': 'உங்கள் சுயவிவரத்தை முடிக்கவும்',
    'Explore Departments': 'விभагங்களை ஆராயுங்கள்',
    'Find a Doctor': 'ஒரு மருத்துவரை தேடுங்கள்',
    'Book Appointment': 'சந்திப்பை பதிவு செய்யுங்கள்',
    'Check My History': 'என் வரலாற்றை பார்க்கவும்',
    profileGuide:
      '<b>உங்கள் சுயவிவரத்தை முடிக்கவும்:</b><br/>1. உங்கள் டாஷ்போர்டில் "Edit Profile" ஐ கிளிக் செய்யுங்கள்<br/>2. உங்கள் ব்যक்তিগত தகவல் (பெயர், வயது, பிறந்த திகதி)<br/>3. உங்கள் பாலினம் மற்றும் இரத்த குழு தேர்வு செய்யுங்கள்<br/>4. உங்கள் முகவரி சேர்க்கவும் (விரும்பினால்)<br/>5. "Save Changes" ஐ கிளிக் செய்யுங்கள்<br/><br/>இது மருத்துவர்களுக்கு உங்கள் மருத்துவ பின்னணியை நன்கு புரிந்துகொள்ள உதவுகிறது.',
    departmentGuide:
      '<b>விभагங்களை ஆராயுங்கள்:</b><br/>1. உங்கள் டாஷ்போர்டுக்கு செல்லுங்கள்<br/>2. நீங்கள் "Available Departments" கார்டைக் காணலாம்<br/>3. கர்டியோலஜி, நியுரோலஜி போன்ற விभागங்களை ஏட்டவும்<br/>4. நிபுணர்களைக் காண "View Details" ஐ கிளிக் செய்யுங்கள்<br/>5. ஒவ்வொரு விभாகத்திலும் திறமைசாலி மருத்துவர் உள்ளனர்<br/><br/>உங்கள் மருத்துவ தேவையைப் பொறுத்து தேர்வு செய்யுங்கள்.',
    doctorGuide:
      '<b>ஒரு மருத்துவரை தேடுங்கள்:</b><br/>1. டாஷ்போர்டிலிருந்து ஒரு விभாகத்தை தேர்வு செய்யுங்கள்<br/>2. அந்த விभாகத்தில் உள்ள அனைத்து கிடைக்கக்கூடிய மருத்துவர்களைக் காணுங்கள்<br/>3. அவர்களின் தகுதி மற்றும் அனுபவத்தை சரிபார்க்கவும்<br/>4. அவர்களின் சிறப்பு நிபுணத்தைப் படிக்கவும்<br/>5. அவர்களின் கிடைக்கின்ற நேரத்தைக் காண மருத்துவரைக் கிளிக் செய்யுங்கள்<br/><br/>நீங்கள் கிடைக்கக்கூடிய எந்த மருத்துவரிடனும் சந்திப்பை பதிவு செய்யலாம்.',
    appointmentGuide:
      '<b>சந்திப்பை பதிவு செய்யுங்கள்:</b><br/>1. உங்களுக்கு விருப்பமான மருத்துவரைக் கண்டுபிடித்து கிளிக் செய்யுங்கள்<br/>2. "Next 7 Days Availability" ஐக் காணுங்கள்<br/>3. உங்களுக்கு பொருத்தமான ஒரு தேதியைத் தேர்வு செய்யுங்கள்<br/>4. சந்திப்பு நிலை கிடைக்கக்கூடிய சறுக்கைகளைக் காட்டும்<br/>5. உறுதிப்படுத்த "Book Now" ஐ கிளிக் செய்யுங்கள்<br/>6. உங்கள் வரலாற்றில் உறுதிப்படுத்தலைச் சரிபார்க்கவும்<br/><br/>தேவைப்பட்டால் நீங்கள் எப்போதும் ரத்து செய்யலாம்.',
    historyGuide:
      '<b>உங்கள் மருத்துவ வரலாற்றை சரிபார்க்கவும்:</b><br/>1. நேவிகேஷன் থেকে "History" ஐ கிளிக் செய்யுங்கள்<br/>2. உங்கள் அனைத்து முந்தைய சந்திப்புகளைக் காணுங்கள்<br/>3. மருத்துவரின் குறிப்புகள் மற்றும் நோயறிதல்களைக் சரிபார்க்கவும்<br/>4. பரிந்துரைக்கப்பட்ட மருந்துகளைச் சரிபார்க்கவும்<br/>5. உங்கள் வரலாற்றை CSV என்ற கோப்பாக ஏற்றுமதி செய்யுங்கள்<br/><br/>ভবிষ்যত ঋபேற்றுதலுக்காக உங்கள் வாழ்க்கைப்பதிவுகளை பாதுக்காப்பாக வைத்திருக்கவும்.'
  },
  te: {
    'Ask me anything...': 'నన్నుండి ఏదైనా అడగండి...',
    'Complete Your Profile': 'మీ ప్రొఫైల్‌ను పూర్తి చేయండి',
    'Explore Departments': 'విభాగాలను అన్వేషించండి',
    'Find a Doctor': 'డాక్టర్‌ను కనుగొనండి',
    'Book Appointment': 'అపాయింట్‌మెంట్‌ను బుక్ చేయండి',
    'Check My History': 'నా చరిత్రను చూడండి',
    profileGuide:
      '<b>మీ ప్రొఫైల్‌ను పూర్తి చేయండి:</b><br/>1. మీ డ్యాష్‌బోర్డ్ నుండి "Edit Profile" ను క్లిక్ చేయండి<br/>2. మీ వ్యక్తిగత సమాచారాన్ని (పేరు, వయస్సు, జన్మ తేదీ)<br/>3. మీ లింగం మరియు రక్త సమూహాన్ని ఎంచుకోండి<br/>4. మీ చిరునామాను జోడించండి (ఐచ్ఛికం)<br/>5. "Save Changes" ను క్లిక్ చేయండి<br/><br/>ఇది వైద్యులకు మీ వైద్య చరిత్రను బాగా అర్థం చేసుకోవడానికి సహాయపడుతుంది.',
    departmentGuide:
      '<b>విభాగాలను అన్వేషించండి:</b><br/>1. మీ డ్యాష్‌బోర్డ్‌కు వెళ్లండి<br/>2. మీరు "Available Departments" కార్డ్‌ను చూస్తారు<br/>3. కార్డియాలజీ, న్యూరాలజీ వంటి విభాగాలను విహారణ చేయండి<br/>4. నిపుణులను చూడటానికి "View Details" ను క్లిక్ చేయండి<br/>5. ప్రతి విభాగానికి నిపుణ వైద్యులు ఉన్నారు<br/><br/>మీ వైద్య అవసరం ఆధారంగా ఎంచుకోండి.',
    doctorGuide:
      '<b>డాక్టర్‌ను కనుగొనండి:</b><br/>1. డ్యాష్‌బోర్డ్ నుండి విభాగాన్ని ఎంచుకోండి<br/>2. ఆ విభాగంలో అందుబాటులో ఉన్న విశేష వైద్యులన్నింటిని చూడండి<br/>3. వారి అర్హతలు మరియు అనుభవాన్ని సరిచేయండి<br/>4. వారి ప్రత్యేకత చదవండి<br/>5. వారి లభ్యతను చూడటానికి వైద్యుడిని క్లిక్ చేయండి<br/><br/>మీరు అందుబాటులో ఉన్న ఏదైనా డాక్టర్‌తో అపాయింట్‌మెంట్‌ను బుక్ చేయవచ్చు.',
    appointmentGuide:
      '<b>అపాయింట్‌మెంట్‌ను బుక్ చేయండి:</b><br/>1. మీకు నచ్చిన డాక్టర్‌ను కనుగొనండి మరియు క్లిక్ చేయండి<br/>2. "Next 7 Days Availability" చూడండి<br/>3. మీకు సరిపోయే తేదీని ఎంచుకోండి<br/>4. అపాయింట్‌మెంట్ స్థితి లభ్యమైన స్లాట్‌లను చూపుతుంది<br/>5. ఖాయం చేయడానికి "Book Now" ను క్లిక్ చేయండి<br/>6. మీ చరిత్రలో ఖాయం చేయడాన్ని సరిచేయండి<br/><br/>అవసరమైతే మీరు ఎప్పుడైనా రద్దు చేయవచ్చు.',
    historyGuide:
      '<b>మీ వైద్య చరిత్రను చూడండి:</b><br/>1. నావిగేషన్ నుండి "History" ను క్లిక్ చేయండి<br/>2. మీ అన్ని చేసిన అపాయింట్‌మెంట్‌లను చూడండి<br/>3. డాక్టర్ నోట్‌లు మరియు రోగ నిర్ధారణలను సరిచేయండి<br/>4. సూచించిన ఔషధాలను సరిచేయండి<br/>5. మీ చరిత్రను CSV గా ఎగుమతి చేయండి<br/><br/>భవిష్యత్ సూచన కోసం మీ రికార్డ్‌లను సురక్షితంగా ఉంచండి.'
  },
  ml: {
    'Ask me anything...': 'എന്നോട് എന്തെങ്കിലും ചോദിക്കുക...',
    'Complete Your Profile': 'നിങ്ങളുടെ പ്രൊഫൈൽ പൂർത്തിയാക്കുക',
    'Explore Departments': 'വിഭാഗങ്ങൾ പര്യവേക്ഷണം ചെയ്യുക',
    'Find a Doctor': 'ഒരു ഡോക്ടർ കണ്ടെത്തുക',
    'Book Appointment': 'നിയമനം ബുക്ക് ചെയ്യുക',
    'Check My History': 'എന്റെ ചരിത്രം പരിശോധിക്കുക',
    profileGuide:
      '<b>നിങ്ങളുടെ പ്രൊഫൈൽ പൂർത്തിയാക്കുക:</b><br/>1. നിങ്ങളുടെ ഡാഷ്ബോർഡിൽ "Edit Profile" ക്ലിക്ക് ചെയ്യുക<br/>2. നിങ്ങളുടെ വ്യക്തിഗത വിവരങ്ങൾ (പേര്, പ്രായം, ജനനത്തീയതി)<br/>3. നിങ്ങളുടെ ലിംഗം, രക്തഗ്രൂപ്പ് തിരഞ്ഞെടുക്കുക<br/>4. നിങ്ങളുടെ വിലാസം ചേർക്കുക (ഐച്ഛികം)<br/>5. "Save Changes" ക്ലിക്ക് ചെയ്യുക<br/><br/>ഇത് ഡോക്ടർമാരെ നിങ്ങളുടെ മെഡിക്കൽ പശ്ചാത്തലം നന്നായി മനസ്സിലാക്കാൻ സഹായിക്കുന്നു.',
    departmentGuide:
      '<b>വിഭാഗങ്ങൾ പര്യവേക്ഷണം ചെയ്യുക:</b><br/>1. നിങ്ങളുടെ ഡാഷ്ബോർഡിലേക്ക് പോകുക<br/>2. നിങ്ങൾ "Available Departments" കാർഡ് കാണും<br/>3. കാർഡിയോളജി, ന്യൂറോളജി തുടങ്ങിയ വിഭാഗങ്ങൾ ബ്രൗസ് ചെയ്യുക<br/>4. വിശേഷജ്ഞരെ കാണാൻ "View Details" ക്ലിക്ക് ചെയ്യുക<br/>5. ഓരോ വിഭാഗത്തിലും നിപുണ ഡോക്ടരുമാരുണ്ട്<br/><br/>നിങ്ങളുടെ മെഡിക്കൽ ആവശ്യം അനുസരിച്ച് തിരഞ്ഞെടുക്കുക.',
    doctorGuide:
      '<b>ഒരു ഡോക്ടർ കണ്ടെത്തുക:</b><br/>1. ഡാഷ്ബോർഡിൽ നിന്ന് ഒരു വിഭാഗം തിരഞ്ഞെടുക്കുക<br/>2. ആ വിഭാഗത്തിലെ ലഭ്യമായ എല്ലാ ഡോക്ടറുമാരെ കാണുക<br/>3. അവരുടെ യോഗ്യതകൾ, അനുഭവം പരിശോധിക്കുക<br/>4. അവരുടെ പ്രത്യേകത വായിക്കുക<br/>5. അവരുടെ ലഭ്യത കാണാൻ ഡോക്ടരിനെ ക്ലിക്ക് ചെയ്യുക<br/><br/>നിങ്ങൾക്ക് ലഭ്യമായ ഏത് ഡോക്ടരുമായും നിയമനം ബുക്ക് ചെയ്യാൻ കഴിയും.',
    appointmentGuide:
      '<b>നിയമനം ബുക്ക് ചെയ്യുക:</b><br/>1. നിങ്ങൾ ഇഷ്ടപ്പെട്ട ഡോക്ടരിനെ കണ്ടെത്തി ക്ലിക്ക് ചെയ്യുക<br/>2. "Next 7 Days Availability" കാണുക<br/>3. നിങ്ങൾക്ക് അനുയോജ്യമായ ഒരു തീയതി തിരഞ്ഞെടുക്കുക<br/>4. നിയമന അവസ്ഥ ലഭ്യ സ്ലോട്ടുകൾ കാണിക്കും<br/>5. സ്ഥിരീകരിക്കാൻ "Book Now" ക്ലിക്ക് ചെയ്യുക<br/>6. നിങ്ങളുടെ ചരിത്രത്തിൽ സ്ഥിരീകരണം പരിശോധിക്കുക<br/><br/>ആവശ്യമെങ്കിൽ നിങ്ങൾ ഏത് സമയത്തും റദ്ദ് ചെയ്യാൻ കഴിയും.',
    historyGuide:
      '<b>നിങ്ങളുടെ മെഡിക്കൽ ചരിത്രം പരിശോധിക്കുക:</b><br/>1. നാവിഗേഷനിൽ നിന്ന് "History" ക്ലിക്ക് ചെയ്യുക<br/>2. നിങ്ങളുടെ എല്ലാ മുൻകാല നിയമനങ്ങൾ കാണുക<br/>3. ഡോക്ടരുടെ കുറിപ്പുകൾ, രോഗനിർണ്ണയം പരിശോധിക്കുക<br/>4. നിർദ്ദേശിത മരുന്നുകൾ പരിശോധിക്കുക<br/>5. നിങ്ങളുടെ ചരിത്രം CSV ആയി എഴുതുക<br/><br/>ഭാവിഷ്യത്തിലെ റഫറൻസിനായി നിങ്ങളുടെ രേഖകൾ സുരക്ഷിതമായി സൂക്ഷിക്കുക.'
  },
  bn: {
    'Ask me anything...': 'আমাকে যেকোনো প্রশ্ন করুন...',
    'Complete Your Profile': 'আপনার প্রোফাইল সম্পূর্ণ করুন',
    'Explore Departments': 'বিভাগ অন্বেষণ করুন',
    'Find a Doctor': 'একজন ডাক্তার খুঁজুন',
    'Book Appointment': 'অ্যাপয়েন্টমেন্ট বুক করুন',
    'Check My History': 'আমার ইতিহাস পরীক্ষা করুন',
    profileGuide:
      '<b>আপনার প্রোফাইল সম্পূর্ণ করুন:</b><br/>1. আপনার ড্যাশবোর্ড থেকে "Edit Profile" ক্লিক করুন<br/>2. আপনার ব্যক্তিগত তথ্য পূরণ করুন (নাম, বয়স, জন্ম তারিখ)<br/>3. আপনার লিঙ্গ এবং রক্তের গ্রুপ নির্বাচন করুন<br/>4. আপনার ঠিকানা যোগ করুন (ঐচ্ছিক)<br/>5. "Save Changes" ক্লিক করুন<br/><br/>এটি ডাক্তারদের আপনার চিকিৎসা পটভূমি ভালভাবে বুঝতে সাহায্য করে।',
    departmentGuide:
      '<b>বিভাগ অন্বেষণ করুন:</b><br/>1. আপনার ড্যাশবোর্ডে যান<br/>2. আপনি "Available Departments" কার্ড দেখতে পাবেন<br/>3. কার্ডিওলজি, নিউরোলজি ইত্যাদি বিভাগ ব্রাউজ করুন<br/>4. বিশেষজ্ঞ দেখতে "View Details" ক্লিক করুন<br/>5. প্রতিটি বিভাগে অভিজ্ঞ ডাক্তার রয়েছে<br/><br/>আপনার চিকিৎসা প্রয়োজন অনুযায়ী বেছে নিন।',
    doctorGuide:
      '<b>একজন ডাক্তার খুঁজুন:</b><br/>1. ড্যাশবোর্ড থেকে একটি বিভাগ নির্বাচন করুন<br/>2. সেই বিভাগে সকল উপলব্ধ ডাক্তার দেখুন<br/>3. তাদের যোগ্যতা এবং অভিজ্ঞতা যাচাই করুন<br/>4. তাদের বিশেষত্ব পড়ুন<br/>5. তাদের উপলব্ধতা দেখতে ডাক্তারে ক্লিক করুন<br/><br/>আপনি কোনো উপলব্ধ ডাক্তারের সাথে অ্যাপয়েন্টমেন্ট বুক করতে পারেন।',
    appointmentGuide:
      '<b>অ্যাপয়েন্টমেন্ট বুক করুন:</b><br/>1. আপনার পছন্দের ডাক্তার খুঁজুন এবং ক্লিক করুন<br/>2. "Next 7 Days Availability" দেখুন<br/>3. আপনার জন্য উপযুক্ত একটি তারিখ নির্বাচন করুন<br/>4. অ্যাপয়েন্টমেন্ট স্ট্যাটাস উপলব্ধ স্লট দেখাবে<br/>5. নিশ্চিত করতে "Book Now" ক্লিক করুন<br/>6. আপনার ইতিহাসে নিশ্চিতকরণ যাচাই করুন<br/><br/>প্রয়োজনে আপনি যেকোনো সময় বাতিল করতে পারেন।',
    historyGuide:
      '<b>আপনার চিকিৎসা ইতিহাস পরীক্ষা করুন:</b><br/>1. নেভিগেশন থেকে "History" ক্লিক করুন<br/>2. আপনার সমস্ত পূর্ববর্তী অ্যাপয়েন্টমেন্ট দেখুন<br/>3. ডাক্তারের নোট এবং রোগ নির্ণয় পরীক্ষা করুন<br/>4. নির্ধারিত ওষুধ পরীক্ষা করুন<br/>5. আপনার ইতিহাস CSV হিসাবে রপ্তানি করুন<br/><br/>ভবিষ্যত রেফারেন্সের জন্য আপনার রেকর্ড নিরাপদে রাখুন.'
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
  background: #fffdf7;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 700px;
  height: 80vh;
  max-height: 850px;
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
  background: #f4e9db;
  color: #3d362f;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #dacbb8;
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
  background: linear-gradient(135deg, #8f7b65 0%, #a68a72 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.header-info h2 {
  font-size: 1.2rem;
  margin: 0;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.header-info p {
  font-size: 0.85rem;
  color: #7d6d5f;
  margin: 0.25rem 0 0 0;
}

.close-btn {
  background: none;
  border: none;
  color: #3d362f;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(143, 123, 101, 0.1);
}

.close-btn:hover {
  background: rgba(143, 123, 101, 0.2);
  transform: rotate(90deg);
}

/* Language Selector */
.language-selector {
  padding: 1rem 1.5rem;
  background: #f2e8d8;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #d8c8b0;
}

.language-selector label {
  font-weight: 700;
  color: #3d362f;
  white-space: nowrap;
}

.language-select {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 2px solid #d8c8b0;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.95rem;
  background: #fff9f1;
  color: #3d362f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.language-select:hover {
  border-color: #8f7b65;
}

.language-select:focus {
  outline: none;
  border-color: #8f7b65;
  box-shadow: 0 0 0 3px rgba(143, 123, 101, 0.15);
}

/* Quick Actions */
.quick-actions {
  padding: 1rem 1.5rem;
  background: #fffdf7;
  border-bottom: 1px solid #d8c8b0;
  flex-shrink: 0;
  overflow-y: auto;
  max-height: 140px;
}

.quick-actions h3 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #3d362f;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
}

.action-btn {
  padding: 0.75rem 0.85rem;
  background: #f0e5d8;
  border: 1px solid #d8c8b0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.7rem;
  font-weight: 700;
  color: #7d6d5f;
  word-wrap: break-word;
  overflow-wrap: break-word;
  text-align: center;
  min-height: 80px;
  justify-content: center;
  line-height: 1.2;
}

.action-btn i {
  font-size: 1.2rem;
  color: #8f7b65;
}

.action-btn:hover {
  background: #e6d9c8;
  border-color: #8f7b65;
  color: #8f7b65;
}

.action-btn.active {
  background: linear-gradient(135deg, #8f7b65 0%, #a68a72 100%);
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
  max-width: 80%;
  animation: messageSlide 0.3s ease;
  flex-wrap: wrap;
  align-items: flex-start;
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
  background: linear-gradient(135deg, #8f7b65 0%, #a68a72 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.message-text {
  padding: 0.75rem 1rem;
  border-radius: 16px;
  line-height: 1.5;
  font-size: 0.95rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
}

.message.assistant .message-text {
  background: #f0e5d8;
  color: #3d362f;
}

.message.user .message-text {
  background: linear-gradient(135deg, #8f7b65 0%, #a68a72 100%);
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
  background: #8f7b65;
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
  background: #fffdf7;
  border-top: 1px solid #d8c8b0;
  display: flex;
  gap: 0.75rem;
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #d8c8b0;
  border-radius: 16px;
  font-family: inherit;
  font-size: 0.95rem;
  color: #3d362f;
  background: #fff9f1;
  transition: all 0.3s ease;
}

.message-input::placeholder {
  color: #bfafa1;
}

.message-input:hover {
  border-color: #8f7b65;
}

.message-input:focus {
  outline: none;
  border-color: #8f7b65;
  box-shadow: 0 0 0 3px rgba(143, 123, 101, 0.15);
}

.send-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #8f7b65 0%, #a68a72 100%);
  color: white;
  border: none;
  border-radius: 12px;
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
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
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
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  }

  .action-btn {
    padding: 0.5rem 0.65rem;
    font-size: 0.65rem;
    min-height: 75px;
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
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .action-btn {
    padding: 0.5rem 0.4rem;
    font-size: 0.6rem;
    min-height: 70px;
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
