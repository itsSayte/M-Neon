async function loadTree() {

    const response = await fetch("/api/tree");
    const data = await response.json();

    let html = "";
    let serverCount = 0;

    data.forEach(category => {

        html += `
            <div class="category">
                <div class="category-title">
                    📁 ${category.name}
                </div>
        `;

        category.servers.forEach(server => {

            serverCount++;

            html += `
                <div class="server">
                    🖥️ ${server.name}
                </div>
            `;
        });

        html += "</div>";
    });

    document.getElementById("tree").innerHTML = html;
    document.getElementById("catCount").innerText = data.length;
    document.getElementById("serverCount").innerText = serverCount;
}

async function createCategory() {

    const name = document.getElementById("categoryName").value;

    if (!name) {
        alert("Veuillez saisir un nom de catégorie");
        return;
    }

    await fetch("/api/category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name
        })
    });

    document.getElementById("categoryName").value = "";

    loadTree();
}

async function loadCategories() {

    const response = await fetch("/api/tree");
    const data = await response.json();

    const select = document.getElementById(
        "modalServerCategory"
    );

    select.innerHTML = "";

    data.forEach(category => {

        const option =
            document.createElement("option");

        option.value = category.name;
        option.textContent = category.name;

        select.appendChild(option);
    });
}

function openModal() {

    document.getElementById(
        "serverModal"
    ).style.display = "flex";

    loadCategories();
}

function closeModal() {

    document.getElementById(
        "serverModal"
    ).style.display = "none";
}

async function createServer() {

    const payload = {

        name: document.getElementById(
            "modalServerName"
        ).value,

        category: document.getElementById(
            "modalServerCategory"
        ).value,

        type: document.getElementById(
            "serverType"
        ).value,

        version: document.getElementById(
            "serverVersion"
        ).value,

        ram_min: document.getElementById(
            "ramMin"
        ).value,

        ram_max: document.getElementById(
            "ramMax"
        ).value
    };

    if (!payload.name) {
        alert("Veuillez saisir un nom de serveur");
        return;
    }

    await fetch("/api/server", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    document.getElementById(
        "modalServerName"
    ).value = "";

    document.getElementById(
        "serverVersion"
    ).value = "";

    document.getElementById(
        "ramMin"
    ).value = "";

    document.getElementById(
        "ramMax"
    ).value = "";

    closeModal();
    loadTree();
}

window.onclick = function(event) {

    const modal =
        document.getElementById("serverModal");

    if (event.target === modal) {
        closeModal();
    }
}

loadTree();