from gtts import gTTS

text="""Bento Africa Temporarily Halts Operations: Bento Africa has suspended its operations after rehiring staff to handle a backlog of tasks. This comes after the company faced protests over delayed January salaries.  
    Marasoft Denies Fraud Allegations: Marasoft has denied fraud allegations but failed to provide evidence, blaming "disgruntled" ex-employees for the claims.  
    Nigerian Fintechs Revamp Operations: Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures following a 2024 ban.  
    Lemfi Acquires Bureau Buttercrane: Lemfi has completed the acquisition of Irish currency exchange Bureau Buttercrane, marking its entry into the European market.  
    NIBSS Bets on QR Codes: The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  
    Safaricom and Kenyan Banks Propose Pesalink: Safaricom and Kenyan commercial banks are pushing for Pesalink to overhaul the national payment system.  
    Moniepoint Mirrors Jack Dorsey's Square: Moniepoint has launched a new POS system inspired by Jack Dorsey's Square.  
    Stitch Acquires ExiPay: South African fintech Stitch has acquired ExiPay to expand into in-person payments."""
tts = gTTS(text, lang='en', tld='com.ng')
tts.save("output-test.mp3")