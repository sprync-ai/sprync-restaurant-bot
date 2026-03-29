const { useState, useEffect, useRef, useCallback } = React;

function App() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            role: 'bot',
            content: '🍽️ Welcome to The Golden Plate! I\'m your booking assistant.\n\nHow can I help you today?',
            timestamp: new Date(),
            quickReplies: ['Book a Table', 'View Menu', 'Contact Info']
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId] = useState(Math.random().toString(36).substring(7));
    const messagesEndRef = useRef(null);
    const chatInputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = useCallback(async (text) => {
        if (!text.trim()) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: text,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    user_message: text,
                    conversation_history: messages.map(m => ({
                        role: m.role,
                        content: m.content,
                        timestamp: m.timestamp
                    }))
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get response');
            }

            const data = await response.json();

            const botMessage = {
                id: Date.now() + 1,
                role: 'bot',
                content: data.bot_message,
                timestamp: new Date(),
                quickReplies: data.quick_replies || [],
                isBookingConfirmed: data.is_booking_confirmed,
                bookingReference: data.booking_reference
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
            const errorMessage = {
                id: Date.now() + 1,
                role: 'bot',
                content: '❌ Sorry, I encountered an error. Please try again.',
                timestamp: new Date(),
                quickReplies: []
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
            chatInputRef.current?.focus();
        }
    }, [messages, sessionId]);

    const handleSendClick = () => {
        sendMessage(inputValue);
    };

    const handleQuickReply = (reply) => {
        sendMessage(reply);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(inputValue);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-white">
            {/* Header */}
            <div className="golden-gradient text-white shadow-lg">
                <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                            <span className="text-2xl">🍽️</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold">The Golden Plate</h1>
                            <p className="text-sm text-blue-100">AI Restaurant Booking</p>
                        </div>
                    </div>
                    <div className="text-right text-sm">
                        <p className="accent-gold">Powered by Sprync AI</p>
                        <p className="text-blue-200">London</p>
                    </div>
                </div>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto chat-container px-4 py-6">
                <div className="max-w-4xl mx-auto space-y-4">
                    {messages.map((message) => (
                        <div key={message.id} className="message-fade-in">
                            {message.role === 'user' ? (
                                // User Message
                                <div className="flex justify-end">
                                    <div className="max-w-xs lg:max-w-md bg-blue-500 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-md">
                                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                                        <p className="text-xs text-blue-100 mt-1 text-right">
                                            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </p>
                                    </div>
                                </div>
                            ) : (
                                // Bot Message
                                <div className="flex justify-start">
                                    <div className="max-w-xs lg:max-w-md">
                                        <div className="bg-white rounded-2xl rounded-tl-none px-4 py-3 shadow-md border border-gray-200">
                                            <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{message.content}</p>
                                            <p className="text-xs text-gray-500 mt-1">
                                                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </p>

                                            {/* Booking Confirmation Alert */}
                                            {message.isBookingConfirmed && message.bookingReference && (
                                                <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                                                    <p className="text-xs font-semibold text-green-800">
                                                        Reference: {message.bookingReference}
                                                    </p>
                                                </div>
                                            )}

                                            {/* Quick Replies */}
                                            {message.quickReplies && message.quickReplies.length > 0 && (
                                                <div className="mt-3 flex flex-wrap gap-2">
                                                    {message.quickReplies.map((reply, idx) => (
                                                        <button
                                                            key={idx}
                                                            onClick={() => handleQuickReply(reply)}
                                                            className="text-xs px-3 py-2 bg-blue-50 text-blue-600 rounded-full border border-blue-200 hover:bg-blue-100 transition-colors font-medium"
                                                        >
                                                            {reply}
                                                        </button>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}

                    {/* Typing Indicator */}
                    {isLoading && (
                        <div className="flex justify-start message-fade-in">
                            <div className="bg-white rounded-2xl rounded-tl-none shadow-md border border-gray-200">
                                <div className="typing-indicator">
                                    <div className="typing-dot"></div>
                                    <div className="typing-dot"></div>
                                    <div className="typing-dot"></div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 bg-white px-4 py-4 shadow-lg">
                <div className="max-w-4xl mx-auto">
                    <div className="flex gap-3 items-end">
                        <textarea
                            ref={chatInputRef}
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message..."
                            className="message-input flex-1 border border-gray-300 rounded-2xl px-4 py-3 text-sm focus:outline-none resize-none"
                            rows="1"
                            disabled={isLoading}
                        />
                        <button
                            onClick={handleSendClick}
                            disabled={isLoading || !inputValue.trim()}
                            className="golden-gradient text-white rounded-full p-3 hover:shadow-lg transition-shadow disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-2 text-center">
                        Powered by Sprync AI | Open: 11:00 AM - 11:00 PM Daily
                    </p>
                </div>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
