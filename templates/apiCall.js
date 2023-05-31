function chat() {
  const user_input = document.getElementById('user-input').value;
  if (user_input.trim() !== "") {
    fetch('/process_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: user_input })
    })
    
    .then(response => response.json())
    .then(data => {
      const response = data?.response; // Add null check here
      const chatHistory = document.getElementById('chat-history');
      chatHistory.innerHTML += "<p><strong>You:</strong> " + user_input + "</p>";
      chatHistory.innerHTML += "<p><strong>AI:</strong> " + (response || "") + "</p>"; // Use empty string if response is null
      document.getElementById('user-input').value = "";
      document.getElementById('user-input').focus();
    })
    .catch(error => {
      console.log(error);
    });
  }
}
