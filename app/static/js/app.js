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
    this.refreshSummary();
    this.renderViews();
  },

  async refreshSummary() {
    try {
      const summary = await API.getTodaySummary();
      this.state.goal = Number(summary.goal ?? 150);
      this.state.current = Number(summary.total_protein ?? 0);
      this.renderStats();
      this.updateWheel(Number(summary.percentage ?? 0));
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
        await this.refreshSummary();
      } catch (err) {
        showMessage(err instanceof Error ? err.message : "Failed to log entry.", "error");
      } finally {
        if (button) button.disabled = false;
      }
    });
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
