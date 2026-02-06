const generateButton = document.getElementById("generate");
const player = document.getElementById("player");
const capOutput = document.getElementById("cap-output");

const buildCapPayload = () => {
  return {
    identifier: `alert-${Date.now()}`,
    sender: "local-emergency-system",
    sent: new Date().toISOString(),
    status: "Actual",
    msgType: "Alert",
    scope: "Public",
    info: {
      category: ["Safety"],
      event: "Emergency Alert",
      urgency: document.getElementById("urgency").value,
      severity: document.getElementById("severity").value,
      certainty: document.getElementById("certainty").value,
      headline: document.getElementById("headline").value,
      description: document.getElementById("text").value,
      instruction: document.getElementById("instruction").value,
      language: document.getElementById("language").value,
    },
  };
};

const decodeAudio = (base64) => {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
};

generateButton.addEventListener("click", async () => {
  const text = document.getElementById("text").value.trim();
  const language = document.getElementById("language").value.trim();
  if (!text) {
    capOutput.textContent = "Please enter a message to synthesize.";
    return;
  }

  capOutput.textContent = "Generating audio...";
  const response = await fetch("/api/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language, cap: buildCapPayload() }),
  });

  if (!response.ok) {
    capOutput.textContent = "Failed to generate audio.";
    return;
  }

  const data = await response.json();
  const bytes = decodeAudio(data.audio_wav_base64);
  const blob = new Blob([bytes], { type: "audio/wav" });
  player.src = URL.createObjectURL(blob);
  capOutput.textContent = JSON.stringify(data.cap, null, 2);
});
