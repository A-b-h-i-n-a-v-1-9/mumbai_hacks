const BACKEND_URL = "http://127.0.0.1:8000/analyze_text";

async function getSelectedTextFromTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return "";

  const [injectionResult] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => window.getSelection().toString()
  });

  return injectionResult?.result || "";
}

document.getElementById("scanBtn").addEventListener("click", async () => {
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = "Analyzing…";

  let text = document.getElementById("input").value.trim();
  if (!text) {
    text = await getSelectedTextFromTab();
  }

  if (!text) {
    resultDiv.textContent = "No text selected or pasted.";
    return;
  }

  try {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("user_id", "chrome_extension");
    formData.append("platform", "chrome");

    const resp = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    if (!resp.ok) {
      resultDiv.textContent = `Backend error: ${resp.status}`;
      return;
    }

    const data = await resp.json();
    const { score = 0, risk = "low", highlights = [] } = data;

    let html = `<strong>Risk:</strong> ${risk.toUpperCase()} (${score.toFixed(
      2
    )}%)<br/>`;

    if (highlights.length) {
      html += "<strong>Signals:</strong><ul>";
      for (const h of highlights.slice(0, 5)) {
        html += `<li><code>${h.span}</code> (${h.type})</li>`;
      }
      html += "</ul>";
    }

    resultDiv.innerHTML = html;
  } catch (err) {
    console.error(err);
    resultDiv.textContent = "Error talking to Scamp backend.";
  }
});
