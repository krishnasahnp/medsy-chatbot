import React, { useState } from 'react';

const AppointmentWidget = () => {
    const [messages, setMessages] = useState([
        { id: 1, text: "I'll help you book an appointment. Let's start with your main concern. Please choose from the list or say it.", sender: 'bot', isSystem: true, options: ['General checkup', 'Fever/Cold', 'Headache'] }
    ]);
    const [selection, setSelection] = useState('');

    const handleOptionClick = (option) => {
        handleProcess(option);
    };

    const handleProcess = async (inputMsg) => {
        // Add user selection
        const userMsg = { id: messages.length + 1, text: inputMsg, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        
        try {
            const response = await fetch('/api/v1/appointments/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: inputMsg, user_id: 1 })
            });
            const data = await response.json();
            
            const botMsg = {
                id: messages.length + 2,
                text: data.response,
                sender: 'bot',
                options: data.options || [],
                state: data.state
            };
            setMessages(prev => [...prev, botMsg]);
            
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white p-4 max-w-lg mx-auto">
            <h2 className="text-xl font-bold mb-4 text-center text-medical-blue">Book an Appointment</h2>
            
            <div className="flex-1 overflow-y-auto space-y-4">
                {messages.map((msg) => (
                    <div key={msg.id} className="space-y-2">
                        <div className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-3 rounded-lg max-w-[80%] ${msg.sender === 'user' ? 'bg-gray-100' : 'bg-blue-50 border border-blue-100'}`}>
                                <p>{msg.text}</p>
                            </div>
                        </div>
                        {msg.options && msg.options.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                                {msg.options.map((opt, idx) => (
                                    <button 
                                        key={idx}
                                        onClick={() => handleOptionClick(opt)}
                                        className="px-3 py-1 bg-white border border-medical-blue text-medical-blue rounded-full text-sm hover:bg-blue-50 transition-colors"
                                    >
                                        {opt}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
                <p className="text-xs text-center text-gray-400">
                    Use quick options or switch to Chat for voice booking.
                </p>
            </div>
        </div>
    );
};

export default AppointmentWidget;
