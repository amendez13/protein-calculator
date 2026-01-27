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
    this.updateWheel(0);
    this.renderStats();
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
