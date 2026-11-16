(() => {
  "use strict";

  const dashboard = document.getElementById("dashboard");
  const loadError = document.getElementById("load-error");
  const sourceIndex = new Map();
  const moneyFormatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  });
  const integerFormatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

  function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    })[char]);
  }

  function safeURL(value) {
    try {
      const parsed = new URL(value);
      return parsed.protocol === "https:" ? parsed.href : "";
    } catch (_error) {
      return "";
    }
  }

  function money(value) {
    return typeof value === "number" && Number.isFinite(value)
      ? moneyFormatter.format(value)
      : "";
  }

  function sourceLink(sourceId, extraClass = "") {
    const source = sourceIndex.get(sourceId);
    if (!source) return "";
    const url = safeURL(source.url);
    if (!url) return "";
    return `<a class="source-chip ${escapeHTML(extraClass)}" href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer" aria-label="Open official source: ${escapeHTML(source.title)}">${escapeHTML(source.short)}</a>`;
  }

  function sourceLinks(sourceIds, extraClass = "") {
    const links = (sourceIds || []).map((id) => sourceLink(id, extraClass)).filter(Boolean).join("");
    return links ? `<div class="source-links">${links}</div>` : `<span class="cell-sub">No linked source</span>`;
  }

  function renderCellValue(value, note = "") {
    const display = typeof value === "number" ? money(value) : String(value ?? "");
    if (!display) return `<span class="empty-value" aria-label="Not confirmed">—</span>`;
    return `<span class="money">${escapeHTML(display)}</span>${note ? `<span class="cell-note">${escapeHTML(note)}</span>` : ""}`;
  }

  function eventSearchText(event) {
    return [event.venue, event.title, event.dates, event.time, event.policy, event.terms, event.entryReview]
      .filter(Boolean).join(" ").toLocaleLowerCase();
  }

  function extraRow(event) {
    let badgeClass = "badge-review";
    if (event.policyType === "unlimited") badgeClass = "badge-reentry";
    if (event.policyType === "limited") badgeClass = "badge-extra";
    const dateLabel = event.dates || "Date not confirmed";
    const timeLabel = event.time || "";
    return `<tr>
      <td><strong>${escapeHTML(event.venue)}</strong><span class="cell-sub">${escapeHTML(event.title)}</span></td>
      <td><strong>${escapeHTML(dateLabel)}</strong>${timeLabel ? `<span class="cell-sub">${escapeHTML(timeLabel)}</span>` : "<span class=\"empty-value\" aria-label=\"Start time unresolved\">—</span>"}</td>
      <td>${renderCellValue(event.buyIn, event.buyIn === null ? "Conflicting official values; see terms." : "")}</td>
      <td>${renderCellValue(event.guarantee)}</td>
      <td><span class="badge ${badgeClass}">${escapeHTML(event.policy)}</span><span class="cell-note">${escapeHTML(event.terms)}</span></td>
      <td>${sourceLinks(event.sourceIds)}</td>
    </tr>`;
  }

  function candidateRow(event) {
    const ratio = event.buyIn && event.guarantee ? event.guarantee / event.buyIn : null;
    return `<tr>
      <td><strong>${escapeHTML(event.venue)}</strong><span class="cell-sub">${escapeHTML(event.title)}</span></td>
      <td><strong>${escapeHTML(event.dates || "Date not confirmed")}</strong>${event.time ? `<span class="cell-sub">${escapeHTML(event.time)}</span>` : "<span class=\"empty-value\" aria-label=\"Start time unresolved\">—</span>"}</td>
      <td>${renderCellValue(event.buyIn)}</td>
      <td>${renderCellValue(event.guarantee)}</td>
      <td>${ratio ? `<span class="money">${integerFormatter.format(ratio)}×</span>` : "<span class=\"empty-value\" aria-label=\"Not available\">—</span>"}</td>
      <td><span class="badge badge-review">Entry cap unknown</span><span class="cell-note">${escapeHTML(event.entryReview)}</span></td>
      <td>${sourceLinks(event.sourceIds)}</td>
    </tr>`;
  }

  function renderFilteredRows(data, type) {
    const rowsElement = document.getElementById(type === "extra" ? "extra-rows" : "candidate-rows");
    const searchElement = document.getElementById(type === "extra" ? "extra-search" : "candidate-search");
    const sortElement = type === "candidate" ? document.getElementById("candidate-sort") : null;
    const search = searchElement.value.trim().toLocaleLowerCase();
    let events = type === "extra" ? [...data.extraEvents] : [...data.candidateEvents];
    events = events.filter((event) => !search || eventSearchText(event).includes(search));

    if (sortElement) {
      const sortBy = sortElement.value;
      events.sort((left, right) => {
        if (sortBy === "buyin") {
          return (left.buyIn ?? Number.POSITIVE_INFINITY) - (right.buyIn ?? Number.POSITIVE_INFINITY)
            || (left.date || "9999").localeCompare(right.date || "9999");
        }
        if (sortBy === "ratio") {
          const leftRatio = left.buyIn && left.guarantee ? left.guarantee / left.buyIn : -1;
          const rightRatio = right.buyIn && right.guarantee ? right.guarantee / right.buyIn : -1;
          return rightRatio - leftRatio || (left.date || "9999").localeCompare(right.date || "9999");
        }
        return (left.date || "9999").localeCompare(right.date || "9999");
      });
    }

    if (!events.length) {
      const colspan = type === "extra" ? 6 : 7;
      rowsElement.innerHTML = `<tr><td colspan="${colspan}" class="empty-row">No events match this filter. Try a venue, event number, or game type.</td></tr>`;
      return;
    }
    rowsElement.innerHTML = events.map(type === "extra" ? extraRow : candidateRow).join("");
  }

  function renderDailyRooms(data) {
    document.getElementById("daily-room-list").innerHTML = data.dailyRooms.map((room) => `
      <div class="daily-room-item">
        <span class="daily-room-time">${escapeHTML(room.times)}</span>
        <div><strong>${escapeHTML(room.venue)}</strong><p>${escapeHTML(room.details)}</p></div>
        ${sourceLinks(room.sourceIds)}
      </div>`).join("");
  }

  function renderConflictSources(data) {
    document.getElementById("conflict-sources").innerHTML = sourceLinks(data.conflictSources);
  }

  function renderChart(data) {
    const unique = new Map();
    [...data.extraEvents, ...data.candidateEvents].forEach((event) => {
      if (typeof event.buyIn !== "number" || typeof event.guarantee !== "number" || event.buyIn <= 0) return;
      const key = `${event.venue}|${event.title}`;
      if (!unique.has(key)) unique.set(key, { ...event, ratio: event.guarantee / event.buyIn });
    });
    const rows = [...unique.values()].sort((a, b) => b.ratio - a.ratio).slice(0, 9);
    const chart = document.getElementById("guarantee-chart");
    if (!rows.length) {
      chart.innerHTML = `<p class="cell-sub">No comparable buy-in / guarantee pairs are confirmed.</p>`;
      return;
    }
    const max = rows[0].ratio;
    chart.innerHTML = rows.map((event) => {
      const width = Math.max(2, (event.ratio / max) * 100);
      const label = `${event.title} · ${event.venue}`;
      return `<div class="chart-row" title="${escapeHTML(label)}">
        <span class="chart-label">${escapeHTML(event.title)}</span>
        <span class="chart-track" aria-hidden="true"><span class="chart-fill" style="width:${width.toFixed(1)}%"></span></span>
        <span class="chart-value">${integerFormatter.format(event.ratio)}×</span>
      </div>`;
    }).join("");
    chart.setAttribute("aria-label", `Top published guarantee to buy-in ratios: ${rows.map((row) => `${row.title}, ${integerFormatter.format(row.ratio)} to one`).join("; ")}`);
  }

  function renderHotels(data) {
    document.getElementById("hotel-rows").innerHTML = data.hotels.map((hotel) => `
      <tr>
        <td><strong>${escapeHTML(hotel.hotel)}</strong><span class="cell-sub">${escapeHTML(hotel.room)}</span></td>
        <td><span class="hotel-quality">${escapeHTML(hotel.signal)}</span></td>
        <td><span class="walk-status">${escapeHTML(hotel.walk)}</span></td>
        <td><span class="money">${escapeHTML(hotel.fee)}</span></td>
        <td><span class="money">${escapeHTML(hotel.feeFourNights)}</span></td>
        <td><span class="badge badge-review">${escapeHTML(hotel.fullStay)}</span><span class="cell-note">No usable date-specific quote</span></td>
        <td>${sourceLinks(hotel.sourceIds)}</td>
      </tr>`).join("");
    document.getElementById("hotel-notes").innerHTML = data.hotelNotes.map((note) => `
      <article class="hotel-note"><strong>${escapeHTML(note.title)}</strong><p>${escapeHTML(note.text)}</p>${sourceLinks(note.sourceIds)}</article>`).join("");
  }

  function renderList(elementId, items) {
    document.getElementById(elementId).innerHTML = items.map((item) => `<li>${escapeHTML(item)}</li>`).join("");
  }

  function renderQuestions(data) {
    document.getElementById("questions-list").innerHTML = data.questions.map((item) => `<li>${escapeHTML(item)}</li>`).join("");
  }

  function renderSuggestions(data) {
    document.getElementById("suggestion-grid").innerHTML = data.suggestions.map((item, index) => `
      <article class="suggestion-card">
        <span class="suggestion-number">SUGGESTION ${String(index + 1).padStart(2, "0")}</span>
        <h3>${escapeHTML(item.title)}</h3>
        <p>${escapeHTML(item.text)}</p>
        <span class="suggestion-tag">${escapeHTML(item.tag)}</span>
      </article>`).join("");
    document.getElementById("decision-paths").innerHTML = `
      <h3>Choose your path</h3>
      ${data.decisionPaths.map((item) => `<article class="path-card"><strong>${escapeHTML(item.title)}</strong><p>${escapeHTML(item.text)}</p></article>`).join("")}`;
  }

  function renderSources(data) {
    const groups = new Map();
    data.sources.forEach((source) => {
      if (!groups.has(source.group)) groups.set(source.group, []);
      groups.get(source.group).push(source);
    });
    document.getElementById("source-groups").innerHTML = [...groups.entries()].map(([group, sources], index) => `
      <details class="source-group" ${index === 0 ? "open" : ""}>
        <summary>${escapeHTML(group)} <span class="cell-sub">${sources.length} official links</span></summary>
        <div class="source-list">${sources.map((source) => {
          const url = safeURL(source.url);
          if (!url) return "";
          return `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer" title="${escapeHTML(source.note)}"><span>${escapeHTML(source.title)}</span><span>Open ↗</span></a>`;
        }).join("")}</div>
      </details>`).join("");
    document.getElementById("source-reviewed").textContent = data.reviewedLabel;
  }

  function renderDayPlan(data) {
    document.getElementById("day-plan-list").innerHTML = data.dayPlan.map((item) => `
      <article class="timeline-item">
        <time class="timeline-time">${escapeHTML(item.time)}</time>
        <div class="timeline-content"><strong>${escapeHTML(item.title)}</strong><p>${escapeHTML(item.text)}</p>${sourceLinks(item.sourceIds)}</div>
        <span class="timeline-kind">${escapeHTML(item.kind)}</span>
      </article>`).join("");
  }

  function render(data) {
    data.sources.forEach((source) => sourceIndex.set(source.id, source));
    document.getElementById("single-count").textContent = "0";
    document.getElementById("extra-count").textContent = String(data.extraEvents.length);
    document.getElementById("hotel-count").textContent = String(data.hotels.length);
    renderDailyRooms(data);
    renderConflictSources(data);
    renderHotels(data);
    renderList("known-list", data.known);
    renderList("missing-list", data.missing);
    renderQuestions(data);
    renderSuggestions(data);
    renderSources(data);
    renderDayPlan(data);
    renderChart(data);
    renderFilteredRows(data, "extra");
    renderFilteredRows(data, "candidate");

    document.getElementById("extra-search").addEventListener("input", () => renderFilteredRows(data, "extra"));
    document.getElementById("candidate-search").addEventListener("input", () => renderFilteredRows(data, "candidate"));
    document.getElementById("candidate-sort").addEventListener("change", () => renderFilteredRows(data, "candidate"));
    dashboard.hidden = false;
  }

  fetch("./data.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch((error) => {
      console.error("Unable to load dashboard data:", error);
      loadError.hidden = false;
    });
})();
