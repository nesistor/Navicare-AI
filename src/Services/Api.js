const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      try {
        const response = await fetch("http://localhost:5000/your-endpoint", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        });
  
        if (!response.ok) {
          throw new Error("Failed to send message to backend");
        }
  
        const data = await response.json();
        // Handle the response data (e.g., set the chat state)
        console.log(data);
      } catch (error) {
        console.error("Error sending message to backend:", error);
      }
    }
  };
  