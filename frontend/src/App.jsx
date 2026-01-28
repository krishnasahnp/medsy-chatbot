import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import AppointmentWidget from './components/AppointmentWidget';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [userName, setUserName] = useState(() => localStorage.getItem('medsy_user_name') || 'Santosh (Guest)');
  const [isEditingName, setIsEditingName] = useState(false);

  const handleNameSave = (e) => {
    if (e.key === 'Enter' || e.type === 'blur') {
      setIsEditingName(false);
      localStorage.setItem('medsy_user_name', userName);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800 font-sans">
      {/* Sidebar / Mobile Tab Bar */}
      <nav className="hidden md:flex flex-col w-64 bg-white border-r border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-medical-blue">Medsy</h1>
          <p className="text-sm text-gray-500">Medical Companion</p>
        </div>
        <ul className="flex-1 p-4 space-y-2">
          <li>
            <button 
              onClick={() => setActiveTab('chat')}
              className={`w-full text-left p-2 rounded-md ${activeTab === 'chat' ? 'bg-medical-blue text-white' : 'hover:bg-gray-100'}`}
            >
              Chat Assistant
            </button>
          </li>
          <li>
            <button 
              onClick={() => setActiveTab('appointments')}
              className={`w-full text-left p-2 rounded-md ${activeTab === 'appointments' ? 'bg-medical-blue text-white' : 'hover:bg-gray-100'}`}
            >
              Appointments
            </button>
          </li>
          <li>
            <button className="w-full text-left p-2 rounded-md hover:bg-gray-100 text-gray-400 cursor-not-allowed">
              Medical Records (Beta)
            </button>
          </li>
        </ul>
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center space-x-2 p-1 hover:bg-gray-50 rounded-lg transition-colors group">
            <div className="w-10 h-10 rounded-full bg-medical-blue/10 flex items-center justify-center text-medical-blue font-bold text-lg border border-medical-blue/20">
              {userName[0].toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              {isEditingName ? (
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  onKeyDown={handleNameSave}
                  onBlur={handleNameSave}
                  autoFocus
                  className="text-sm font-medium w-full bg-transparent border-b border-medical-blue focus:outline-none"
                />
              ) : (
                <div 
                  onClick={() => setIsEditingName(true)}
                  className="cursor-pointer"
                >
                  <p className="text-sm font-medium truncate group-hover:text-medical-blue transition-colors">{userName}</p>
                  <p className="text-[10px] text-gray-400">Click to edit profile</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full relative">
        {/* Mobile Header */}
        <header className="md:hidden h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 z-10 w-full fixed top-0 left-0">
          <h1 className="text-xl font-bold text-medical-blue">Medsy</h1>
          <button className="p-2 text-gray-600">
            {/* Hamburger Icon */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </header>

        {/* content container */}
        <div className="flex-1 overflow-hidden pt-16 md:pt-0">
          {activeTab === 'chat' && <ChatInterface />}
          {activeTab === 'appointments' && <AppointmentWidget />}
        </div>

        {/* Mobile Bottom Nav */}
        <div className="md:hidden h-16 bg-white border-t border-gray-200 flex justify-around items-center fixed bottom-0 left-0 w-full z-10">
           <button 
             onClick={() => setActiveTab('chat')}
             className={`flex flex-col items-center ${activeTab === 'chat' ? 'text-medical-blue' : 'text-gray-400'}`}
           >
             <span>Chat</span>
           </button>
           <button 
             onClick={() => setActiveTab('appointments')}
             className={`flex flex-col items-center ${activeTab === 'appointments' ? 'text-medical-blue' : 'text-gray-400'}`}
           >
             <span>Book</span>
           </button>
        </div>
      </main>
    </div>
  );
}

export default App;
