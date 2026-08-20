# SmartTriage Hackathon Presentation Script

*(Time your reading to roughly 3 minutes depending on your presentation slot)*

**[Slide 1: Title & The Problem]**
"Hello judges, my name is Mahfuz, and I’m excited to present SmartTriage. Emergency departments around the world are facing a crisis. Patients routinely wait hours just to be seen by a triage nurse, leading to undocumented deterioration in the waiting room and severe cognitive burnout for clinical staff. We built SmartTriage to solve this."

**[Slide 2: The Solution - Show the Main Dashboard]**
"SmartTriage is an autonomous, AI-powered triage system that instantly categorizes patients upon arrival.
Here is the core dashboard used by ED staff. Let me show you how a patient is enrolled."

**[Slide 3: Voice Intake - Open Patient Registration Modal]**
"Normally, a nurse spends precious minutes typing patient details. With SmartTriage, a patient or clerk simply speaks their symptoms. *(Click the Voice Dictation Button)* Our system uses the latest Gemini multimodal models to parse the unstructured speech directly into a structured clinical JSON payload, instantly capturing chief complaints and vitals."

**[Slide 4: The Triage Engine Architecture]**
"The moment the patient is saved, our 3-layer AI engine kicks in.
First, a deterministic Rules Engine checks for critical red flags—like extremely low oxygen. If found, it routes them immediately, saving API tokens and ensuring safety.
Second, a Machine Learning Random Forest classifier calculates probabilities based on historical triage data.
Finally, an LLM acts as the explainability layer, synthesizing the ML output into a clear, clinical rationale for the doctor."

**[Slide 5: Show Patient Detail Page & Translation]**
"Let's look at a patient card. Here you see the AI confidence score and the clinical rationale. But we went further for patient equity. With a single click, we can translate this complex medical rationale into the patient's native language, empowering them to understand their own care plan."

**[Slide 6: Innovation - Hardware IoT Simulation]**
"Now, what about the waiting room? To prevent silent deterioration, we built the system to integrate directly with IoT edge devices. *(Open registration modal again, click 'Connect Oximeter')*. As you can see, the system is designed to stream live pulse and oxygen data directly from a wearable sensor while the patient waits."

**[Slide 7: Public Monitor & Privacy Mode - Show `/monitor` screen]**
"We also built a custom Big Screen Monitor view for the waiting room itself. *(Switch to `/monitor`)*. This gives patients peace of mind by showing live estimated wait times. Notice that all names and MRNs are automatically masked—this is our HIPAA-compliant Privacy Mode, proving our data handling is production-ready."

**[Slide 8: Business Model & Token Optimization - Click Analytics Modal]**
"Finally, the business side. SmartTriage is highly optimized. *(Click System Analytics button)*. As you can see on our Analytics dashboard, by intercepting critical patients with our Rules Engine, we save massive amounts of LLM tokens. Our blended cost per triage is less than a tenth of a cent, making our B2B SaaS model incredibly profitable and scalable for any hospital network."

**[Slide 9: Conclusion]**
"SmartTriage isn't just a prototype; it's fully dockerized and ready for real-world deployment. Thank you, and I’d be happy to answer any questions."
