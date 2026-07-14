document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('tweetInput').value.trim();
    const resultContainer = document.getElementById('resultContainer');
    const sentimentResult = document.getElementById('sentimentResult');
    const btn = document.getElementById('analyzeBtn');

    if (!text) {
        alert('Please enter some text first!');
        return;
    }

    // Set Loading State
    btn.innerText = 'Analyzing...';
    btn.disabled = true;
    btn.classList.add('opacity-75', 'cursor-not-allowed');

    try {
        // Diarahkan ke port 8000 (FastAPI default)
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        
        if (response.ok) {
            resultContainer.classList.remove('hidden');
            sentimentResult.innerText = data.sentiment;

            // Reset kelas warna
            resultContainer.className = "mt-6 p-5 rounded-lg border text-center transition-all duration-300 ";

            // Pewarnaan dinamis berdasarkan label (0: Bearish, 1: Bullish, 2: Neutral)
            if (data.label === 1) {
                resultContainer.classList.add('bg-green-50', 'border-green-300', 'text-green-800');
            } else if (data.label === 0) {
                resultContainer.classList.add('bg-red-50', 'border-red-300', 'text-red-800');
            } else {
                resultContainer.classList.add('bg-gray-50', 'border-gray-300', 'text-gray-700');
            }
        } else {
            // FastAPI biasanya mengirim error detail dalam properti 'detail'
            alert('Error: ' + (data.detail || data.error));
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the backend server. Make sure backend/app.py is running on port 8000!');
    } finally {
        // Reset Button State
        btn.innerText = 'Analyze Sentiment';
        btn.disabled = false;
        btn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
});