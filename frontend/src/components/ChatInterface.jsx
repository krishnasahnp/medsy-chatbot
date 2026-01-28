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
                            <p>{msg.text}</p>
                            
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
                        onChange={(e) => alert('Report uploaded successfully!')} 
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
