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
                intent: data.intent,
                options: data.options || [],
                state: data.state
            };
            setMessages(prev => [...prev, botMsg]);
            
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-white p-4 w-full">
            <h2 className="text-2xl font-bold mb-6 text-center text-medical-blue border-b pb-4 mt-16 md:mt-0">Book an Appointment</h2>
            
            <div className="flex-1 overflow-y-auto space-y-4 pb-20">
                {messages.map((msg) => (
                    <div key={msg.id} className="space-y-2">
                        <div className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-4 rounded-xl shadow-sm max-w-[85%] ${
                                msg.sender === 'user' 
                                    ? 'bg-medical-blue text-white rounded-tr-none' 
                                    : 'bg-blue-50/50 border border-blue-100 text-gray-800 rounded-tl-none'
                            }`}>
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
                                    <div className="mt-4 bg-gray-50 border border-gray-200 rounded-xl p-4 shadow-sm overflow-hidden relative text-gray-800">
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
                                    </div>
                                )}

                                {/* Interactive Upload Prompt */}
                                {msg.intent?.is_upload_prompt && (
                                    <div className="mt-4 p-4 bg-white/10 border border-dashed border-white/40 rounded-xl text-center">
                                        <button 
                                            onClick={() => document.getElementById('wigdet-report-upload').click()}
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
                            </div>
                        </div>
                        {msg.options && msg.options.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                                {msg.options.map((opt, idx) => (
                                    <button 
                                        key={idx}
                                        onClick={() => handleOptionClick(opt)}
                                        className="px-4 py-2 bg-white border border-medical-blue text-medical-blue rounded-full text-sm font-medium hover:bg-medical-blue hover:text-white transition-all shadow-sm"
                                    >
                                        {opt}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
                <div className="h-20" /> {/* Spacer for mobile nav */}
            </div>

            {/* Hidden File Input */}
            <input 
                id="wigdet-report-upload" 
                type="file" 
                className="hidden" 
                onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                        const fileMsg = {
                            id: Date.now(),
                            text: `Uploaded: ${file.name}`,
                            sender: 'user',
                            fileData: {
                                name: file.name,
                                size: (file.size / 1024).toFixed(1) + ' KB'
                            }
                        };
                        setMessages(prev => [...prev, fileMsg]);
                        
                        setTimeout(() => {
                            handleProcess("See Summary");
                        }, 800);
                    }
                }} 
            />

            <div className="mt-4 pt-4 border-t border-gray-100">
                <p className="text-xs text-center text-gray-400">
                    Use quick options or switch to Chat for voice booking.
                </p>
            </div>
        </div>
    );
};

export default AppointmentWidget;
