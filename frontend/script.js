const API_BASE_URL = "http://localhost:8000";

async function searchImportedProducts() {
    const container = document.getElementById("imported-products");
    container.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`${API_BASE_URL}/recognized_products/imported`);
        const products = await response.json();

        if (products.length === 0) {
            container.innerHTML = "<p>No imported products found.</p>";
        } else {
            products.forEach(product => {
                const div = document.createElement("div");
                div.innerHTML = `
                    <h3>${product.product_name}</h3>
                    <p><strong>Brand:</strong> ${product.brand_name}</p>
                    <p><strong>Origin:</strong> Imported</p>
                `;
                container.appendChild(div);
            });
        }
    } catch (error) {
        console.error("Error fetching imported products:", error);
    }
}

async function searchLocallyMadeProducts() {
    const container = document.getElementById("locally-made-products");
    container.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`${API_BASE_URL}/recognized_products/local`);
        const products = await response.json();

        if (products.length === 0) {
            container.innerHTML = "<p>No locally made products found.</p>";
        } else {
            products.forEach(product => {
                const div = document.createElement("div");
                div.innerHTML = `
                    <h3>${product.product_name}</h3>
                    <p><strong>Brand:</strong> ${product.brand_name}</p>
                    <p><strong>Origin:</strong> Locally made</p>
                `;
                container.appendChild(div);
            });
        }
    } catch (error) {
        console.error("Error fetching locally made products:", error);
    }
}


async function searchProductByName() {
    const name = document.getElementById("search-name").value;
    const container = document.getElementById("search-results-name");
    container.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`${API_BASE_URL}/search_product_by_name?product_name=${name}`);
        const result = await response.json();

        if (!result.recognized) {
            container.innerHTML = `
                <p><strong>Product not recognized.</strong></p>
                <a href="#report-product" style="color: blue; text-decoration: underline;">Do you want to report this product?</a>
            `;
        } else {
            container.innerHTML = `
                <p><strong>Product recognized:</strong> Yes</p>
                <p><strong>Flagged:</strong> ${result.flagged ? "Yes" : "No"}</p>
            `;
        }
    } catch (error) {
        console.error("Error searching product by name:", error);
    }
}

async function searchProductByBrand() {
    const brand = document.getElementById("search-brand").value;
    const container = document.getElementById("search-results-brand");
    container.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`${API_BASE_URL}/search_product_by_brand?brand_name=${brand}`);
        const result = await response.json();

        if (result.flagged_products.length === 0) {
            container.innerHTML = "<p>No products found for this brand.</p>";
        } else {
            result.flagged_products.forEach(product => {
                const div = document.createElement("div");
                div.innerHTML = `
                    <h3>${product.flaged_product_name}</h3>
                    <p><strong>Number of Reports:</strong> ${product.number_of_reports}</p>
                `;
                container.appendChild(div);
            });
        }
    } catch (error) {
        console.error("Error searching product by brand:", error);
    }
}
async function reportProduct() {
    document.getElementById("report-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const report = {
            product_name: document.getElementById("product-name").value,
            brand_name: document.getElementById("brand-name").value,
            social_media_platform: document.getElementById("platform").value,
            post_url: document.getElementById("post-url").value,
            author_name: document.getElementById("author-name").value,
            description: document.getElementById("description").value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/submit_report/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(report)
            });

            if (response.ok) {
                const result = await response.json();

                // Replace the form with a success message
                const formContainer = document.getElementById("report-form").parentElement;
                formContainer.innerHTML = ""; // Remove the form

                const successMessage = document.createElement("div");
                successMessage.innerText = "Report submitted successfully!";
                successMessage.style.color = "green";
                successMessage.style.fontSize = "24px";
                successMessage.style.textAlign = "center";
                successMessage.style.marginTop = "20px";

                formContainer.appendChild(successMessage);
            } else {
                throw new Error("Failed to submit report");
            }
        } catch (error) {
            console.error("Error submitting report:", error);

            // Display an error message inside the form container
            const formContainer = document.getElementById("report-form").parentElement;
            formContainer.innerHTML = ""; // Remove the form

            const errorMessage = document.createElement("div");
            errorMessage.innerText = "An error occurred while submitting the report. Please try again.";
            errorMessage.style.color = "red";
            errorMessage.style.fontSize = "18px";
            errorMessage.style.textAlign = "center";
            errorMessage.style.marginTop = "20px";

            formContainer.appendChild(errorMessage);
        }
    });
}



function navigateToSection(sectionId) {
    const sections = document.querySelectorAll("section");
    sections.forEach((section) => {
        if (section.id === sectionId) {
            section.classList.add("active");
            section.style.display = "block"; // Ensure it is shown
        } else {
            section.classList.remove("active");
            section.style.display = "none"; // Ensure others are hidden
        }
    });

    // Scroll to the top for better user experience
    window.scrollTo(0, 0);
}

// Automatically show the home section on page load
window.onload = () => navigateToSection("Home");

// Attach navigation links to the respective sections
document.querySelectorAll("nav a").forEach((link) => {
    link.addEventListener("click", (event) => {
        event.preventDefault();
        const sectionId = link.getAttribute("href").substring(1); // Get the section ID
        navigateToSection(sectionId);
    });
});
