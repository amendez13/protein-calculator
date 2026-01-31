const API = {
  async getFoods(search = "") {
    const url = new URL("/api/foods/", window.location.origin);
    if (search) url.searchParams.set("search", search);
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load foods");
    return res.json();
  },

  async logEntry(foodId, quantity, quantityType) {
    const res = await fetch("/api/entries/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        food_item_id: foodId,
        quantity,
        quantity_type: quantityType,
        is_simulation: false,
      }),
    });
    if (!res.ok) {
      const detail = await res.text();
      throw new Error(detail || "Failed to log entry");
    }
    return res.json();
  },

  async getTodaySummary() {
    const res = await fetch("/api/summary/today");
    if (!res.ok) throw new Error("Failed to load summary");
    return res.json();
  },

  async getTodayEntries() {
    const res = await fetch("/api/entries/today");
    if (!res.ok) throw new Error("Failed to load entries");
    return res.json();
  },

  async deleteEntry(entryId) {
    const res = await fetch(`/api/entries/${entryId}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete entry");
  },

  async getSimulationSummary() {
    const res = await fetch("/api/summary/simulation");
    if (!res.ok) throw new Error("Failed to load simulation summary");
    return res.json();
  },

  async getSimulationEntries() {
    const res = await fetch("/api/entries/simulation");
    if (!res.ok) throw new Error("Failed to load simulation entries");
    return res.json();
  },

  async addSimulationEntry(foodId, quantity, quantityType) {
    const res = await fetch("/api/entries/simulation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        food_item_id: foodId,
        quantity,
        quantity_type: quantityType,
        is_simulation: true,
      }),
    });
    if (!res.ok) {
      const detail = await res.text();
      throw new Error(detail || "Failed to add planned entry");
    }
    return res.json();
  },

  async clearSimulation() {
    const res = await fetch("/api/entries/simulation", { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to clear simulation");
  },

  async deleteSimulationEntry(entryId) {
    const res = await fetch(`/api/entries/simulation/${entryId}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete planned entry");
  },

  async getHistory(days = 14) {
    const url = new URL("/api/summary/history", window.location.origin);
    url.searchParams.set("days", String(days));
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load history");
    return res.json();
  },

  async getSettings() {
    const res = await fetch("/api/settings/");
    if (!res.ok) throw new Error("Failed to load settings");
    return res.json();
  },

  async updateSettings(goal) {
    const res = await fetch("/api/settings/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ daily_protein_goal: goal }),
    });
    if (!res.ok) {
      const detail = await res.text();
      throw new Error(detail || "Failed to update settings");
    }
    return res.json();
  },

  async createFood(payload) {
    const res = await fetch("/api/foods/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const detail = await res.text();
      throw new Error(detail || "Failed to create food");
    }
    return res.json();
  },
};

