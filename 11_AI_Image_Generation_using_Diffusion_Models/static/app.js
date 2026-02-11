/* -------------------------------------------------------------------
   AI Image Studio — Frontend Logic
   ------------------------------------------------------------------- */

(function () {
  "use strict";

  // ── DOM handles ───────────────────────────────────────────────────
  const $  = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  const form            = $("#gen-form");
  const promptEl        = $("#prompt");
  const negativeEl      = $("#negative");
  const modelEl         = $("#model");
  const guidanceEl      = $("#guidance");
  const guidanceVal     = $("#guidance-val");
  const stepsEl         = $("#steps");
  const stepsVal        = $("#steps-val");
  const btnGenerate     = $("#btn-generate");
  const btnCancel       = $("#btn-cancel");
  const resultArea      = $("#result-area");
  const placeholder     = $("#result-placeholder");
  const spinner         = $("#spinner");
  const resultWrapper   = $("#result-wrapper");
  const resultImg       = $("#result-img");
  const resultTime      = $("#result-time");
  const resultDownload  = $("#result-download");
  const galleryGrid     = $("#gallery-grid");
  const deviceBadge     = $("#device-badge");
  const deviceLabel     = $("#device-label");
  const lightbox        = $("#lightbox");
  const lightboxImg     = $("#lightbox-img");
  const lightboxDownload = $("#lightbox-download");
  const toastContainer  = $("#toast-container");

  // Model download elements
  const btnDownloadModel       = $("#btn-download-model");
  const btnCancelDownload      = $("#btn-cancel-download");
  const modelStatusBadge       = $("#model-status-badge");
  const downloadProgressContainer = $("#download-progress-container");
  const downloadProgressFill   = $("#download-progress-fill");
  const downloadProgressText   = $("#download-progress-text");

  // Model download status cache
  let modelStatuses = {};
  let downloadingModelId = null;
  let downloadAbortController = null;

  // ── Slider live values ────────────────────────────────────────────
  guidanceEl.addEventListener("input", () => {
    guidanceVal.textContent = parseFloat(guidanceEl.value).toFixed(1);
  });
  stepsEl.addEventListener("input", () => {
    stepsVal.textContent = stepsEl.value;
  });

  // ── Toast helper ──────────────────────────────────────────────────
  function toast(message, type = "error") {
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = message;
    toastContainer.appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transition = "opacity .3s";
      setTimeout(() => el.remove(), 300);
    }, 5000);
  }

  // ── Fetch helpers ─────────────────────────────────────────────────
  async function fetchJSON(url, opts = {}) {
    const res = await fetch(url, opts);
    const data = await res.json();
    if (!res.ok) throw data;
    return data;
  }

  // ── Load device info ──────────────────────────────────────────────
  async function loadDevice() {
    try {
      const info = await fetchJSON("/api/device");
      const isCPU = info.device === "cpu";
      deviceLabel.textContent = isCPU
        ? info.name
        : `${info.name} • ${info.vram_gb} GB`;
      if (isCPU) deviceBadge.classList.add("cpu");
    } catch {
      deviceLabel.textContent = "Unknown device";
    }
  }

  // ── Load models ───────────────────────────────────────────────────
  async function loadModels() {
    try {
      const models = await fetchJSON("/api/models");
      modelEl.innerHTML = "";
      models.forEach((m) => {
        const opt = document.createElement("option");
        opt.value = m.id;
        opt.textContent = `${m.name}  (${m.vram})`;
        if (m.default) opt.selected = true;
        modelEl.appendChild(opt);
      });
      // After loading models, check their download status
      loadModelStatus();
    } catch {
      toast("Failed to load models list");
    }
  }

  // ── Model download status ─────────────────────────────────────────
  async function loadModelStatus() {
    try {
      modelStatuses = await fetchJSON("/api/model-status");
      updateModelBadge();
    } catch {
      // Non-critical, skip
    }
  }

  function updateModelBadge() {
    const currentModel = modelEl.value;
    const isDownloaded = modelStatuses[currentModel];
    const isDownloading = downloadingModelId === currentModel;

    if (isDownloading) {
      modelStatusBadge.textContent = "Downloading…";
      modelStatusBadge.className = "model-status-badge downloading";
      btnDownloadModel.textContent = "Downloading…";
      btnDownloadModel.disabled = true;
      btnDownloadModel.classList.add("downloading");
      btnDownloadModel.classList.remove("ready");
      btnCancelDownload.style.display = "inline-flex";
      return;
    }

    if (isDownloaded) {
      modelStatusBadge.textContent = "✓ Downloaded • Available";
      modelStatusBadge.className = "model-status-badge downloaded";
      btnDownloadModel.textContent = "✓ Available";
      btnDownloadModel.disabled = true;
      btnDownloadModel.classList.add("ready");
      btnDownloadModel.classList.remove("downloading");
      btnCancelDownload.style.display = "none";
    } else {
      modelStatusBadge.textContent = "Not downloaded";
      modelStatusBadge.className = "model-status-badge not-downloaded";
      btnDownloadModel.innerHTML = '<span class="dl-icon">⬇</span> Download Model';
      btnDownloadModel.disabled = false;
      btnDownloadModel.classList.remove("ready");
      btnDownloadModel.classList.remove("downloading");
      btnCancelDownload.style.display = "none";
    }
  }

  // Update badge when model selection changes
  modelEl.addEventListener("change", () => {
    updateModelBadge();
  });

  // ── Model download ────────────────────────────────────────────────
  btnDownloadModel.addEventListener("click", async () => {
    const modelId = modelEl.value;
    if (downloadingModelId) return;

    downloadAbortController = new AbortController();
    downloadingModelId = modelId;
    updateModelBadge();
    downloadProgressContainer.style.display = "flex";
    downloadProgressFill.classList.remove("error");
    downloadProgressFill.style.width = "0%";
    downloadProgressText.textContent = "Starting…";

    try {
      const response = await fetch("/api/download-model", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_id: modelId }),
        signal: downloadAbortController.signal,
      });
      if (!response.ok || !response.body) {
        throw new Error("Unable to start model download.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let downloadFailed = false;
      let failureMessage = "Model download failed.";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop(); // keep incomplete chunk

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const event = JSON.parse(line.slice(6));
              if (event.progress >= 0) {
                // Animate the progress bar smoothly
                const pct = Math.min(event.progress, 100);
                downloadProgressFill.style.width = pct + "%";
                downloadProgressText.textContent = event.status || `${pct}%`;
              } else {
                // Error
                downloadFailed = true;
                failureMessage = event.status || "Download failed";
                downloadProgressFill.style.width = "0%";
                downloadProgressFill.classList.add("error");
                downloadProgressText.textContent = "Failed";
              }
            } catch {
              // Malformed JSON, ignore
            }
          }
        }
      }

      // Check if download succeeded
      if (!downloadFailed && downloadProgressFill.style.width === "100%") {
        toast("Model downloaded successfully!", "success");
        modelStatuses[modelId] = true;
        downloadProgressText.textContent = "Downloaded";
        updateModelBadge();

        // Hide progress after a moment
        setTimeout(() => {
          downloadProgressContainer.style.display = "none";
          downloadProgressFill.style.width = "0%";
        }, 2000);
      } else if (downloadFailed) {
        toast(failureMessage);
        setTimeout(() => {
          downloadProgressContainer.style.display = "none";
          downloadProgressFill.style.width = "0%";
          downloadProgressFill.classList.remove("error");
        }, 2000);
      }
    } catch (err) {
      if (err && err.name === "AbortError") {
        toast("Download cancelled.", "success");
        downloadProgressText.textContent = "Cancelled";
      } else {
        toast(err.message || "Model download failed. Check server logs.");
        downloadProgressFill.classList.add("error");
        downloadProgressText.textContent = "Failed";
      }
      setTimeout(() => {
        downloadProgressContainer.style.display = "none";
        downloadProgressFill.style.width = "0%";
        downloadProgressFill.classList.remove("error");
      }, 2000);
    } finally {
      downloadAbortController = null;
      downloadingModelId = null;
      updateModelBadge();
    }
  });

  btnCancelDownload.addEventListener("click", () => {
    if (downloadAbortController) {
      downloadAbortController.abort();
    }
  });

  // ── Load generated images ─────────────────────────────────────────
  async function loadGenerated() {
    try {
      const images = await fetchJSON("/api/generated");
      if (images.length === 0) {
        galleryGrid.innerHTML =
          '<div class="gallery-empty">No images yet. Generate your first one above!</div>';
        return;
      }
      galleryGrid.innerHTML = images
        .map(
          (img) =>
            `<div class="gallery-item" data-src="${img.url}" data-filename="${img.filename}">
               <img src="${img.url}" alt="${img.filename}" loading="lazy" />
               <div class="gallery-item-overlay">
                 <a class="gallery-download-btn" href="/api/download-image/${img.filename}" download="${img.filename}" title="Save Image">⬇</a>
               </div>
             </div>`
        )
        .join("");

      // Gallery click → lightbox (but not on download button)
      $$(".gallery-item").forEach((item) => {
        item.addEventListener("click", (e) => {
          // Don't open lightbox if download button clicked
          if (e.target.closest(".gallery-download-btn")) return;
          const src = item.dataset.src;
          const filename = item.dataset.filename;
          lightboxImg.src = src;
          lightboxDownload.href = `/api/download-image/${filename}`;
          lightboxDownload.download = filename;
          lightbox.classList.add("active");
        });
      });

      // Stop download button click from propagating
      $$(".gallery-download-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
        });
      });
    } catch {
      // Generated section is nice-to-have; fail silently
    }
  }

  // ── Lightbox close ────────────────────────────────────────────────
  lightbox.addEventListener("click", (e) => {
    // Don't close if clicking the download button or the image
    if (e.target.closest(".lightbox-download-btn")) return;
    lightbox.classList.remove("active");
    lightboxImg.src = "";
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") lightbox.classList.remove("active");
  });

  // ── Image generation ──────────────────────────────────────────────
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const prompt = promptEl.value.trim();
    if (!prompt) {
      toast("Please enter a prompt.");
      promptEl.focus();
      return;
    }

    // Switch UI state
    btnGenerate.disabled = true;
    btnGenerate.classList.add("loading");
    btnGenerate.style.display = "none";
    btnCancel.style.display = "block";
    placeholder.style.display = "none";
    resultWrapper.style.display = "none";
    spinner.classList.add("active");

    try {
      const data = await fetchJSON("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          negative_prompt: negativeEl.value.trim(),
          guidance_scale: parseFloat(guidanceEl.value),
          steps: parseInt(stepsEl.value, 10),
          model_id: modelEl.value,
        }),
      });

      // Show result
      spinner.classList.remove("active");
      resultImg.src = data.image_url;
      resultTime.textContent = `⏱ ${data.generation_time}s`;
      resultDownload.href = `/api/download-image/${data.filename}`;
      resultDownload.download = data.filename;
      resultWrapper.style.display = "block";

      // Also open in lightbox on result click
      resultImg.onclick = () => {
        lightboxImg.src = data.image_url;
        lightboxDownload.href = `/api/download-image/${data.filename}`;
        lightboxDownload.download = data.filename;
        lightbox.classList.add("active");
      };

      toast("Image generated successfully!", "success");

      // Refresh generated section to include new image
      loadGenerated();
    } catch (err) {
      spinner.classList.remove("active");
      placeholder.style.display = "";

      if (err && err.cancelled) {
        toast("Generation cancelled by user.", "warning");
      } else {
        const messages =
          err && err.errors ? err.errors : ["Image generation failed. Check the server logs."];
        messages.forEach((m) => toast(m));
      }
    } finally {
      btnGenerate.disabled = false;
      btnGenerate.classList.remove("loading");
      btnGenerate.style.display = "block";
      btnCancel.style.display = "none";
    }
  });

  // ── Cancel generation ─────────────────────────────────────────────
  btnCancel.addEventListener("click", async () => {
    btnCancel.disabled = true;
    btnCancel.textContent = "Cancelling…";
    try {
      await fetchJSON("/api/cancel", { method: "POST" });
    } catch {
      toast("Failed to send cancel request.");
    } finally {
      btnCancel.disabled = false;
      btnCancel.innerHTML = "✕ Cancel Generation";
    }
  });

  // ── Init ──────────────────────────────────────────────────────────
  loadDevice();
  loadModels();
  loadGenerated();
})();
