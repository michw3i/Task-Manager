
// CONNECTING FRONT TO BACK API
const API = "http://127.0.0.1:5000"; // Flask default
let currentUser = { id: null, name: ""};
let events = {};
let currentDate = new Date();

async function api(path, opts = {}){
  try {
    const res = await fetch(API + path, {
      headers: {"Content-Type": "application/json"},
      ...opts,
    });
    if (!res.ok){
      const msg = await res.text().catch(() => res.statusText);
      throw new Error(`Server error (${res.status}): ${msg || res.statusText}`);
    }
    return res.json();
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Cannot connect to server. Make sure the backend is running on http://127.0.0.1:5000');
    }
    throw error;
  }
}

// Create/find user and cache id/name
async function ensureUser(name){
  const data = await api("/user", {
    method: "POST",
    body: JSON.stringify({name}),
  });
  currentUser = { id: data.user_id, name: data.name || name};
}

// Pull all tasks for currentUser and rebuild events
async function syncFromServer(){
  if (!currentUser.name) return;
  const data = await api(`/tasks/${encodeURIComponent(currentUser.name)}`);
  events = {};
  for (const t of (data.tasks || [])){
    const d = (t.due_date || "").trim()
    if (!d) continue;
    if (!events[d]) events[d] = [];
    events[d].push({id: t.id, description: t.description});
  }
}

// Add a task for currentUser 
async function addTask(description, due_date){
  if (!currentUser.id) throw new Error ("No user selected");
  await api("/task", {
    method: "POST",
    body: JSON.stringify({
      user_id: currentUser.id,
      description,
      due_date
    }),
  });
}
           // Dynamic page loader: intercept clicks on local .html links and load them into an embedded area
            async function loadPage(url) {
                try {
                    const res = await fetch(url);
                    if (!res.ok) throw new Error('Failed to load ' + url + ': ' + res.status);
                    const html = await res.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');

                    // Move stylesheet links from the fetched head into current document head (avoid duplicates)
                    const links = Array.from(doc.querySelectorAll('link[rel="stylesheet"]'));
                    links.forEach(link => {
                        const href = link.href || link.getAttribute('href');
                        if (href && !document.querySelector('link[rel="stylesheet"][href="' + href + '"]')) {
                            const newLink = document.createElement('link');
                            newLink.rel = 'stylesheet';
                            newLink.href = href;
                            document.head.appendChild(newLink);
                        }
                    });

                    // Special case: Calendar.html -> inject calendar portion into the existing todo list area
                    if (url.endsWith('Calendar.html')) {
                        const todoList = document.getElementById('todoList');
                        if (!todoList) return;

                        // Build an embedded container to host the calendar markup
                        const container = document.createElement('div');
                        container.id = 'embeddedCalendar';
                        container.className = 'embedded-page';

                        // Extract calendar-related elements from the fetched document
                        // Prefer elements with ids used in Calendar.html
      events[dateStr].forEach((task, idx) => {
        const evDiv = document.createElement("div");
        evDiv.textContent = task.description;
        evDiv.classList.add("event");

        // Delete button
        const delBtn = document.createElement("span");
        delBtn.textContent = "×";
        delBtn.classList.add("delete");
        delBtn.onclick = async (e) => {
          e.stopPropagation();
          try {
            // Delete from server
            if (task.id) {
              await api(`/task/${task.id}`, { method: "DELETE" });
            }
            // Remove from local events
            events[dateStr].splice(idx, 1);
            if (events[dateStr].length === 0) delete events[dateStr];
            generateCalendar(currentDate);
          } catch (err) {
            alert("Error deleting task: " + err.message);
          }
                        // Execute scripts from fetched document so the calendar interactivity initializes
                        const scripts = Array.from(doc.querySelectorAll('script'));
                        scripts.forEach(s => {
                            const newScript = document.createElement('script');
                            if (s.src) {
                                // Convert relative src to absolute based on url
                                const src = s.getAttribute('src');
                                const base = url.substring(0, url.lastIndexOf('/') + 1);
                                newScript.src = src.startsWith('http') ? src : base + src;
                            } else {
                                newScript.textContent = s.textContent;
                            }
                            // Append to container to keep scope close to embedded content
                            container.appendChild(newScript);
                        });

                        return;
                    }

                    // Default behavior: inject body content (fallback)
                    // Remove top-level navigation from fetched content to avoid duplicate nav bars
                    const navs = doc.querySelectorAll('.navigation');
                    navs.forEach(n => n.remove());
                    const bodyEl = document.getElementById('body');
                    bodyEl.innerHTML = doc.body.innerHTML;

document.getElementById("eventForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("Name").value.trim();
  const date = document.getElementById("eventDate").value;
  const text = document.getElementById("eventText").value.trim();

  if (!name || !date || !text) return;

  try{
    // Makes sure user still exists (server returns user_id)
    if (!currentUser.name || currentUser.name !== name){
      await ensureUser(name);
    }

    // Add task to database
    await addTask(text, date);

    // Pull fresh tasks from server
    await syncFromServer();
    generateCalendar(currentDate);

    // Clear form
    e.target.reset();
  } catch (err){
    alert("Error: " + err.message);
  }
});                 });

                } catch (err) {
                    console.error(err);
                    document.getElementById('body').innerHTML = '<p style="color:red">Unable to load page: ' + err.message + '</p>';
                }
            }

            // Global click handler to intercept local HTML links
            document.addEventListener('click', function(e) {
                const a = e.target.closest('a');
                if (!a) return;
                const href = a.getAttribute('href');
                if (!href) return;
                // Only intercept relative HTML pages in the same folder
                if (href.endsWith('.html') && !href.startsWith('http') && !href.startsWith('mailto:')) {
                    e.preventDefault();
                    loadPage(href);
                }
            });

            // Show the to-do fieldset only after entering name
            (function attachTodoHandlers() {
                const nameForm = document.querySelector('form[action=""]');
                if (nameForm) {
                    nameForm.addEventListener('submit', function(event) {
                        event.preventDefault();
                        const value = document.getElementById('name').value;
                        document.getElementById('result').innerHTML = 'To-do for ' + value + ':<br><br>';
                        document.getElementById('todoFieldset').style.display = '';
                    });
                }

                const todoForm = document.getElementById('todoForm');
                if (todoForm) {
                    todoForm.addEventListener('submit', function(event) {
                        event.preventDefault();
                        const todoText = document.getElementById('todo').value.trim();
                        const dueDate = document.getElementById('dueDate').value;
                        if (todoText) {
                            const li = document.createElement('li');
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            // When checkbox is checked, apply strikethrough
                            checkbox.addEventListener('change', function() {
                                if (checkbox.checked) {
                                    li.classList.add('strikethrough');
                                } else {
                                    li.classList.remove('strikethrough');
                                }
                            });
                            li.appendChild(checkbox);
                            li.appendChild(document.createTextNode(' ' + todoText));
                            if (dueDate) {
                                const due = document.createElement('span');
                                due.className = 'due-date';
                                due.textContent = 'Due: ' + dueDate;
                                li.appendChild(due);
                            }
                            const listEl = document.getElementById('todoList');
                            if (listEl) listEl.appendChild(li);
                            document.getElementById('todo').value = '';
                            document.getElementById('dueDate').value = '';
                        }
                    });
                }
            })()