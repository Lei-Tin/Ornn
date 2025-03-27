function adjustCardHeight(listElement) {
    const card = listElement.closest('.toggle-card');
    if (card && card.classList.contains('expanded')) {
        requestAnimationFrame(() => {
            card.style.maxHeight = card.scrollHeight + "px";
        });
    }
}


// Add listener for toggle cards
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.toggle-card[data-expandable="true"]').forEach(card => {
        if (card.classList.contains('expanded')) {
            requestAnimationFrame(() => {
                card.style.maxHeight = card.scrollHeight + "px";
            });
        } else if (card.classList.contains('collapsed')) {
            requestAnimationFrame(() => {
                card.style.maxHeight = "60px";
            });
        }

        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.attributeName === 'class') {
                    if (card.classList.contains('expanded')) {
                        requestAnimationFrame(() => {
                            card.style.maxHeight = card.scrollHeight + "px";
                        });
                    } else if (card.classList.contains('collapsed')) {
                        requestAnimationFrame(() => {
                            card.style.maxHeight = "60px";
                        });
                    }
                }
            });
        });

        observer.observe(card, { attributes: true });
    });
});



// Send updated setting to the backend
async function updateSetting(setting, value) {
    const response = await fetch('/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ setting, value }),
    });
    const result = await response.json();

    // Debug purposes
    console.log(result.message);
}

// Fetch champions from backend
async function fetchChampions() {
    const response = await fetch('/champions');
    const data = await response.json();
    championsList = data.champions.sort();
}

// Handle checkbox toggle
function toggleFeature(feature) {
    const checkbox = document.getElementById(feature);
    const isChecked = checkbox.checked;

    // Update the backend with the new state
    updateSetting(feature, isChecked);

    // Fetch updated champions list if ranked mode toggle is changed
    if (feature === 'ranked_mode_enabled') {
        fetchChampions();
    }

    const card = document.getElementById(`${feature}_card`);

    if (isChecked) {
        card.classList.add('expanded');
        card.classList.remove('collapsed');
    } else {
        card.classList.add('collapsed');
        card.classList.remove('expanded');
    }
}

// Handle adding champions to a list
function addChampion(listId, championName) {
    const list = document.getElementById(listId);
    const existing = Array.from(list.children).map(li => li.firstChild.textContent);

    if (existing.includes(championName)) return; // Avoid duplicates

    const listItem = document.createElement('li');
    listItem.textContent = championName;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Remove';
    deleteButton.onclick = function () {
        list.removeChild(listItem);
        updateChampionList(listId);
        adjustCardHeight(list);
    };

    listItem.appendChild(deleteButton);
    list.appendChild(listItem);

    adjustCardHeight(list);

    updateChampionList(listId);
}

// Update champion list on the backend
async function updateChampionList(listId) {
    const list = document.getElementById(listId);
    const champions = Array.from(list.children).map((item) => item.firstChild.textContent);
    const setting = listId === 'ban_list' ? 'auto_ban_list_champions' : 'auto_lock_in_champions';

    await updateSetting(setting, champions);
}

// Store fetched champions for search functionality
let championsList = [];

// Fetch champions on page load
document.addEventListener("DOMContentLoaded", fetchChampions);

// Display champions dropdown
function displayChampionsDropdown(filtered, dropdown, input) {
    dropdown.innerHTML = '';

    // Find curr list
    const curr_list_type = dropdown.id.includes('lock_in') ? 'lock_in_list' : 'ban_list';

    // Remove champs that are already in the dropdown of lock_in_list
    const curr_lock_in_list = Array.from(document.getElementById(curr_list_type).children)
        .map(child => child.firstChild.textContent.trim());

    filtered = filtered.filter(champ => !curr_lock_in_list.includes(champ));

    if (filtered.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    dropdown.style.display = 'block';

    filtered.forEach(champ => {
        const li = document.createElement('li');
        li.textContent = champ;
        li.onclick = () => {
            addChampion(curr_list_type, champ);
            input.value = '';
            dropdown.innerHTML = '';
            dropdown.style.display = 'none';
        };
        dropdown.appendChild(li);
    });
}

// Search champions based on input
function searchChampions(inputId, dropdownId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    input.onfocus = () => {
        const query = input.value.toLowerCase().trim();
        // Check if query is empty, if its empty, then I display everything
        var filtered;

        if (query === '') {
            filtered = championsList;
        } else {
            filtered = championsList.filter(name => name.toLowerCase().includes(query));
        }

        displayChampionsDropdown(filtered, dropdown, input);
    };

    input.oninput = () => {
        const query = input.value.toLowerCase().trim();
        var filtered;

        // Check if query is empty, if its empty, then I display everything
        if (query === '') {
            filtered = championsList;
        } else {
            filtered = championsList.filter(name => name.toLowerCase().includes(query));
        }

        displayChampionsDropdown(filtered, dropdown, input);
    };

    input.onblur = () => setTimeout(() => { dropdown.style.display = 'none'; }, 100);
}