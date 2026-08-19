document.addEventListener('DOMContentLoaded', () => {
    // Removed direct API calls due to CORS/Proxy limitations
    // App will now use local backend endpoints again

    // Navigation Logic
    const navLinks = document.querySelectorAll('.nav-links li');
    const views = document.querySelectorAll('.view');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            views.forEach(v => v.classList.remove('active-view'));

            link.classList.add('active');
            const targetId = link.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active-view');
        });
    });

    // Chat Helper
    function addChatMessage(text, sender) {
        const chatOutput = document.getElementById('chat-output');
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        msgDiv.textContent = text;
        chatOutput.appendChild(msgDiv);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    // Chat Logic
    const chatBtn = document.getElementById('chat-btn');
    const chatInput = document.getElementById('chat-input');

    chatBtn.addEventListener('click', async () => {
        const text = chatInput.value.trim();
        if (!text) return;
        
        addChatMessage(text, 'user');
        chatInput.value = '';
        
        chatBtn.disabled = true;
        chatBtn.textContent = '...';

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: text })
            });
            const data = await res.json();
            if (data.response) {
                addChatMessage(data.response, 'ai');
            } else {
                addChatMessage("Error connecting to AI.", 'ai');
            }
        } catch (e) {
            addChatMessage("Network error.", 'ai');
        } finally {
            chatBtn.disabled = false;
            chatBtn.textContent = 'Send';
        }
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') chatBtn.click();
    });

    // Visual Gen Logic
    const visualBtn = document.getElementById('visual-btn');
    const visualInput = document.getElementById('visual-input');
    const visualOutput = document.getElementById('visual-output');

    visualBtn.addEventListener('click', () => {
        const text = visualInput.value.trim();
        if (!text) return;

        visualOutput.innerHTML = '<div class="placeholder-text">Generating visual...</div>';
        visualBtn.disabled = true;

        visualOutput.innerHTML = `<img src="/api/visual?prompt=${encodeURIComponent(text)}" alt="Generated Visual" onload="document.getElementById('visual-btn').disabled=false" onerror="this.outerHTML='<div class=\\'placeholder-text\\'>Failed to load visual.</div>'; document.getElementById('visual-btn').disabled=false">`;
    });

    // Code Explainer Logic
    const codeBtn = document.getElementById('code-btn');
    const codeInput = document.getElementById('code-input');
    const codeResult = document.getElementById('code-result-text');

    codeBtn.addEventListener('click', async () => {
        const code = codeInput.value.trim();
        if (!code) return;

        codeResult.textContent = 'Analyzing code... please wait.';
        codeBtn.disabled = true;

        const prompt = `Please explain the following code and add comments:\n\`\`\`python\n${code}\n\`\`\``;

        try {
            const res = await fetch('/api/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });
            const data = await res.json();
            
            if (data.response) {
                codeResult.textContent = data.response;
            } else {
                codeResult.textContent = 'Error parsing response.';
            }
        } catch (e) {
            codeResult.textContent = 'Network error during analysis.';
        } finally {
            codeBtn.disabled = false;
        }
    });
});