const App = {
  state: {
    entries: [],
    foods: [],
    goal: 150,
    current: 0,
    currentTab: "today",
  },

  init() {
    this.bindTabs();
    this.bindLogForm();
    this.bindEntriesList();
    this.bindSimulationForm();
    this.bindSimulationEntriesList();
    this.bindClearSimulation();
    this.bindHistoryView();
    this.bindSettingsView();
    this.refreshSummary();
    this.loadTodayEntries();
    this.renderViews();
  },

  async refreshSummary() {
    try {
      const summary = await API.getTodaySummary();
      this.state.goal = Number(summary.goal ?? 150);
      this.state.current = Number(summary.total_protein ?? 0);
      this.renderStats();
      this.updateWheel(Number(summary.percentage ?? 0));
      if (this.state.currentTab === "simulation") {
        this.loadSimulation();
      }
    } catch {
      this.renderStats();
      this.updateWheel(0);
    }
  },

  bindTabs() {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => this.setTab(tab.dataset.tab));
    });
  },

  setTab(tabName) {
    if (!tabName) return;
    this.state.currentTab = tabName;
    this.renderTabs();
    this.renderViews();
    if (tabName === "simulation") {
      this.loadSimulation();
    }
    if (tabName === "history") {
      this.loadHistory();
    }
    if (tabName === "settings") {
      this.loadSettings();
      this.loadFoodsAdmin();
    }
  },

  bindLogForm() {
    const form = document.getElementById("log-form");
    const foodSearch = document.getElementById("food-search");
    const foodDropdown = document.getElementById("food-dropdown");
    const selectedFoodId = document.getElementById("selected-food-id");
    const quantity = document.getElementById("quantity");
    const quantityType = document.getElementById("quantity-type");
    const message = document.getElementById("log-message");

    if (!form || !foodSearch || !foodDropdown || !selectedFoodId || !quantity || !quantityType || !message) return;

    const showMessage = (text, kind) => {
      message.classList.toggle("is-error", kind === "error");
      message.classList.toggle("is-success", kind === "success");
      message.textContent = text;
    };

    const hideDropdown = () => {
      foodDropdown.innerHTML = "";
      foodDropdown.setAttribute("hidden", "");
    };

    const renderDropdown = (foods) => {
      if (!foods.length) {
        hideDropdown();
        return;
      }

      foodDropdown.removeAttribute("hidden");
      foodDropdown.innerHTML = foods
        .slice(0, 20)
        .map((food) => {
          const meta = food.serving_size_grams
            ? `${food.protein_per_100g}g/100g • ${food.serving_size_grams}g ${food.serving_name || "serving"}`
            : `${food.protein_per_100g}g/100g`;
          return `
            <div class="dropdown__item" role="option" data-id="${food.id}" data-name="${food.name}">
              ${food.name}
              <span class="dropdown__meta">${meta}</span>
            </div>
          `;
        })
        .join("");
    };

    let searchTimeout = null;
    let lastQuery = "";

    foodSearch.addEventListener("input", () => {
      const query = foodSearch.value.trim();
      lastQuery = query;
      selectedFoodId.value = "";
      showMessage("", "none");

      if (searchTimeout) window.clearTimeout(searchTimeout);
      if (!query) {
        hideDropdown();
        return;
      }

      searchTimeout = window.setTimeout(async () => {
        try {
          const foods = await API.getFoods(query);
          if (lastQuery !== query) return;
          renderDropdown(foods);
        } catch {
          hideDropdown();
        }
      }, 200);
    });

    foodDropdown.addEventListener("click", (e) => {
      const item = e.target.closest(".dropdown__item");
      if (!item) return;
      const id = item.getAttribute("data-id");
      const name = item.getAttribute("data-name");
      if (!id || !name) return;

      selectedFoodId.value = id;
      foodSearch.value = name;
      hideDropdown();
    });

    document.addEventListener("click", (e) => {
      if (e.target === foodSearch) return;
      if (foodDropdown.contains(e.target)) return;
      hideDropdown();
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      showMessage("", "none");

      const foodId = Number(selectedFoodId.value);
      const qty = Number(quantity.value);
      const qtyType = String(quantityType.value || "grams");

      if (!foodId) {
        showMessage("Pick a food from the dropdown.", "error");
        return;
      }
      if (!Number.isFinite(qty) || qty <= 0) {
        showMessage("Enter a quantity greater than 0.", "error");
        return;
      }

      const button = form.querySelector('button[type="submit"]');
      if (button) button.disabled = true;

      try {
        await API.logEntry(foodId, qty, qtyType);
        quantity.value = "";
        selectedFoodId.value = "";
        foodSearch.value = "";
        hideDropdown();
        showMessage("Logged.", "success");
        await this.loadTodayEntries();
        await this.refreshSummary();
      } catch (err) {
        showMessage(err instanceof Error ? err.message : "Failed to log entry.", "error");
      } finally {
        if (button) button.disabled = false;
      }
    });
  },

  bindEntriesList() {
    const list = document.getElementById("entries-list");
    if (!list) return;

    list.addEventListener("click", async (e) => {
      const button = e.target.closest(".delete-btn");
      if (!button) return;
      const id = Number(button.getAttribute("data-id"));
      if (!id) return;

      button.disabled = true;
      try {
        await this.deleteEntry(id);
      } finally {
        button.disabled = false;
      }
    });
  },

  async loadTodayEntries() {
    try {
      const entries = await API.getTodayEntries();
      this.state.entries = Array.isArray(entries) ? entries : [];
      this.renderEntries();
    } catch {
      this.state.entries = [];
      this.renderEntries();
    }
  },

  renderEntries() {
    const list = document.getElementById("entries-list");
    const total = document.getElementById("total-protein");
    if (!list || !total) return;

    const entries = this.state.entries || [];
    if (!entries.length) {
      list.innerHTML = '<div class="empty-state">No entries yet. Log a food above.</div>';
      total.textContent = "0";
      return;
    }

    const formatQuantity = (entry) => {
      const qty = Number(entry.quantity ?? 0);
      const type = String(entry.quantity_type ?? "grams");
      if (type === "servings") return `${qty} servings`;
      return `${qty}g`;
    };

    const sum = entries.reduce((acc, entry) => acc + Number(entry.protein_amount ?? 0), 0);
    total.textContent = String(Math.round(sum * 10) / 10);

    list.innerHTML = entries
      .map((entry) => {
        const name = entry.food_item?.name || "Unknown";
        const qty = formatQuantity(entry);
        const protein = `${Number(entry.protein_amount ?? 0)}g`;
        return `
          <div class="entry-item" data-id="${entry.id}">
            <div class="entry-item__name">${name}</div>
            <div class="entry-item__meta">${qty}</div>
            <div class="entry-item__protein">${protein}</div>
            <button class="delete-btn" type="button" data-id="${entry.id}" aria-label="Delete entry">×</button>
          </div>
        `;
      })
      .join("");
  },

  async deleteEntry(entryId) {
    await API.deleteEntry(entryId);
    await this.loadTodayEntries();
    await this.refreshSummary();
  },

  bindSimulationEntriesList() {
    const list = document.getElementById("simulation-entries");
    if (!list) return;

    list.addEventListener("click", async (e) => {
      const button = e.target.closest(".delete-btn");
      if (!button) return;
      const id = Number(button.getAttribute("data-id"));
      if (!id) return;

      button.disabled = true;
      try {
        await this.deleteSimulationEntry(id);
      } finally {
        button.disabled = false;
      }
    });
  },

  async deleteSimulationEntry(entryId) {
    await API.deleteSimulationEntry(entryId);
    await this.loadSimulation();
  },

  bindSimulationForm() {
    const form = document.getElementById("simulation-form");
    const foodSearch = document.getElementById("sim-food-search");
    const foodDropdown = document.getElementById("sim-food-dropdown");
    const selectedFoodId = document.getElementById("sim-selected-food-id");
    const quantity = document.getElementById("sim-quantity");
    const quantityType = document.getElementById("sim-quantity-type");
    const message = document.getElementById("sim-message");

    if (!form || !foodSearch || !foodDropdown || !selectedFoodId || !quantity || !quantityType || !message) return;

    const showMessage = (text, kind) => {
      message.classList.toggle("is-error", kind === "error");
      message.classList.toggle("is-success", kind === "success");
      message.textContent = text;
    };

    const hideDropdown = () => {
      foodDropdown.innerHTML = "";
      foodDropdown.setAttribute("hidden", "");
    };

    const renderDropdown = (foods) => {
      if (!foods.length) {
        hideDropdown();
        return;
      }

      foodDropdown.removeAttribute("hidden");
      foodDropdown.innerHTML = foods
        .slice(0, 20)
        .map((food) => {
          const meta = food.serving_size_grams
            ? `${food.protein_per_100g}g/100g • ${food.serving_size_grams}g ${food.serving_name || "serving"}`
            : `${food.protein_per_100g}g/100g`;
          return `
            <div class="dropdown__item" role="option" data-id="${food.id}" data-name="${food.name}">
              ${food.name}
              <span class="dropdown__meta">${meta}</span>
            </div>
          `;
        })
        .join("");
    };

    let searchTimeout = null;
    let lastQuery = "";

    foodSearch.addEventListener("input", () => {
      const query = foodSearch.value.trim();
      lastQuery = query;
      selectedFoodId.value = "";
      showMessage("", "none");

      if (searchTimeout) window.clearTimeout(searchTimeout);
      if (!query) {
        hideDropdown();
        return;
      }

      searchTimeout = window.setTimeout(async () => {
        try {
          const foods = await API.getFoods(query);
          if (lastQuery !== query) return;
          renderDropdown(foods);
        } catch {
          hideDropdown();
        }
      }, 200);
    });

    foodDropdown.addEventListener("click", (e) => {
      const item = e.target.closest(".dropdown__item");
      if (!item) return;
      const id = item.getAttribute("data-id");
      const name = item.getAttribute("data-name");
      if (!id || !name) return;

      selectedFoodId.value = id;
      foodSearch.value = name;
      hideDropdown();
    });

    document.addEventListener("click", (e) => {
      if (e.target === foodSearch) return;
      if (foodDropdown.contains(e.target)) return;
      hideDropdown();
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      showMessage("", "none");

      const foodId = Number(selectedFoodId.value);
      const qty = Number(quantity.value);
      const qtyType = String(quantityType.value || "grams");

      if (!foodId) {
        showMessage("Pick a food from the dropdown.", "error");
        return;
      }
      if (!Number.isFinite(qty) || qty <= 0) {
        showMessage("Enter a quantity greater than 0.", "error");
        return;
      }

      const button = form.querySelector('button[type="submit"]');
      if (button) button.disabled = true;

      try {
        await API.addSimulationEntry(foodId, qty, qtyType);
        quantity.value = "";
        selectedFoodId.value = "";
        foodSearch.value = "";
        hideDropdown();
        showMessage("Planned.", "success");
        await this.loadSimulation();
      } catch (err) {
        showMessage(err instanceof Error ? err.message : "Failed to plan entry.", "error");
      } finally {
        if (button) button.disabled = false;
      }
    });
  },

  bindClearSimulation() {
    const button = document.getElementById("clear-simulation");
    if (!button) return;

    button.addEventListener("click", async () => {
      const ok = window.confirm("Clear all planned items?");
      if (!ok) return;
      button.disabled = true;
      try {
        await API.clearSimulation();
        await this.loadSimulation();
      } finally {
        button.disabled = false;
      }
    });
  },

  async loadSimulation() {
    try {
      const [summary, entries] = await Promise.all([API.getSimulationSummary(), API.getSimulationEntries()]);
      this.renderSimulation(summary, Array.isArray(entries) ? entries : []);
    } catch {
      this.renderSimulation({ goal: this.state.goal, actual_protein: this.state.current, simulation_protein: 0, combined_total: this.state.current }, []);
    }
  },

  renderSimulation(summary, entries) {
    const actual = Number(summary.actual_protein ?? 0);
    const planned = Number(summary.simulation_protein ?? 0);
    const combined = Number(summary.combined_total ?? actual + planned);
    const goal = Number(summary.goal ?? this.state.goal ?? 150);

    const simActual = document.getElementById("sim-actual");
    const simPlanned = document.getElementById("sim-planned");
    const simGoal = document.getElementById("sim-goal");
    const simCombined = document.getElementById("sim-combined");

    if (simActual) simActual.textContent = String(actual);
    if (simPlanned) simPlanned.textContent = String(planned);
    if (simGoal) simGoal.textContent = String(goal);
    if (simCombined) simCombined.textContent = `${combined}g`;

    this.updateSimulationWheel(actual, combined, goal);
    this.renderSimulationEntries(entries);
  },

  updateSimulationWheel(actual, combined, goal) {
    const circumference = 314;
    const safeGoal = goal > 0 ? goal : 1;
    const actualPercent = Math.max(0, Math.min(100, (actual / safeGoal) * 100));
    const combinedPercent = Math.max(0, Math.min(100, (combined / safeGoal) * 100));

    const actualCircle = document.querySelector(".progress-wheel--sim .progress--actual");
    const plannedCircle = document.querySelector(".progress-wheel--sim .progress--planned");
    if (!actualCircle || !plannedCircle) return;

    plannedCircle.style.strokeDashoffset = String(circumference - (combinedPercent / 100) * circumference);
    actualCircle.style.strokeDashoffset = String(circumference - (actualPercent / 100) * circumference);
  },

  renderSimulationEntries(entries) {
    const container = document.getElementById("simulation-entries");
    if (!container) return;

    if (!entries.length) {
      container.innerHTML = '<div class="empty-state">No planned items yet.</div>';
      return;
    }

    const formatQuantity = (entry) => {
      const qty = Number(entry.quantity ?? 0);
      const type = String(entry.quantity_type ?? "grams");
      if (type === "servings") return `${qty} servings`;
      return `${qty}g`;
    };

    container.innerHTML = entries
      .map((entry) => {
        const name = entry.food_item?.name || "Unknown";
        const qty = formatQuantity(entry);
        const protein = `${Number(entry.protein_amount ?? 0)}g`;
        return `
          <div class="entry-item" data-id="${entry.id}">
            <div class="entry-item__name">${name}</div>
            <div class="entry-item__meta">${qty}</div>
            <div class="entry-item__protein">${protein}</div>
            <button class="delete-btn" type="button" data-id="${entry.id}" aria-label="Remove planned item">×</button>
          </div>
        `;
      })
      .join("");
  },

  bindHistoryView() {
    // No-op for now; reserved for future interactions (date range, etc).
  },

  async loadHistory() {
    try {
      const items = await API.getHistory(14);
      this.renderHistory(Array.isArray(items) ? items : []);
    } catch {
      this.renderHistory([]);
    }
  },

  renderHistory(items) {
    const list = document.getElementById("history-list");
    if (!list) return;

    if (!items.length) {
      list.innerHTML = '<div class="empty-state">No history yet.</div>';
      return;
    }

    const fmt = new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" });

    list.innerHTML = items
      .map((item) => {
        const day = new Date(String(item.date));
        const total = Number(item.total_protein ?? 0);
        const goal = Number(item.goal ?? 150);
        const percent = goal > 0 ? Math.max(0, Math.min(100, (total / goal) * 100)) : 0;
        return `
          <div class="history-day">
            <span class="history-day__date">${fmt.format(day)}</span>
            <div class="mini-progress" style="--progress: ${percent}%"></div>
            <span class="history-day__total">${total}g / ${goal}g</span>
          </div>
        `;
      })
      .join("");
  },

  bindSettingsView() {
    const saveGoal = document.getElementById("save-goal");
    const goalInput = document.getElementById("goal-input");
    const settingsMessage = document.getElementById("settings-message");
    const foodsSearch = document.getElementById("foods-search");
    const addFoodForm = document.getElementById("add-food-form");
    const addFoodMessage = document.getElementById("add-food-message");

    if (saveGoal && goalInput && settingsMessage) {
      const showSettingsMessage = (text, kind) => {
        settingsMessage.classList.toggle("is-error", kind === "error");
        settingsMessage.classList.toggle("is-success", kind === "success");
        settingsMessage.textContent = text;
      };

      saveGoal.addEventListener("click", async () => {
        showSettingsMessage("", "none");
        const goal = Number(goalInput.value);
        if (!Number.isFinite(goal) || goal < 1 || goal > 500) {
          showSettingsMessage("Goal must be between 1 and 500.", "error");
          return;
        }

        saveGoal.disabled = true;
        try {
          await API.updateSettings(goal);
          showSettingsMessage("Saved.", "success");
          await this.refreshSummary();
          if (this.state.currentTab === "history") await this.loadHistory();
          if (this.state.currentTab === "simulation") await this.loadSimulation();
        } catch (err) {
          showSettingsMessage(err instanceof Error ? err.message : "Failed to save.", "error");
        } finally {
          saveGoal.disabled = false;
        }
      });
    }

    if (foodsSearch) {
      let timer = null;
      foodsSearch.addEventListener("input", () => {
        if (timer) window.clearTimeout(timer);
        timer = window.setTimeout(() => this.loadFoodsAdmin(foodsSearch.value.trim()), 200);
      });
    }

    if (addFoodForm && addFoodMessage) {
      const showAddFoodMessage = (text, kind) => {
        addFoodMessage.classList.toggle("is-error", kind === "error");
        addFoodMessage.classList.toggle("is-success", kind === "success");
        addFoodMessage.textContent = text;
      };

      addFoodForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        showAddFoodMessage("", "none");

        const name = document.getElementById("add-food-name")?.value?.trim() || "";
        const proteinPer100g = Number(document.getElementById("add-food-protein")?.value);
        const category = document.getElementById("add-food-category")?.value?.trim() || null;
        const servingSize = Number(document.getElementById("add-food-serving-grams")?.value);
        const servingName = document.getElementById("add-food-serving-name")?.value?.trim() || null;

        if (!name) {
          showAddFoodMessage("Name is required.", "error");
          return;
        }
        if (!Number.isFinite(proteinPer100g) || proteinPer100g < 0) {
          showAddFoodMessage("Protein per 100g must be 0 or greater.", "error");
          return;
        }

        const payload = {
          name,
          protein_per_100g: proteinPer100g,
          category: category || undefined,
          serving_size_grams: Number.isFinite(servingSize) && servingSize > 0 ? servingSize : undefined,
          serving_name: servingName || undefined,
        };

        const button = addFoodForm.querySelector('button[type="submit"]');
        if (button) button.disabled = true;

        try {
          await API.createFood(payload);
          showAddFoodMessage("Food created.", "success");
          addFoodForm.reset();
          await this.loadFoodsAdmin(foodsSearch?.value?.trim() || "");
        } catch (err) {
          showAddFoodMessage(err instanceof Error ? err.message : "Failed to create food.", "error");
        } finally {
          if (button) button.disabled = false;
        }
      });
    }
  },

  async loadSettings() {
    const goalInput = document.getElementById("goal-input");
    if (!goalInput) return;
    try {
      const settings = await API.getSettings();
      goalInput.value = String(Number(settings.daily_protein_goal ?? this.state.goal ?? 150));
    } catch {
      goalInput.value = String(this.state.goal ?? 150);
    }
  },

  async loadFoodsAdmin(search = "") {
    const list = document.getElementById("foods-list");
    if (!list) return;

    try {
      const foods = await API.getFoods(search);
      if (!foods.length) {
        list.innerHTML = '<div class="empty-state">No foods found.</div>';
        return;
      }
      list.innerHTML = foods
        .slice(0, 50)
        .map((food) => {
          const meta = `${food.protein_per_100g}g/100g${food.category ? ` • ${food.category}` : ""}`;
          return `
            <div class="food-row">
              <div class="food-row__name">${food.name}</div>
              <div class="food-row__meta">${meta}</div>
            </div>
          `;
        })
        .join("");
    } catch {
      list.innerHTML = '<div class="empty-state">Failed to load foods.</div>';
    }
  },

  updateWheel(percentage) {
    const clamped = Math.max(0, Math.min(100, percentage));
    const circle = document.querySelector(".progress-wheel .progress");
    if (!circle) return;

    const circumference = 314;
    const offset = circumference - (clamped / 100) * circumference;
    circle.style.strokeDashoffset = String(offset);
  },

  renderTabs() {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((tab) => {
      tab.classList.toggle("is-active", tab.dataset.tab === this.state.currentTab);
    });
  },

  renderViews() {
    const views = document.querySelectorAll(".view");
    views.forEach((view) => {
      const isActive = view.dataset.view === this.state.currentTab;
      view.toggleAttribute("hidden", !isActive);
    });
  },

  renderStats() {
    const goal = document.getElementById("stats-goal");
    const current = document.getElementById("stats-current");
    const wheelCurrent = document.getElementById("current-protein");

    if (goal) goal.textContent = String(this.state.goal);
    if (current) current.textContent = String(this.state.current);
    if (wheelCurrent) wheelCurrent.textContent = `${this.state.current}g`;
  },
};

document.addEventListener("DOMContentLoaded", () => App.init());
