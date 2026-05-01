# Proxima LMSYS Chatbot Arena Integration Report

## Summary of Conversation and Tasks
You requested the integration of the LMSYS Chatbot Arena (chat.lmsys.org, now lmarena.ai) into the [Proxima](https://github.com/Zen4-bit/Proxima) project. Proxima is a local AI gateway that connects to multiple AI providers natively through browser sessions without requiring API keys.

You outlined a 5-phase plan:
1. **Reconnaissance & DOM Mapping:** Inspecting Gradio's dynamic DOM for inputs, buttons (TOS Agree, Send), and output areas.
2. **Building the Proxima Engine:** Creating a script to manage interactions (like `chatgpt-engine.js`). You initially suggested using Playwright for this.
3. **Handling the "A/B" Problem:** Structuring the engine to return JSON containing both Model A and Model B's outputs and wiring it into the MCP Tool configuration.
4. **Testing & Environment Deployment:** Visual and headless testing across different machines.
5. **The "Agentic" Polish:** Using a local model like Gemma 2 to summarize the differences between Model A and Model B.

You asked me to execute this within my environment and, if successful, provide a changelog to use later.

---

## Problems Encountered

During the **Phase 1 (Reconnaissance)** step, I attempted to use Headless Playwright within my sandbox environment to map the DOM of `lmarena.ai`. I encountered the following critical issues:

1. **Aggressive Bot Protection / Cloudflare:**
   When navigating to `https://lmarena.ai` via headless Playwright, the site failed to load the core Gradio application. Instead, it returned minimal HTML indicative of a Cloudflare block or a 404 error page.
   - *Evidence:* The `textarea` elements and chat UI components were completely absent from the DOM, and screenshots confirmed the site was blocking automated headless access.
2. **Incompatibility with Proxima's Architecture:**
   While your plan suggested instantiating a Playwright browser within the engine script (`engines/lmsys-engine.js`), **Proxima does not use Playwright**.
   - Proxima operates as an Electron app using `BrowserView` instances (managed in `Proxima/electron/browser-manager.cjs`).
   - Proxima relies on complex, pre-configured Electron browser sessions with custom headers, user agents, and Cloudflare bypass scripts (e.g., overriding `navigator.webdriver`, `WebGLRenderingContext`, etc.) to stay undetected.
   - Introducing Playwright would mean shipping a massive secondary browser binary alongside Electron, which breaks Proxima's lightweight design philosophy and bypasses its existing stealth capabilities.
3. **Hardware & Environment Limitations:**
   My environment runs strictly in an isolated, headless container. I cannot perform "visual debugging" (Phase 4) or spawn separate local models like Gemma 2 natively (Phase 5).

---

## Possible Solutions and Implementation Strategy

To successfully implement this on your local machine, you should pivot away from Playwright and build the integration entirely within Proxima's existing Electron `BrowserView` architecture.

Here is the exact roadmap to build this:

### 1. Register the New Provider
In `Proxima/electron/browser-manager.cjs`, add LMSYS to the `providers` object:
```javascript
lmsys: {
    url: 'https://lmarena.ai/',
    partition: 'persist:lmsys',
    color: '#ff5722'
}
```

### 2. Create the Electron Engine Script
Create `Proxima/electron/providers/lmsys-engine.js`. This script will be injected into the `BrowserView` context (just like `claude-engine.js`). It must interact directly with the DOM.

**Key DOM Logic for `lmsys-engine.js`:**
```javascript
(function() {
    if (window.__proximaLmsys) return;

    // 1. TOS Bypass
    async function acceptTOS() {
        const buttons = Array.from(document.querySelectorAll('button'));
        const agreeBtn = buttons.find(b => b.textContent.includes('Agree') || b.textContent.includes('Accept'));
        if (agreeBtn) agreeBtn.click();
    }

    // 2. Send Message
    async function send(message) {
        await acceptTOS();

        // Find input
        const textarea = document.querySelector('textarea');
        if (!textarea) throw new Error("Input not found");

        // Inject value (React/Gradio needs native event firing)
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
        nativeInputValueSetter.call(textarea, message);
        textarea.dispatchEvent(new Event('input', { bubbles: true }));

        // Find send button (look for the specific SVG path Gradio uses for send)
        const buttons = Array.from(document.querySelectorAll('button'));
        const sendBtn = buttons.find(b => b.innerHTML.includes('M5.5 10L7.25 12L5.5 14'));
        if (sendBtn) sendBtn.click();

        // 3. Polling for Completion
        return await pollForOutput();
    }

    // 4. Extracting Outputs
    async function pollForOutput() {
        return new Promise((resolve) => {
            let checks = 0;
            const interval = setInterval(() => {
                checks++;
                // Check if generation is done (e.g., stop button disappears, or send button reappears)
                const isGenerating = document.body.innerHTML.includes('Stop generating');

                if (!isGenerating && checks > 5) {
                    clearInterval(interval);
                    // Gradio text outputs are usually in markdown divs
                    const outputs = document.querySelectorAll('.prose, .markdown');
                    // Model A is usually outputs[0] or outputs[outputs.length - 2]
                    // Model B is usually outputs[1] or outputs[outputs.length - 1]

                    resolve(JSON.stringify({
                        model_a: outputs[outputs.length - 2]?.innerText || "No output",
                        model_b: outputs[outputs.length - 1]?.innerText || "No output"
                    }));
                }
            }, 1000);
        });
    }

    window.__proximaLmsys = { send };
})();
```

### 3. Wire into the Application
1. **API Endpoint (`Proxima/electron/rest-api.cjs`):** Update the API to accept `model: "lmsys"` and route it to `provider-api.cjs`.
2. **Provider API (`Proxima/electron/provider-api.cjs`):** Add logic to load the new `lmsys-engine.js` script.
3. **MCP Tool (`Proxima/src/mcp-server-v3.js`):** Register a new tool `compare_arena_models` that specifically queries `model: "lmsys"` and returns the JSON payload.

### Summary
Because `lmarena.ai` actively blocks headless bot requests and relies on complex Gradio WebSocket streaming, Proxima's existing **stealth Electron BrowserView** is the *only* viable way to scrape it reliably. By injecting pure JavaScript (`lmsys-engine.js`) into the page rather than using Playwright, you leverage Proxima's existing Cloudflare bypasses and maintain the app's architectural integrity.