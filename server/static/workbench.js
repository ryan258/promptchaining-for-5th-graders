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
    const draftConflict = editor.querySelector("[data-draft-conflict]");
    let lastSavedDraft = null;
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

    function setDraftStatus(message) {
      if (draftStatus.textContent !== message) draftStatus.textContent = message;
    }

    function showDraftConflict() {
      draftConflict.hidden = false;
      setDraftStatus("Another tab changed this draft. Choose which version to keep.");
    }

    function saveDraft(force = false) {
      renumber();
      try {
        if (force !== true && localStorage.getItem(key) !== lastSavedDraft) {
          showDraftConflict();
          return;
        }
        const draft = JSON.stringify({ ...readEditor(), saved_at: new Date().toISOString() });
        localStorage.setItem(key, draft);
        lastSavedDraft = draft;
        draftConflict.hidden = true;
        storageWorks = true;
        setDraftStatus("Draft saved in this browser. Save the recipe or prepare a chain to keep it in workspace backups.");
      } catch (_error) {
        storageWorks = false;
        setDraftStatus("Browser draft storage is unavailable. Use Save recipe to keep your changes on this computer.");
      }
    }

    try {
      lastSavedDraft = localStorage.getItem(key);
      if (!editor.hasAttribute("data-form-error") && lastSavedDraft && lastSavedDraft.length <= 300000
          && applyDraft(JSON.parse(lastSavedDraft))) {
        setDraftStatus("Recovered your draft from this browser. Nothing has been sent to a model.");
        discard.hidden = false;
      }
    } catch (_error) {
      storageWorks = false;
      setDraftStatus("Browser draft recovery is unavailable. Use Save recipe to keep your work.");
    }
    renumber();

    window.addEventListener("storage", (event) => {
      if (event.storageArea === localStorage && (event.key === key || event.key === null) && event.newValue !== lastSavedDraft) {
        showDraftConflict();
      }
    });
    editor.querySelector("[data-keep-this-draft]").addEventListener("click", () => {
      saveDraft(true);
      editor.querySelector("[data-intention]").focus();
    });
    editor.querySelector("[data-load-other-draft]").addEventListener("click", () => {
      try {
        const raw = localStorage.getItem(key);
        if (!(raw ? raw.length <= 300000 && applyDraft(JSON.parse(raw)) : applyDraft(original))) {
          setDraftStatus("The other draft could not be loaded. Your visible text is still here.");
          return;
        }
        lastSavedDraft = raw;
        lastRemoved = null;
        undo.hidden = true;
        discard.hidden = !raw;
        draftConflict.hidden = true;
        setDraftStatus(raw ? "Loaded the other tab’s draft." : "The other tab discarded its draft. The saved recipe is open.");
        editor.querySelector("[data-intention]").focus();
      } catch (_error) {
        setDraftStatus("The other draft could not be loaded. Your visible text is still here.");
      }
    });

    function reorderSteps(before, after, restoredStep = null) {
      const changes = new Map();
      for (const [index, node] of after.entries()) {
        const sourceOrder = node === restoredStep ? lastRemoved.order : before;
        const sourceIndex = sourceOrder.indexOf(node);
        const prompt = node.querySelector('[name="step_prompt"]');
        let broken = false;
        const remapped = prompt.value.replace(/\{\{\s*output\[-([1-8])\](\.[A-Za-z_][A-Za-z0-9_]*)?\s*\}\}/g,
          (reference, offset, field = "") => {
            const original = sourceOrder[sourceIndex - Number(offset)];
            const targetIndex = after.indexOf(original);
            if (targetIndex < 0 || targetIndex >= index) {
              broken = true;
              return reference;
            }
            return `{{output[-${index - targetIndex}]${field}}}`;
          });
        if (broken) {
          window.studioMessage(`This change would break a handoff in “${node.querySelector('[name="step_name"]').value}”. Edit that prompt first.`);
          return false;
        }
        changes.set(prompt, remapped);
      }
      for (const [prompt, remapped] of changes) prompt.value = remapped;
      list.replaceChildren(...after);
      return true;
    }

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
      const order = Array.from(list.children);
      const index = order.indexOf(node);
      if (event.target.closest("[data-step-remove]") && list.children.length > 1) {
        if (!reorderSteps(order, order.filter((step) => step !== node))) return;
        lastRemoved = { node, next: order[index + 1], order };
        undo.hidden = false;
        undo.focus();
        window.studioMessage("Step removed. Undo is available beside Add a step.");
        saveDraft();
      } else {
        const direction = event.target.closest("[data-step-up]") ? -1 : event.target.closest("[data-step-down]") ? 1 : 0;
        const neighbor = index + direction;
        if (!direction || neighbor < 0 || neighbor >= order.length) return;
        const moved = [...order];
        [moved[index], moved[neighbor]] = [moved[neighbor], moved[index]];
        if (!reorderSteps(order, moved)) return;
        saveDraft();
        node.querySelector("summary").focus();
      }
    });
    undo.addEventListener("click", () => {
      if (!lastRemoved || list.children.length >= 8) return;
      const order = Array.from(list.children);
      const restored = [...order];
      const nextIndex = order.indexOf(lastRemoved.next);
      restored.splice(nextIndex === -1 ? order.length : nextIndex, 0, lastRemoved.node);
      if (!reorderSteps(order, restored, lastRemoved.node)) return;
      lastRemoved.node.querySelector("summary").focus();
      lastRemoved = null;
      undo.hidden = true;
      saveDraft();
    });
    discard.addEventListener("click", () => {
      if (!draftConflict.hidden) {
        showDraftConflict();
        return;
      }
      applyDraft(original);
      try { localStorage.removeItem(key); lastSavedDraft = null; } catch (_error) { storageWorks = false; }
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
      const activeForm = event.target.closest?.("form");
      const button = editor ? editor.querySelector("[data-prepare-run]")
        : activeForm?.querySelector("[data-primary-action]") || document.querySelector("[data-primary-action]");
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
  let runView;
  document.addEventListener("htmx:beforeSwap", (event) => {
    const target = event.detail.target;
    if (!event.detail.shouldSwap || target.id !== "run-workspace") return;
    const focus = document.activeElement;
    runView = {
      details: Array.from(target.querySelectorAll("details[id]"), (panel) => [panel.id, panel.open]),
      focus: target.contains(focus) ? { id: focus.id, detailsId: focus.closest("details[id]")?.id } : null,
      state: target.dataset.runState,
    };
  });
  document.addEventListener("htmx:afterSwap", (event) => {
    const workspace = document.getElementById("run-workspace");
    if (!workspace || !runView || event.detail.target.id !== "run-workspace") return;
    for (const [id, open] of runView.details) {
      const panel = document.getElementById(id);
      if (panel) panel.open = open;
    }
    if (runView.focus) {
      const { id, detailsId } = runView.focus;
      const control = document.getElementById(id) || document.getElementById(detailsId)?.querySelector("summary");
      (control || document.getElementById("run-action-heading"))?.focus();
    }
    const messages = {
      completed: "Chain complete. Every answer is saved.",
      paused: "Progress saved. The chain is ready for your review.",
      failed: "A step needs attention. Open the run message for details.",
      interrupted: "This run was interrupted. Open the run message for details.",
      "save-pending": "An answer is waiting to be saved on this computer.",
    };
    const state = workspace.dataset.runState;
    if (state !== runView.state && messages[state]) window.studioMessage(messages[state]);
    runView = null;
  });
  document.addEventListener("htmx:sendError", () => {
    window.studioMessage("Progress could not refresh. Your completed steps are saved. Use Refresh progress when the connection returns.");
  });
})();
