import React, { useState, useEffect, useRef } from 'react';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { id: 1, text: "Hello! I'm Medsy, your medical companion. How are you feeling today?", sender: 'bot', timestamp: new Date() }
    ]);
    const [inputText, setInputText] = useState('');
    const [isListening, setIsListening] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        const newUserMsg = { 
            id: messages.length + 1, 
            text: inputText, 
            sender: 'user', 
            timestamp: new Date() 
        };
        
        setMessages(prev => [...prev, newUserMsg]);
        setInputText('');

        // Call API
        try {
            const response = await fetch('/api/v1/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: newUserMsg.text, user_id: 1 })
            });
            const data = await response.json();
            
            const botMsg = {
                id: messages.length + 2,
                text: data.response,
                sender: 'bot',
                isEmergency: data.is_emergency,
                intent: data.intent,
                options: data.intent?.options || [],
                timestamp: new Date()
            };
            setMessages(prev => [...prev, botMsg]);
            
        } catch (error) {
            console.error("Error sending message:", error);
            const errorMsg = {
                id: messages.length + 2,
                text: "Sorry, I'm having trouble connecting to the server.",
                sender: 'bot',
                isError: true,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMsg]);
        }
    };

    const toggleListening = () => {
        if (isListening) {
            setIsListening(false);
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Your browser does not support Speech Recognition. Please try Chrome or Edge.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            setIsListening(true);
        };

        recognition.onresult = (event) => {
            const speechToText = event.results[0][0].transcript;
            setInputText(speechToText);
            setIsListening(false);
            
            // Auto-submit after voice input
            setTimeout(() => {
                document.getElementById('chat-submit-btn')?.click();
            }, 500);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            setIsListening(false);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognition.start();
    };

    return (
        <div className="flex flex-col h-full bg-white relative">
            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-20">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
                        <div 
                            className={`max-w-[80%] md:max-w-[70%] p-4 rounded-2xl shadow-lg backdrop-blur-md text-sm md:text-base transition-all hover:scale-[1.02]
                            ${msg.sender === 'user' 
                                ? 'bg-medical-blue/90 text-white rounded-tr-none border border-white/20' 
                                : msg.isEmergency 
                                    ? 'bg-emergency-red/90 text-white border border-red-400/50'
                                    : 'bg-white/70 text-gray-800 rounded-tl-none border border-gray-100'
                            }`}
                        >
                            {msg.fileData ? (
                                <div className="flex items-center space-x-3 bg-white/10 p-3 rounded-xl border border-white/20">
                                    <div className="p-2 bg-white/20 rounded-lg">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium truncate">{msg.fileData.name}</p>
                                        <p className="text-[10px] opacity-70">{msg.fileData.size} • Uploaded successfully</p>
                                    </div>
                                    <div className="text-green-400">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                        </svg>
                                    </div>
                                </div>
                            ) : (
                                <p>{msg.text}</p>
                            )}
                            
                            {/* Modern Appointment Summary Card */}
                            {msg.intent?.is_summary && msg.intent?.booking_data && (
                                <div className="mt-4 bg-gray-50 border border-gray-200 rounded-xl p-4 shadow-sm overflow-hidden relative">
                                    <div className="absolute top-0 right-0 p-2 opacity-10">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-900" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                    </div>
                                    <div className="flex items-center space-x-2 mb-3">
                                        <span className="bg-medical-blue text-white text-[10px] px-2 py-0.5 rounded-full uppercase tracking-widest font-bold">Confirmed</span>
                                        <span className="text-gray-400 text-[10px] font-mono">ID: {msg.intent.booking_data.id}</span>
                                    </div>
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter">Patient:</span>
                                            <span className="text-gray-800 font-semibold text-sm">{msg.intent.booking_data.patient_name}</span>
                                        </div>
                                        <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter">Physician:</span>
                                            <span className="text-gray-800 font-semibold text-sm">{msg.intent.booking_data.doctor}</span>
                                        </div>
                                        <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter">Reason:</span>
                                            <span className="text-gray-800 font-medium text-sm">{msg.intent.booking_data.problem}</span>
                                        </div>
                                        <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter">Schedule:</span>
                                            <span className="text-gray-800 font-medium text-sm">{msg.intent.booking_data.date} at {msg.intent.booking_data.time}</span>
                                        </div>
                                        <div className="flex flex-col pt-1">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter mb-1">Clinic Location:</span>
                                            <div className="flex items-start space-x-1">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-medical-blue mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                                </svg>
                                                <span className="text-gray-700 text-xs leading-tight">{msg.intent.booking_data.location}</span>
                                            </div>
                                        </div>
                                        <div className="flex justify-between items-center pt-2">
                                            <span className="text-gray-500 text-[11px] uppercase tracking-tighter">Reports Attached:</span>
                                            <span className={`text-[11px] px-2 py-0.5 rounded-full font-bold ${msg.intent.booking_data.has_reports ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                                                {msg.intent.booking_data.has_reports ? 'YES' : 'NONE'}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="mt-4 pt-3 border-t border-gray-100 text-center">
                                        <p className="text-[10px] text-gray-400 italic">Medsy Medical Assistant - Healthcare in your pocket</p>
                                    </div>
                                </div>
                            )}

                            {/* Interactive Upload Prompt */}
                            {msg.intent?.is_upload_prompt && (
                                <div className="mt-4 p-4 bg-white/10 border border-dashed border-white/40 rounded-xl text-center">
                                    <button 
                                        onClick={() => document.getElementById('report-upload').click()}
                                        className="flex flex-col items-center justify-center w-full space-y-2 py-4 hover:bg-white/5 transition-colors group"
                                    >
                                        <div className="p-3 bg-medical-blue rounded-full group-hover:scale-110 transition-transform shadow-lg">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                            </svg>
                                        </div>
                                        <span className="text-sm font-semibold text-white">Upload Prescription / Report</span>
                                        <span className="text-[10px] text-white/60">PDF, JPG, or PNG (Max 10MB)</span>
                                    </button>
                                </div>
                            )}

                            {msg.options && msg.options.length > 0 && (
                                <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-white/10">
                                    {msg.options.map((opt, idx) => (
                                        <button 
                                            key={idx}
                                            onClick={() => {
                                                setInputText(opt);
                                                setTimeout(() => {
                                                    document.getElementById('chat-submit-btn')?.click();
                                                }, 100);
                                            }}
                                            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-colors border
                                                ${(msg.sender === 'user' || msg.isEmergency)
                                                    ? 'bg-white/20 hover:bg-white/30 text-white border-white/10' 
                                                    : 'bg-medical-blue/10 hover:bg-medical-blue/20 text-medical-blue border-medical-blue/20'
                                                }`}
                                        >
                                            {opt}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                        <span className="text-[10px] mt-1 px-2 opacity-60 text-gray-500">
                            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="absolute bottom-16 md:bottom-0 w-full bg-white border-t border-gray-200 p-4">
                <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
                    {/* Attachment Button */}
                    <button 
                        type="button" 
                        onClick={() => document.getElementById('report-upload').click()}
                        className="p-3 bg-gray-100 text-gray-500 rounded-full hover:bg-gray-200"
                        title="Upload Medical Reports"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                    </button>
                    <input 
                        id="report-upload" 
                        type="file" 
                        className="hidden" 
                        onChange={(e) => {
                            const file = e.target.files[0];
                            if (file) {
                                // Add a visual "File Upload" message from the user
                                const fileMsg = {
                                    id: Date.now(),
                                    text: `Uploaded: ${file.name}`,
                                    sender: 'user',
                                    fileData: {
                                        name: file.name,
                                        size: (file.size / 1024).toFixed(1) + ' KB'
                                    },
                                    timestamp: new Date()
                                };
                                setMessages(prev => [...prev, fileMsg]);
                                
                                // Auto-trigger summary transition
                                setTimeout(() => {
                                    setInputText("See Summary");
                                    setTimeout(() => {
                                        document.getElementById('chat-submit-btn')?.click();
                                    }, 100);
                                }, 800);
                            }
                        }} 
                    />

                    <button 
                        type="button" 
                        onClick={toggleListening}
                        className={`p-3 rounded-full transition-colors ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'}`}
                    >
                        {/* Mic Icon */}
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                        </svg>
                    </button>
                    <input 
                        type="text" 
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type a message..." 
                        className="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-medical-blue focus:border-transparent"
                    />
                    <button 
                        id="chat-submit-btn"
                        type="submit" 
                        disabled={!inputText.trim()}
                        className="p-3 bg-medical-blue text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {/* Send Icon */}
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
