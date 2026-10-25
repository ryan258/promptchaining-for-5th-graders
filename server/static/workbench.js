/* Small enhancements only. Saving, running, exporting and restoring use HTML forms. */
(() => {
  "use strict";
  let messageTimer;
  window.studioMessage = (message) => {
    const box = document.getElementById("studio-message");
    if (!box) return;
    box.textContent = message;
    box.hidden = false;
    clearTimeout(messageTimer);
    messageTimer = setTimeout(() => { box.hidden = true; }, 6500);
  };
  window.copyStudioText = (source, button) => {
    const selectForCopy = () => {
      source.setAttribute("tabindex", "-1");
      source.focus();
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = window.getSelection();
      if (selection) { selection.removeAllRanges(); selection.addRange(range); }
      window.studioMessage("Copy is unavailable. The text is selected; use your system's copy command.");
    };
    if (!navigator.clipboard) { selectForCopy(); return; }
    navigator.clipboard.writeText(source.innerText.trim()).then(() => {
      const label = button.dataset.originalLabel || button.textContent;
      button.dataset.originalLabel = label;
      button.textContent = "Copied";
      window.studioMessage("Answer copied.");
      setTimeout(() => { button.textContent = label; }, 1400);
    }).catch(selectForCopy);
  };

  const editor = document.querySelector("[data-chain-editor]");
  if (editor) {
    const list = editor.querySelector("[data-step-list]");
    const template = document.getElementById("new-step-template");
    const draftStatus = editor.querySelector("[data-draft-status]");
    const discard = editor.querySelector("[data-discard-draft]");
    const key = "prompt-studio:draft:v1:" + editor.dataset.draftKey;
    let storageWorks = true;
    let lastRemoved = null;
    const undo = document.createElement("button");
    undo.type = "button";
    undo.className = "quiet-button";
    undo.textContent = "Undo removed step";
    undo.hidden = true;
    editor.querySelector("[data-add-step]").after(undo);

    function readEditor() {
      const value = {};
      ["title", "description", "topic", "context", "audience", "model"].forEach((name) => {
        const field = editor.elements.namedItem(name);
        if (field) value[name] = field.value;
      });
      value.review_each = editor.elements.namedItem("review_each").checked;
      value.steps = Array.from(list.querySelectorAll("[data-step]")).map((node) => ({
        name: node.querySelector('[name="step_name"]').value,
        purpose: node.querySelector('[name="step_purpose"]').value,
        prompt: node.querySelector('[name="step_prompt"]').value,
      }));
      return value;
    }
    const original = readEditor();

    function renumber() {
      const steps = list.querySelectorAll("[data-step]");
      steps.forEach((node, index) => {
        node.querySelector("[data-step-number]").textContent = String(index + 1).padStart(2, "0");
        node.querySelector("[data-step-label]").textContent = node.querySelector('[name="step_name"]').value || "Untitled step";
        node.querySelector("[data-purpose-label]").textContent = node.querySelector('[name="step_purpose"]').value;
        node.querySelector("[data-step-up]").disabled = index === 0;
        node.querySelector("[data-step-down]").disabled = index === steps.length - 1;
        node.querySelector("[data-step-remove]").disabled = steps.length === 1;
      });
      editor.querySelector("[data-add-step]").disabled = steps.length >= 8;
    }

    function applyDraft(value) {
      if (!value || !Array.isArray(value.steps) || value.steps.length < 1 || value.steps.length > 8) return false;
      if (!value.steps.every((s) => s && typeof s.name === "string" && typeof s.prompt === "string" && typeof s.purpose === "string")) return false;
      ["title", "description", "topic", "context", "audience", "model"].forEach((name) => {
        const field = editor.elements.namedItem(name);
        if (field && typeof value[name] === "string") {
          // A model removed from configuration is never reintroduced from a draft.
          if (field.tagName !== "SELECT" || Array.from(field.options).some((o) => o.value === value[name])) field.value = value[name];
        }
      });
      if (typeof value.review_each === "boolean") editor.elements.namedItem("review_each").checked = value.review_each;
      list.replaceChildren();
      value.steps.forEach((step) => {
        const fragment = template.content.cloneNode(true);
        fragment.querySelector('[name="step_name"]').value = step.name;
        fragment.querySelector('[name="step_purpose"]').value = step.purpose;
        fragment.querySelector('[name="step_prompt"]').value = step.prompt;
        fragment.querySelector("details").open = false;
        list.append(fragment);
      });
      renumber();
      return true;
    }

    function saveDraft() {
      renumber();
      try {
        localStorage.setItem(key, JSON.stringify({ ...readEditor(), saved_at: new Date().toISOString() }));
        storageWorks = true;
        draftStatus.textContent = "Draft saved in this browser. Save the recipe or prepare a chain to keep it in workspace backups.";
      } catch (_error) {
        storageWorks = false;
        draftStatus.textContent = "Browser draft storage is unavailable. Use Save recipe to keep your changes on this computer.";
      }
    }

    try {
      const raw = localStorage.getItem(key);
      if (raw && raw.length <= 300000 && applyDraft(JSON.parse(raw))) {
        draftStatus.textContent = "Recovered your draft from this browser. Nothing has been sent to a model.";
        discard.hidden = false;
      }
    } catch (_error) {
      storageWorks = false;
      draftStatus.textContent = "Browser draft recovery is unavailable. Use Save recipe to keep your work.";
    }
    renumber();

    editor.addEventListener("input", saveDraft);
    editor.addEventListener("change", saveDraft);
    editor.addEventListener("invalid", (event) => {
      const step = event.target.closest("details");
      if (step) step.open = true;
    }, true);
    editor.addEventListener("submit", (event) => {
      saveDraft();
      if (event.submitter && event.submitter.value === "run" && !editor.elements.namedItem("topic").value.trim()) {
        event.preventDefault();
        editor.elements.namedItem("topic").focus();
        window.studioMessage("Give the chain a topic before preparing it.");
      }
    });

    editor.addEventListener("click", (event) => {
      const example = event.target.closest("[data-topic-example]");
      if (example) {
        const field = editor.querySelector("[data-intention]");
        field.value = example.dataset.topicExample;
        field.focus();
        saveDraft();
        return;
      }
      if (event.target.closest("[data-add-step]")) {
        if (list.children.length >= 8) return;
        list.append(template.content.cloneNode(true));
        renumber();
        list.lastElementChild.querySelector("input").focus();
        saveDraft();
        return;
      }
      const node = event.target.closest("[data-step]");
      if (!node) return;
      if (event.target.closest("[data-step-remove]") && list.children.length > 1) {
        lastRemoved = { node, next: node.nextElementSibling };
        node.remove();
        undo.hidden = false;
        undo.focus();
        window.studioMessage("Step removed. Undo is available beside Add a step. Review any output references.");
        saveDraft();
      } else if (event.target.closest("[data-step-up]") && node.previousElementSibling) {
        list.insertBefore(node, node.previousElementSibling);
        saveDraft();
        node.querySelector("summary").focus();
      } else if (event.target.closest("[data-step-down]") && node.nextElementSibling) {
        list.insertBefore(node.nextElementSibling, node);
        saveDraft();
        node.querySelector("summary").focus();
      }
    });
    undo.addEventListener("click", () => {
      if (!lastRemoved || list.children.length >= 8) return;
      list.insertBefore(lastRemoved.node, lastRemoved.next && lastRemoved.next.parentNode === list ? lastRemoved.next : null);
      lastRemoved.node.querySelector("summary").focus();
      lastRemoved = null;
      undo.hidden = true;
      saveDraft();
    });
    discard.addEventListener("click", () => {
      applyDraft(original);
      try { localStorage.removeItem(key); } catch (_error) { storageWorks = false; }
      discard.hidden = true;
      draftStatus.textContent = storageWorks ? "Recovered draft discarded. The saved recipe is restored." : "The saved recipe is restored. Browser storage is unavailable.";
      editor.querySelector("[data-intention]").focus();
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.isComposing || event.repeat) return;
    const typing = event.target.closest && event.target.closest('input, textarea, select, [contenteditable="true"]');
    if (event.altKey && !event.ctrlKey && !event.metaKey && !typing && event.code === "KeyN") {
      event.preventDefault(); window.location.assign("/studio/recipes");
    } else if (event.altKey && !event.ctrlKey && !event.metaKey && !typing && event.code === "KeyL") {
      event.preventDefault(); window.location.assign("/studio/library");
    } else if ((event.metaKey || event.ctrlKey) && !event.altKey && event.code === "KeyS" && editor) {
      event.preventDefault(); editor.requestSubmit(editor.querySelector("[data-save-recipe]"));
    } else if ((event.metaKey || event.ctrlKey) && !event.altKey && event.code === "Enter") {
      const button = editor ? editor.querySelector("[data-prepare-run]") : document.querySelector("[data-primary-action]");
      if (button && !button.disabled) { event.preventDefault(); button.form.requestSubmit(button); }
    }
  });

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-go-back]")) {
      if (window.history.length > 1) window.history.back();
      else window.location.assign("/studio/recipes");
    }
    const anchor = event.target.closest('a[href^="#answer-"]');
    if (anchor) {
      const panel = document.getElementById(anchor.getAttribute("href").slice(1));
      if (panel) panel.open = true;
    }
  });
  document.addEventListener("submit", (event) => {
    if (event.defaultPrevented || event.target.hasAttribute("hx-post")) return;
    const form = event.target;
    if (form.dataset.submitting) { event.preventDefault(); return; }
    form.dataset.submitting = "true";
    // Keep the submitter's name/value in the native request.
    setTimeout(() => form.querySelectorAll('button[type="submit"]').forEach((b) => { b.disabled = true; }), 0);
  });
  window.addEventListener("pageshow", () => {
    document.querySelectorAll("form[data-submitting]").forEach((form) => {
      delete form.dataset.submitting;
      form.querySelectorAll('button[type="submit"]').forEach((b) => { b.disabled = b.hasAttribute("data-prepare-run") && !form.querySelector('[name="model"]'); });
    });
  });
  document.addEventListener("htmx:afterSwap", (event) => {
    const workspace = document.getElementById("run-workspace");
    if (workspace && workspace.dataset.runState !== "running" && event.detail.target.id === "run-workspace") {
      window.studioMessage(workspace.dataset.runState === "completed" ? "Chain complete. Every answer is saved." : "Progress saved. The chain is ready for your review.");
    }
  });
  document.addEventListener("htmx:sendError", () => {
    window.studioMessage("Progress could not refresh. Your completed steps are saved. Use Refresh progress when the connection returns.");
  });
})();
