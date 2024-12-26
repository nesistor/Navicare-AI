import { useState } from "react";
const ChatBox = ({ onSendMessage }) => {
    const [message, setMessage] = useState("");
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (message.trim()) {
        onSendMessage(message);
  
        try {
          const response = await fetch("http://localhost:5000/api/send-message", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
          });
          const result = await response.json();
          console.log("Message sent to backend:", result);
        } catch (error) {
          console.error("Error sending message to backend:", error);
        }
  
        setMessage("");
      }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <textarea
            className="form-control"
            placeholder="Type your prompt here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows="4"
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Send
        </button>
      </form>
    );
  };
  
  export default ChatBox;
  