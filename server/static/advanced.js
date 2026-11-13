/* Show the bounded request count before an Advanced pattern is dispatched. */
(() => {
  "use strict";
  document.addEventListener("input", (event) => {
    const fields = event.target.closest("[data-pattern-fields]");
    const plan = fields && fields.querySelector("[data-request-plan]");
    if (!plan || !plan.dataset.countField) return;
    const field = fields.querySelector(`[name="${plan.dataset.countField}"]`);
    const value = Number(field.value);
    plan.textContent = Number.isInteger(value) && value >= 1 && value <= 5
      ? `Runs ${Number(plan.dataset.countBase) + Number(plan.dataset.countFactor) * value} model requests. No automatic retries. Provider charges apply. Generated reasoning requires your review.`
      : "Choose a depth or round count from 1 to 5 before running.";
  });
})();

const toolPicker = document.getElementById("tool_key");
if (toolPicker) {
  const form = toolPicker.form;
  const count = form.querySelector("[data-tool-request-count]");
  const context = document.getElementById("tool_context");
  const topicLabel = form.querySelector("[data-tool-topic-label]");
  const contextLabel = form.querySelector("[data-tool-context-label]");
  const contextHelp = form.querySelector("[data-tool-context-help]");
  const updateTool = () => {
    const connector = toolPicker.value.endsWith(":subject_connector");
    const requests = toolPicker.selectedOptions[0]?.dataset.requests;
    if (requests) count.textContent = `Runs up to ${requests} model requests.`;
    topicLabel.textContent = connector ? "First subject" : "Topic";
    contextLabel.textContent = connector ? "Second subject" : "Context";
    contextHelp.textContent = connector ? "Give the tool two distinct subjects to compare." : "Optional audience, tone, or constraints.";
    context.required = connector;
  };
  toolPicker.addEventListener("change", updateTool);
  updateTool();
}

(() => {
  function syncPatternShell(shell) {
    if (!shell) {
      return;
    }

    const picker = shell.querySelector("[data-pattern-picker]");
    if (!picker) {
      return;
    }

    const selected = picker.value;

    shell.querySelectorAll("[data-select-pattern]").forEach(function (button) {
      button.classList.toggle("is-active", button.dataset.selectPattern === selected);
    });

    shell.querySelectorAll("[data-pattern-panel]").forEach(function (panel) {
      panel.hidden = panel.dataset.patternPanel !== selected;
    });

    shell.querySelectorAll("[data-pattern-fields]").forEach(function (fieldset) {
      const isActive = fieldset.dataset.patternFields === selected;
      fieldset.hidden = !isActive;
      fieldset.disabled = !isActive;
    });
  }

  function normalizeFillValue(value) {
    if (Array.isArray(value)) {
      return value.join("\n");
    }
    if (typeof value === "boolean") {
      return value ? "true" : "false";
    }
    if (value === null || value === undefined) {
      return "";
    }
    return String(value);
  }

  function readDemoExamples(form) {
    if (!form) {
      return [];
    }

    const source = form.querySelector("[data-demo-examples]");
    if (!source) {
      return [];
    }

    try {
      const parsed = JSON.parse(source.textContent || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (_error) {
      return [];
    }
  }

  function findFillTarget(form, fieldName) {
    if (!form || !fieldName) {
      return null;
    }

    const escapedName = window.CSS && window.CSS.escape ? window.CSS.escape(fieldName) : fieldName;
    return (
      form.querySelector('[name="' + escapedName + '"]:not([disabled])') ||
      form.querySelector('[name="' + escapedName + '"]')
    );
  }

  function updateDemoNote(form, example) {
    const note = form ? form.querySelector("[data-demo-note]") : null;
    if (!note) {
      return;
    }

    if (!note.dataset.defaultText) {
      note.dataset.defaultText = note.textContent || "";
    }

    if (example && example.label) {
      note.textContent = "Loaded demo: " + example.label;
      return;
    }

    note.textContent = note.dataset.defaultText;
  }

  function applyDemoExample(form, example) {
    if (!form || !example || !example.fields) {
      return;
    }

    const fields = example.fields;
    const shell = form.closest("[data-pattern-shell]");
    const patternName = normalizeFillValue(fields.pattern_name || "");

    if (patternName) {
      const picker = findFillTarget(form, "pattern_name");
      if (picker) {
        picker.value = patternName;
        syncPatternShell(shell);
        picker.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }

    Object.entries(fields).forEach(function ([fieldName, rawValue]) {
      const target = findFillTarget(form, fieldName);
      if (!target) {
        return;
      }

      target.value = normalizeFillValue(rawValue);
      target.dispatchEvent(new Event("input", { bubbles: true }));
      target.dispatchEvent(new Event("change", { bubbles: true }));
    });

    updateDemoNote(form, example);
  }

  document.querySelectorAll("[data-pattern-shell]").forEach(syncPatternShell);

  document.addEventListener("click", function (event) {
    const randomFillTrigger = event.target.closest("[data-random-fill-form]");
    if (randomFillTrigger) {
      const form = randomFillTrigger.closest("form");
      const examples = readDemoExamples(form);
      if (examples.length) {
        const selected = examples[Math.floor(Math.random() * examples.length)];
        applyDemoExample(form, selected);
      } else {
        updateDemoNote(form, null);
      }
    }

    const fillTrigger = event.target.closest("[data-fill-target]");
    if (fillTrigger) {
      const target = document.querySelector(fillTrigger.dataset.fillTarget);
      if (target) {
        target.value = fillTrigger.dataset.fillValue || "";
        target.dispatchEvent(new Event("input", { bubbles: true }));
        target.focus();
      }
    }

    const copyTrigger = event.target.closest("[data-copy-nearest]");
    if (copyTrigger) {
      const scope = copyTrigger.closest("[data-copy-scope]") || document;
      const source = scope.querySelector(copyTrigger.dataset.copyNearest);
      if (source && window.copyStudioText) window.copyStudioText(source, copyTrigger);
    }

    const patternTrigger = event.target.closest("[data-select-pattern]");
    if (patternTrigger) {
      const shell = patternTrigger.closest("[data-pattern-shell]");
      const picker = shell ? shell.querySelector("[data-pattern-picker]") : null;
      if (picker) {
        picker.value = patternTrigger.dataset.selectPattern || "";
        syncPatternShell(shell);
      }
    }
  });

  document.addEventListener("change", function (event) {
    const picker = event.target.closest("[data-pattern-picker]");
    if (picker) {
      syncPatternShell(picker.closest("[data-pattern-shell]"));
    }
  });
})();
