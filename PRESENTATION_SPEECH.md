# SmartTriage Hackathon Presentation Script

*(Time your reading to roughly 3 to 4 minutes depending on your presentation slot)*

**[Slide 1: Title & The Problem]**
"Hello judges, my name is Mahfuz, and I’m excited to present SmartTriage. Emergency departments around the world are facing a severe crisis. Patients routinely wait hours just to be seen by a triage nurse, leading to undocumented deterioration in the waiting room and severe cognitive burnout for clinical staff. We built SmartTriage to solve this bottleneck permanently."

**[Slide 2: The Solution - Show the Main Dashboard]**
"SmartTriage is an autonomous, AI-powered triage system that instantly categorizes patients upon arrival. And by the way, what you are looking at is not a local prototype—this is fully Dockerized and deployed live in production on a DigitalOcean droplet. 

Here is the core dashboard used by ED staff. Let me show you how a patient is enrolled."

**[Slide 3: Voice Intake & IoT - Open Patient Registration Modal]**
"Normally, a nurse spends precious minutes typing patient details. With SmartTriage, a patient or clerk simply speaks their symptoms. *(Click the Voice Dictation Button)* Our system uses Gemini multimodal AI to parse unstructured speech directly into a clinical JSON payload. 

But what about vitals? To prevent silent deterioration, we built the system to integrate directly with IoT edge devices. *(Click 'Connect Oximeter')*. The system streams live pulse and oxygen data directly from a wearable sensor while the patient waits."

**[Slide 4: The Triage Engine Architecture]**
"The moment the patient is saved, our 3-layer AI engine kicks in.
First, a deterministic **Rules Engine** checks for critical red flags—like extremely low oxygen. If found, it routes them immediately, saving API tokens and ensuring clinical safety.
Second, a **Machine Learning Random Forest** classifier calculates probabilities based on historical triage data.
Finally, an **LLM** acts as the explainability layer, synthesizing the ML output into a clear, clinical rationale for the doctor."

**[Slide 5: Translation & Patient Equity - Show Patient Detail Page]**
"Let's look at a patient card. Here you see the AI confidence score and the clinical rationale. But we went further for patient equity. With a single click, we can translate this complex medical rationale into the patient's native language, empowering them to understand their own care plan."

**[Slide 6: Disaster Preparedness - Click the MCI Mode Button]**
"Emergency departments also face mass casualty events. *(Click MCI Mode)*. With one click, SmartTriage instantly switches the entire hospital to Mass Casualty Incident mode, hiding non-essential data and converting the board to massive, high-contrast triage tags (Immediate, Delayed, Minor) so staff can operate at lightning speed."

**[Slide 7: Public Monitor & Privacy Mode - Show `/monitor` screen]**
"We also built a custom Big Screen Monitor view for the waiting room itself. *(Switch to `/monitor`)*. This gives patients peace of mind by showing live estimated wait times. Notice that all names are automatically masked—this is our HIPAA-compliant Privacy Mode, proving our data handling is production-ready."

**[Slide 8: Business Model & Token Optimization - Click Analytics Modal]**
"Finally, the business side. SmartTriage is highly optimized. *(Click System Analytics button)*. As you can see, by intercepting critical patients with our Rules Engine, we bypass the LLM entirely for obvious cases. This brings our blended API cost to less than a tenth of a cent per triage, making our SaaS model incredibly profitable."

**[Slide 9: Conclusion]**
"SmartTriage is fast, safe, cost-effective, and live right now. Thank you, and I’d be happy to answer any questions."
