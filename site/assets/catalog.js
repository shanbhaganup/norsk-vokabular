(() => {
  const app = document.getElementById("catalog-app");
  if (!app) return;

  const searchInput = document.getElementById("word-search");
  const resultCount = document.getElementById("result-count");
  const wordList = document.getElementById("word-list");
  const showMore = document.getElementById("show-more");
  const detail = document.getElementById("entry-detail");
  const pageSize = 50;
  let entries = [];
  let filteredEntries = [];
  let visibleCount = pageSize;
  let selectedId = "";

  const normalize = (value) => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase();
  const tokens = (value) => normalize(value).match(/[\p{L}\p{N}]+/gu) || [];
  const node = (tag, className, value) => {
    const item = document.createElement(tag);
    if (className) item.className = className;
    if (value !== undefined) item.textContent = value;
    return item;
  };
  const clear = (element) => { while (element.firstChild) element.removeChild(element.firstChild); };

  function prepareSearch(entry) {
    const meaning = normalize(`${entry.index_english || ""} ${entry.english || ""}`).trim();
    entry.search = {
      lemma: normalize(entry.lemma),
      meaning,
      meaningTokens: tokens(meaning),
      topics: normalize((entry.topics || []).join(" ")),
      topicTokens: tokens((entry.topics || []).join(" ")),
      type: normalize(`${entry.index_type || ""} ${entry.word_type || ""} ${entry.sense || ""}`),
      forms: normalize((entry.forms || []).map((form) => `${form.label} ${form.value}`).join(" ")),
    };
    return entry;
  }

  function searchRank(entry, query) {
    const fields = entry.search;
    if (fields.lemma === query) return 0;
    if (fields.lemma.startsWith(query)) return 1;
    if (fields.lemma.includes(query)) return 2;
    if (fields.meaning === query) return 3;
    if (fields.meaningTokens.includes(query)) return 4;
    if (fields.meaning.startsWith(query)) return 5;
    if (fields.meaningTokens.some((word) => word.startsWith(query))) return 6;
    if (fields.meaning.includes(query)) return 7;
    if (fields.topicTokens.includes(query)) return 8;
    if (fields.topicTokens.some((word) => word.startsWith(query))) return 9;
    if (fields.type.includes(query)) return 10;
    if (fields.forms.includes(query)) return 11;
    return -1;
  }

  function renderResults() {
    const query = normalize(searchInput.value.trim());
    if (query) {
      filteredEntries = entries
        .map((entry) => ({ entry, rank: searchRank(entry, query) }))
        .filter((result) => result.rank >= 0)
        .sort((a, b) => a.rank - b.rank || a.entry.lemma.localeCompare(b.entry.lemma, "nb"))
        .map((result) => result.entry);
    } else {
      filteredEntries = entries;
    }
    const count = Math.min(visibleCount, filteredEntries.length);
    resultCount.textContent = query
      ? `Showing ${count.toLocaleString()} of ${filteredEntries.length.toLocaleString()} matching words.`
      : `Showing ${count.toLocaleString()} of ${filteredEntries.length.toLocaleString()} words. Type to search.`;
    clear(wordList);

    if (filteredEntries.length === 0) {
      const empty = node("li", "empty-results", "No words match that search.");
      wordList.append(empty);
      showMore.hidden = true;
      selectedId = "";
      clear(detail);
      detail.append(node("p", "", "No entry matches this search."));
      return;
    }

    const visible = filteredEntries.slice(0, count);
    for (const entry of visible) {
      const li = node("li");
      const button = node("button", "word-option");
      button.type = "button";
      button.dataset.entryId = entry.id;
      button.setAttribute("aria-current", entry.id === selectedId ? "true" : "false");
      const headword = node("strong", "word-headword", entry.lemma);
      const meaning = node("span", "word-meaning", entry.index_english || entry.english);
      const meta = node("span", "word-meta", `${entry.index_type || entry.word_type} · ${(entry.topics || []).join("; ")}`);
      button.append(headword, meaning, meta);
      button.addEventListener("click", () => selectEntry(entry));
      li.append(button);
      wordList.append(li);
    }
    showMore.hidden = count >= filteredEntries.length;

    if (!selectedId && visible.length) selectEntry(visible[0], false);
    else if (selectedId && !visible.some((entry) => entry.id === selectedId)) {
      const first = visible[0];
      if (first) selectEntry(first, false);
    }
  }

  function addMetadata(list, label, value) {
    if (!value) return;
    list.append(node("dt", "", label), node("dd", "", value));
  }

  function plainMarkdown(value) {
    return String(value || "")
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1 ($2)")
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/\*(.*?)\*/g, "$1")
      .replace(/`([^`]+)`/g, "$1");
  }

  function renderSources(sources) {
    const list = node("ul", "source-list");
    for (const source of sources || []) {
      const li = node("li");
      if (/^https?:\/\//i.test(source.url || "")) {
        const link = node("a", "", source.label);
        link.href = source.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        li.append(link);
      } else {
        li.textContent = source.url ? `${source.label} (${source.url})` : source.label;
      }
      list.append(li);
    }
    return list;
  }

  function renderEntry(entry) {
    clear(detail);
    detail.append(node("h2", "", entry.lemma));
    detail.append(node("p", "entry-meaning", entry.english));

    if ((entry.topics || []).length) {
      const topics = node("div", "topic-list");
      topics.setAttribute("aria-label", "Topics");
      for (const topic of entry.topics) topics.append(node("span", "topic-chip", topic));
      detail.append(topics);
    }

    const metadata = node("dl", "entry-metadata");
    addMetadata(metadata, "Word type / gender", entry.index_type || entry.word_type);
    addMetadata(metadata, "Sense", entry.sense);
    addMetadata(metadata, "Checked on", entry.checked_on);
    addMetadata(metadata, "Entry ID", entry.id);
    if (entry.index_english && entry.index_english !== entry.english) addMetadata(metadata, "Index meaning", entry.index_english);
    detail.append(metadata);

    detail.append(node("h3", "", "Forms and examples"));
    if ((entry.forms || []).length) {
      const wrap = node("div", "form-table-wrap");
      const table = node("table", "form-table");
      const thead = node("thead");
      const headerRow = node("tr");
      for (const label of ["Form / feature", "Value", "Norwegian example", "English translation"]) headerRow.append(node("th", "", label));
      thead.append(headerRow);
      const tbody = node("tbody");
      for (const form of entry.forms) {
        const row = node("tr");
        for (const value of [form.label, form.value, form.example, form.translation]) row.append(node("td", "", value));
        tbody.append(row);
      }
      table.append(thead, tbody);
      wrap.append(table);
      detail.append(wrap);
    } else {
      detail.append(node("p", "", "No form table is available for this entry."));
    }

    if (entry.form_status) {
      detail.append(node("h3", "", "Form status"));
      detail.append(node("p", "", entry.form_status));
    }
    if (entry.notes) {
      detail.append(node("h3", "", "Notes"));
      detail.append(node("p", "entry-notes", plainMarkdown(entry.notes)));
    }
    if ((entry.sources || []).length) {
      detail.append(node("h3", "", "Sources"));
      detail.append(renderSources(entry.sources));
    }
  }

  function selectEntry(entry, updateList = true) {
    selectedId = entry.id;
    renderEntry(entry);
    for (const button of wordList.querySelectorAll(".word-option")) {
      button.setAttribute("aria-current", button.dataset.entryId === selectedId ? "true" : "false");
    }
    if (updateList) renderResults();
  }

  searchInput.addEventListener("input", () => {
    visibleCount = pageSize;
    renderResults();
  });
  showMore.addEventListener("click", () => {
    visibleCount += pageSize;
    renderResults();
  });

  fetch("./data/vocabulary.json")
    .then((response) => { if (!response.ok) throw new Error("Vocabulary data is not available"); return response.json(); })
    .then((data) => {
      entries = data.map(prepareSearch);
      renderResults();
    })
    .catch((error) => { resultCount.textContent = `${error.message}. Generate site data and reload.`; });
})();
